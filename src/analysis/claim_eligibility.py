"""Citation eligibility for technical claims used as execution rationale.

Policy version ``claim-v2`` (Issue #36): a geometric FVG/OB is not automatically
eligible as *core execution* evidence. Overlapping opposite structure, thin
gaps vs ATR, unbound reaction IDs, or unverified fact relationships demote the
claim to supporting / observation / uncitable.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Literal

from src.analysis.ict_pa import FairValueGap, TimeframeAnalysis
from src.analysis.price_action_facts import build_price_action_summaries
from src.core.types import LevelProposal, MarketContext

CLAIM_POLICY_VERSION = "claim-v2"

CitationEligibility = Literal[
    "core_execution",
    "supporting",
    "observation_only",
    "uncitable",
]

# Calibrated floors for claim-v2 (documented; can be replaced by backtest table later).
MIN_FVG_WIDTH_ATR_FOR_CORE = 0.35
MAX_COUNTER_OVERLAP_PTS = 0.5  # treat as overlapping if interval distance <= this
MAX_CLAIM_NEAR_PTS = 0.5


@dataclass
class ClaimAudit:
    claim_id: str
    fact_ids: list[str] = field(default_factory=list)
    eligibility: CitationEligibility = "observation_only"
    quality: dict[str, Any] = field(default_factory=dict)
    counterevidence: list[dict[str, Any]] = field(default_factory=list)
    reaction_evidence_id: str = ""
    policy_version: str = CLAIM_POLICY_VERSION
    reasons: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @property
    def allows_execution_authorization(self) -> bool:
        return self.eligibility == "core_execution"


def _overlap_amount(a_lo: float, a_hi: float, b_lo: float, b_hi: float) -> float:
    lo = max(min(a_lo, a_hi), min(b_lo, b_hi))
    hi = min(max(a_lo, a_hi), max(b_lo, b_hi))
    return max(0.0, hi - lo)


def _zones_near(a_lo: float, a_hi: float, b_lo: float, b_hi: float, *, tol: float) -> bool:
    if _overlap_amount(a_lo, a_hi, b_lo, b_hi) > 0:
        return True
    # Gap between intervals
    if max(a_lo, a_hi) < min(b_lo, b_hi):
        return (min(b_lo, b_hi) - max(a_lo, a_hi)) <= tol
    if max(b_lo, b_hi) < min(a_lo, a_hi):
        return (min(a_lo, a_hi) - max(b_lo, b_hi)) <= tol
    return False


def _reaction_index(reactions: list[dict[str, Any]] | None) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for row in reactions or []:
        rid = str(row.get("id") or "").strip()
        if rid:
            out[rid] = row
    return out


def _collect_fvgs(analyses: dict[str, TimeframeAnalysis]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for tf, analysis in analyses.items():
        atr = float(analysis.atr) if analysis.atr else None
        for idx, fvg in enumerate(analysis.active_fvgs or analysis.fvgs or []):
            if not isinstance(fvg, FairValueGap):
                continue
            low, high = float(fvg.low), float(fvg.high)
            width = abs(high - low)
            width_atr = (width / atr) if atr and atr > 0 else None
            fact_base = f"{tf}.fvg.{idx}"
            rows.append(
                {
                    "tf": tf,
                    "direction": fvg.direction,
                    "low": low,
                    "high": high,
                    "width": round(width, 4),
                    "width_atr_ratio": round(width_atr, 4) if width_atr is not None else None,
                    "atr": atr,
                    "fact_ids": [f"{fact_base}.low", f"{fact_base}.high"],
                    "kind": "fvg",
                }
            )
    return rows


def technical_claim_fact_catalog(
    ctx: MarketContext,
    *,
    price_action: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    """Return the canonical technical facts an LLM may bind into a reaction.

    Zone facts expose their two registry-compatible boundary IDs as a single
    entity. Point facts (PA S/R and volume-profile levels) expose one ID. The
    model can explain these facts in prose, but only IDs from this catalog are
    eligible for deterministic relationship checks.
    """
    rows: list[dict[str, Any]] = []
    for tf, analysis in ctx.analyses.items():
        for idx, fvg in enumerate(analysis.active_fvgs or analysis.fvgs or []):
            if not isinstance(fvg, FairValueGap):
                continue
            low, high = sorted((float(fvg.low), float(fvg.high)))
            rows.append(
                {
                    "fact_ids": [f"{tf}.fvg.{idx}.low", f"{tf}.fvg.{idx}.high"],
                    "kind": "fvg",
                    "timeframe": tf,
                    "direction": fvg.direction,
                    "low": low,
                    "high": high,
                    "as_of": str(fvg.time),
                }
            )
        for idx, ob in enumerate(analysis.order_blocks or []):
            low, high = sorted((float(ob.low), float(ob.high)))
            rows.append(
                {
                    "fact_ids": [f"{tf}.ob.{idx}.low", f"{tf}.ob.{idx}.high"],
                    "kind": "order_block",
                    "timeframe": tf,
                    "direction": ob.direction,
                    "low": low,
                    "high": high,
                    "as_of": str(ob.time),
                }
            )

    pa_blocks = (
        price_action
        if price_action is not None
        else build_price_action_summaries(ctx.enriched) if ctx.enriched else {}
    )
    for tf, block in pa_blocks.items():
        if not isinstance(block, dict):
            continue
        profile = block.get("volume_profile") or {}
        for key in ("poc", "vah", "val"):
            raw = profile.get(key)
            try:
                price = float(raw)
            except (TypeError, ValueError):
                continue
            rows.append(
                {
                    "fact_ids": [f"pa.{tf}.{key}"],
                    "kind": key,
                    "timeframe": tf,
                    "direction": "neutral",
                    "low": price,
                    "high": price,
                    "price": price,
                }
            )
        for idx, level in enumerate(block.get("sr_levels") or []):
            if not isinstance(level, dict):
                continue
            try:
                price = float(level.get("price"))
            except (TypeError, ValueError):
                continue
            kind = str(level.get("kind") or "").lower()
            direction = str(level.get("direction") or "").lower()
            if direction not in ("bullish", "bearish"):
                direction = "bullish" if kind == "support" else "bearish" if kind == "resistance" else "neutral"
            rows.append(
                {
                    "fact_ids": [f"pa.{tf}.sr.{idx}"],
                    "kind": kind or "sr",
                    "timeframe": tf,
                    "direction": direction,
                    "low": price,
                    "high": price,
                    "price": price,
                }
            )
    return rows


def _fact_entity_for_ids(
    fact_ids: list[str], catalog: list[dict[str, Any]]
) -> dict[str, Any] | None:
    wanted = {str(fid).strip() for fid in fact_ids if str(fid).strip()}
    if not wanted:
        return None
    for row in catalog:
        available = {str(fid) for fid in row.get("fact_ids") or []}
        if wanted == available:
            return row
    return None


def _fact_direction_supports_trade(fact: dict[str, Any], direction: str) -> bool:
    fact_direction = str(fact.get("direction") or "neutral").lower()
    wanted = "bearish" if direction == "SELL" else "bullish"
    return fact_direction in (wanted, "neutral")


def _relationship_holds(
    relation_type: str,
    left: dict[str, Any],
    right: dict[str, Any],
) -> bool:
    left_low, left_high = float(left["low"]), float(left["high"])
    right_low, right_high = float(right["low"]), float(right["high"])
    if relation_type == "overlap":
        # Point facts may sit exactly on a zone boundary, so inclusive interval
        # intersection is intentional here.
        return max(left_low, right_low) <= min(left_high, right_high)
    if relation_type == "near":
        return _zones_near(
            left_low,
            left_high,
            right_low,
            right_high,
            tol=MAX_CLAIM_NEAR_PTS,
        )
    if relation_type == "contradiction":
        opposite = {str(left.get("direction")), str(right.get("direction"))} == {
            "bullish",
            "bearish",
        }
        return opposite and _zones_near(
            left_low,
            left_high,
            right_low,
            right_high,
            tol=MAX_CLAIM_NEAR_PTS,
        )
    return False


def _aligned_fvgs(
    *,
    direction: str,
    entry_low: float,
    entry_high: float,
    zones: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    want = "bearish" if direction == "SELL" else "bullish"
    return [
        z
        for z in zones
        if z["direction"] == want
        and _zones_near(entry_low, entry_high, z["low"], z["high"], tol=MAX_COUNTER_OVERLAP_PTS)
    ]


def _counter_fvgs(
    *,
    direction: str,
    entry_low: float,
    entry_high: float,
    zones: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    opposite = "bullish" if direction == "SELL" else "bearish"
    return [
        z
        for z in zones
        if z["direction"] == opposite
        and _zones_near(entry_low, entry_high, z["low"], z["high"], tol=MAX_COUNTER_OVERLAP_PTS)
    ]


def adjudicate_level_proposal_claim(
    proposal: LevelProposal,
    ctx: MarketContext,
    *,
    level_reactions: list[dict[str, Any]] | None = None,
) -> ClaimAudit:
    """Decide whether a level proposal's technical thesis may drive execution."""
    claim_id = f"level_claim:{proposal.path_id or 'x'}:{proposal.direction}"
    reactions = _reaction_index(level_reactions)
    rid = str(proposal.reaction_evidence_id or "").strip()
    catalog = technical_claim_fact_catalog(ctx)
    zones = _collect_fvgs(ctx.analyses)
    aligned = _aligned_fvgs(
        direction=proposal.direction,
        entry_low=proposal.entry_low,
        entry_high=proposal.entry_high,
        zones=zones,
    )
    counters = _counter_fvgs(
        direction=proposal.direction,
        entry_low=proposal.entry_low,
        entry_high=proposal.entry_high,
        zones=zones,
    )

    fact_ids: list[str] = []
    for zone in aligned[:3]:
        fact_ids.extend(zone["fact_ids"])
    quality: dict[str, Any] = {
        "aligned_fvg_count": len(aligned),
        "counter_fvg_count": len(counters),
        "best_width_atr_ratio": None,
        "reaction_bound": bool(rid),
        "reaction_resolved": False,
        "structured_fact_bind": False,
        "claimed_fact_count": 0,
        "resolved_fact_count": 0,
        "claimed_relationship_count": 0,
        "verified_relationship_count": 0,
        "entry_fact_bound": False,
    }
    reasons: list[str] = []
    counterevidence: list[dict[str, Any]] = []
    reaction: dict[str, Any] = {}

    if rid:
        if rid not in reactions:
            return ClaimAudit(
                claim_id=claim_id,
                fact_ids=fact_ids,
                eligibility="uncitable",
                quality={**quality, "reaction_resolved": False},
                counterevidence=[{"kind": "missing_reaction", "id": rid}],
                reaction_evidence_id=rid,
                reasons=[f"reaction_evidence_id {rid} not found in technical.level_reactions"],
            )
        reaction = reactions[rid]
        quality["reaction_resolved"] = True
        fact_ids.append(f"reaction:{rid}")
        reasons.append(f"bound reaction {rid}")
    else:
        reasons.append("no reaction_evidence_id — technical bind missing")

    raw_fact_ids = reaction.get("fact_ids") or []
    claimed_fact_ids = (
        sorted(
            {
                str(value).strip()
                for value in raw_fact_ids
                if isinstance(value, (str, int, float)) and str(value).strip()
            }
        )
        if isinstance(raw_fact_ids, list)
        else []
    )
    raw_relationships = reaction.get("relationships") or []
    relationships = (
        [row for row in raw_relationships if isinstance(row, dict)]
        if isinstance(raw_relationships, list)
        else []
    )
    quality["claimed_fact_count"] = len(claimed_fact_ids)
    quality["claimed_relationship_count"] = len(relationships)

    known_ids = {
        str(fid) for row in catalog for fid in (row.get("fact_ids") or [])
    }
    unknown_ids = [fid for fid in claimed_fact_ids if fid not in known_ids]
    claimed_id_set = set(claimed_fact_ids)
    cited_entities = [
        row
        for row in catalog
        if set(row.get("fact_ids") or []).issubset(claimed_id_set)
    ]
    resolved_ids = {
        str(fid) for row in cited_entities for fid in (row.get("fact_ids") or [])
    }
    partial_ids = [fid for fid in claimed_fact_ids if fid in known_ids and fid not in resolved_ids]
    quality["resolved_fact_count"] = len(resolved_ids)
    quality["structured_fact_bind"] = bool(claimed_fact_ids) and not unknown_ids and not partial_ids
    fact_ids.extend(claimed_fact_ids)

    if not claimed_fact_ids:
        counterevidence.append({"kind": "missing_structured_fact_bind", "reaction_id": rid})
        reasons.append("reaction has no structured fact_ids; prose alone cannot authorize execution")
    if unknown_ids:
        counterevidence.append({"kind": "unknown_claim_fact_ids", "fact_ids": unknown_ids})
        reasons.append(f"unknown reaction fact_ids: {unknown_ids}")
    if partial_ids:
        counterevidence.append({"kind": "partial_zone_fact_ids", "fact_ids": partial_ids})
        reasons.append("zone claims must cite both low/high fact IDs")

    entry_bound_keys: set[tuple[str, ...]] = set()
    for entity in cited_entities:
        if not _fact_direction_supports_trade(entity, proposal.direction):
            continue
        if _zones_near(
            proposal.entry_low,
            proposal.entry_high,
            float(entity["low"]),
            float(entity["high"]),
            tol=MAX_CLAIM_NEAR_PTS,
        ):
            entry_bound_keys.add(tuple(sorted(str(fid) for fid in entity["fact_ids"])))
    quality["entry_fact_bound"] = bool(entry_bound_keys)
    if claimed_fact_ids and not entry_bound_keys:
        counterevidence.append(
            {
                "kind": "facts_not_bound_to_entry",
                "entry_low": proposal.entry_low,
                "entry_high": proposal.entry_high,
                "fact_ids": claimed_fact_ids,
            }
        )
        reasons.append("no direction-aligned cited fact overlaps or is near the proposed entry")

    verified_edges: list[tuple[tuple[str, ...], tuple[str, ...]]] = []
    relationship_audit: list[dict[str, Any]] = []
    for relation in relationships:
        relation_type = str(relation.get("type") or "").strip().lower()
        left_ids = relation.get("left_fact_ids") or []
        right_ids = relation.get("right_fact_ids") or []
        left = _fact_entity_for_ids(left_ids, catalog) if isinstance(left_ids, list) else None
        right = _fact_entity_for_ids(right_ids, catalog) if isinstance(right_ids, list) else None
        relation_ids_declared = bool(
            left
            and right
            and set(left.get("fact_ids") or []).issubset(claimed_id_set)
            and set(right.get("fact_ids") or []).issubset(claimed_id_set)
        )
        holds = bool(
            relation_ids_declared
            and left
            and right
            and _relationship_holds(relation_type, left, right)
        )
        audit_row = {
            "kind": "invalid_claimed_relationship",
            "type": relation_type,
            "left_fact_ids": list(left_ids) if isinstance(left_ids, list) else [],
            "right_fact_ids": list(right_ids) if isinstance(right_ids, list) else [],
            "verified": holds,
        }
        relationship_audit.append({key: value for key, value in audit_row.items() if key != "kind"})
        if not holds:
            counterevidence.append(audit_row)
            reasons.append(f"claimed {relation_type or 'unknown'} relationship did not verify")
            continue
        left_key = tuple(sorted(str(fid) for fid in left["fact_ids"]))
        right_key = tuple(sorted(str(fid) for fid in right["fact_ids"]))
        verified_edges.append((left_key, right_key))
        if relation_type == "contradiction":
            counterevidence.append({**audit_row, "kind": "verified_contradiction"})
            reasons.append("structured relationship explicitly identifies contradictory evidence")

    quality["verified_relationship_count"] = len(verified_edges)
    quality["relationship_audit"] = relationship_audit
    if cited_entities and not relationships:
        counterevidence.append({"kind": "missing_fact_relationships", "fact_ids": claimed_fact_ids})
        reasons.append("core execution claims require at least one structured fact relationship")

    # Every extra confluence fact must be connected through verified relations
    # to a fact that is geometrically bound to the proposed entry.
    reachable = set(entry_bound_keys)
    changed = True
    while changed:
        changed = False
        for left_key, right_key in verified_edges:
            if left_key in reachable and right_key not in reachable:
                reachable.add(right_key)
                changed = True
            if right_key in reachable and left_key not in reachable:
                reachable.add(left_key)
                changed = True
    cited_keys = {
        tuple(sorted(str(fid) for fid in row["fact_ids"])) for row in cited_entities
    }
    disconnected = sorted(cited_keys - reachable)
    if disconnected:
        counterevidence.append(
            {
                "kind": "disconnected_claim_facts",
                "fact_ids": [fid for key in disconnected for fid in key],
            }
        )
        reasons.append("cited confluence facts are not connected to the entry-bound fact")

    best_ratio: float | None = None
    for zone in aligned:
        ratio = zone.get("width_atr_ratio")
        if ratio is None:
            continue
        if best_ratio is None or ratio > best_ratio:
            best_ratio = float(ratio)
    quality["best_width_atr_ratio"] = best_ratio

    for zone in counters:
        counterevidence.append(
            {
                "kind": "overlapping_opposite_fvg",
                "timeframe": zone["tf"],
                "direction": zone["direction"],
                "low": zone["low"],
                "high": zone["high"],
                "fact_ids": zone["fact_ids"],
            }
        )
        reasons.append(
            f"counterevidence: {zone['tf']} {zone['direction']} FVG "
            f"{zone['low']:.2f}-{zone['high']:.2f}"
        )

    thin = best_ratio is not None and best_ratio < MIN_FVG_WIDTH_ATR_FOR_CORE
    if thin:
        reasons.append(
            f"aligned FVG width/ATR={best_ratio:.3f} < {MIN_FVG_WIDTH_ATR_FOR_CORE} "
            f"(policy {CLAIM_POLICY_VERSION})"
        )

    structured_invalid = bool(
        unknown_ids
        or partial_ids
        or not claimed_fact_ids
        or not entry_bound_keys
        or disconnected
        or any(c["kind"] == "invalid_claimed_relationship" for c in counterevidence)
        or not relationships
    )
    has_explicit_contradiction = any(
        c["kind"] == "verified_contradiction" for c in counterevidence
    )

    if not aligned and not rid:
        eligibility: CitationEligibility = "observation_only"
        reasons.append("no aligned FVG/OB and no reaction bind — observation only")
    elif counters or has_explicit_contradiction or structured_invalid:
        eligibility = "observation_only"
        reasons.append("claim facts/relationships are conflicted or unverifiable")
    elif thin or not quality["reaction_resolved"]:
        eligibility = "supporting"
        reasons.append(f"eligibility demoted to {eligibility}")
    else:
        eligibility = "core_execution"
        reasons.append("entry-bound facts + verified relationships + no counter FVG")

    return ClaimAudit(
        claim_id=claim_id,
        fact_ids=sorted(set(fact_ids)),
        eligibility=eligibility,
        quality=quality,
        counterevidence=counterevidence,
        reaction_evidence_id=rid,
        reasons=reasons,
    )


def claim_allows_execution_authorization(signal_or_meta: dict[str, Any] | None) -> bool:
    """Rule/engine signals default allow; LLM claims must be core_execution."""
    if not signal_or_meta:
        return True
    elig = signal_or_meta.get("claim_eligibility")
    if elig is None or elig == "":
        # Legacy / rule signals without claim audit.
        return True
    return elig == "core_execution"
