"""Citation eligibility for technical claims used as execution rationale.

Policy version ``claim-v1`` (Issue #36): a geometric FVG/OB is not automatically
eligible as *core execution* evidence. Overlapping opposite structure, thin
gaps vs ATR, or unbound reaction IDs demote the claim to supporting /
observation / uncitable.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Literal

from src.analysis.ict_pa import FairValueGap, TimeframeAnalysis
from src.core.types import LevelProposal, MarketContext

CLAIM_POLICY_VERSION = "claim-v1"

CitationEligibility = Literal[
    "core_execution",
    "supporting",
    "observation_only",
    "uncitable",
]

# Calibrated floors for claim-v1 (documented; can be replaced by backtest table later).
MIN_FVG_WIDTH_ATR_FOR_CORE = 0.35
MAX_COUNTER_OVERLAP_PTS = 0.5  # treat as overlapping if interval distance <= this


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
    for z in aligned[:3]:
        fact_ids.extend(z["fact_ids"])
    quality: dict[str, Any] = {
        "aligned_fvg_count": len(aligned),
        "counter_fvg_count": len(counters),
        "best_width_atr_ratio": None,
        "reaction_bound": bool(rid),
        "reaction_resolved": False,
    }
    reasons: list[str] = []
    counterevidence: list[dict[str, Any]] = []

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
        quality["reaction_resolved"] = True
        fact_ids.append(f"reaction:{rid}")
        reasons.append(f"bound reaction {rid}")
    else:
        reasons.append("no reaction_evidence_id — technical bind missing")

    best_ratio: float | None = None
    for z in aligned:
        ratio = z.get("width_atr_ratio")
        if ratio is None:
            continue
        if best_ratio is None or ratio > best_ratio:
            best_ratio = float(ratio)
    quality["best_width_atr_ratio"] = best_ratio

    for z in counters:
        counterevidence.append(
            {
                "kind": "overlapping_opposite_fvg",
                "timeframe": z["tf"],
                "direction": z["direction"],
                "low": z["low"],
                "high": z["high"],
                "fact_ids": z["fact_ids"],
            }
        )
        reasons.append(
            f"counterevidence: {z['tf']} {z['direction']} FVG {z['low']:.2f}-{z['high']:.2f}"
        )

    thin = best_ratio is not None and best_ratio < MIN_FVG_WIDTH_ATR_FOR_CORE
    if thin:
        reasons.append(
            f"aligned FVG width/ATR={best_ratio:.3f} < {MIN_FVG_WIDTH_ATR_FOR_CORE} "
            f"(policy {CLAIM_POLICY_VERSION})"
        )

    if not aligned and not rid:
        eligibility: CitationEligibility = "observation_only"
        reasons.append("no aligned FVG/OB and no reaction bind — observation only")
    elif counters or thin or not quality["reaction_resolved"]:
        # Conflicted / thin / unbound → cannot be core execution thesis.
        if counters and thin:
            eligibility = "observation_only"
        elif counters:
            eligibility = "observation_only"
        elif thin:
            eligibility = "supporting"
        else:
            eligibility = "supporting"
        reasons.append(f"eligibility demoted to {eligibility}")
    else:
        eligibility = "core_execution"
        reasons.append("aligned structure + resolved reaction + no counter FVG")

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
