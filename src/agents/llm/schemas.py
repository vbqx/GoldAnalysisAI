"""Parse LLM JSON into pipeline domain types."""

from __future__ import annotations

from typing import Any

from src.config import ANALYST_TEAM_ITEMS_MAX, LLM_MIN_ANALYST_ITEMS, PAYLOAD_EVIDENCE_MAX
from src.core.types import (
    AgentEvidence,
    AnalystReport,
    Bias,
    EvidenceItem,
    LevelProposal,
    ManagerDecision,
    ResearchDebate,
    RiskProfile,
    RiskReview,
    TransactionProposal,
)

_DEFAULT_ITEM_SOURCE = {
    "technical": "tradingview_ict",
    "structure": "tradingview_ict",
    "price_action": "dgt_price_action",
    "lux_panel": "lux_smc_panel",
    "fundamentals": "macro",
    "news": "jin10",
    "sentiment": "tradingview_social",
    "external": "external",
}


def _item_refs(row: dict[str, Any], category: str) -> dict[str, Any]:
    refs = row.get("refs") if isinstance(row.get("refs"), dict) else {}
    if refs.get("source"):
        return refs
    source = row.get("source")
    if source:
        return {**refs, "source": str(source)}
    default = _DEFAULT_ITEM_SOURCE.get(category)
    if default:
        return {**refs, "source": default}
    return refs


def _clamp_strength(v: Any) -> float:
    try:
        f = float(v)
    except (TypeError, ValueError):
        return 0.3
    return max(0.0, min(1.0, f))


def _string_list(value: Any, *, fallback: list[str] | None = None, limit: int = 8) -> list[str]:
    if isinstance(value, list):
        out = [str(v).strip() for v in value if str(v).strip()]
        return out[:limit]
    text = str(value or "").strip()
    if text:
        return [text]
    return fallback or []


def _index_list(value: Any, *, allowed: set[int]) -> list[int]:
    if not isinstance(value, list):
        return []
    out: list[int] = []
    for raw in value:
        try:
            idx = int(raw)
        except (TypeError, ValueError):
            continue
        if idx in allowed and idx not in out:
            out.append(idx)
    return out


def _float_field(row: dict[str, Any], name: str) -> float:
    try:
        return float(row[name])
    except (KeyError, TypeError, ValueError) as exc:
        raise ValueError(f"level proposal missing numeric {name}") from exc


def parse_analyst_report(data: dict[str, Any], *, agent: str) -> AnalystReport:
    bias = str(data.get("bias", "neutral")).lower()
    if bias not in ("bullish", "bearish", "neutral"):
        bias = "neutral"

    items_raw = data.get("items") or []
    items: list[EvidenceItem] = []
    if isinstance(items_raw, list):
        for idx, row in enumerate(items_raw[:ANALYST_TEAM_ITEMS_MAX]):
            if not isinstance(row, dict):
                continue
            summary = str(row.get("summary", "")).strip()
            if not summary:
                continue
            category = str(row.get("category", "external"))
            refs = _item_refs(row, category)
            evidence_id = str(row.get("evidence_id") or "").strip() or f"{agent}:{idx}"
            items.append(
                EvidenceItem(
                    category=category,
                    summary=summary,
                    strength=_clamp_strength(row.get("strength", 0.3)),
                    timeframe=row.get("timeframe"),
                    refs=refs,
                    evidence_id=evidence_id,
                )
            )

    if len(items) < LLM_MIN_ANALYST_ITEMS:
        raise ValueError(
            f"{agent} returned {len(items)} items (min {LLM_MIN_ANALYST_ITEMS})"
        )

    confidence = _clamp_strength(data.get("confidence", 0.5))
    summary = str(data.get("summary", "")).strip()
    if not summary:
        summary = f"LLM {agent}：共 {len(items)} 条证据，偏向 {bias}，置信 {confidence:.0%}"

    return AnalystReport(
        agent=agent,
        bias=bias,  # type: ignore[arg-type]
        items=items,
        confidence=confidence,
        summary=summary,
    )


def parse_agent_evidence(
    data: dict[str, Any],
    *,
    agent: str,
    direction: Bias,
    allowed_evidence_ids: set[str] | None = None,
    evidence_registry: dict[str, EvidenceItem] | None = None,
) -> AgentEvidence:
    from src.agents.analysts.evidence_provenance import (
        blend_research_confidence,
        build_research_provenance_meta,
        parse_research_items,
    )

    items_raw = data.get("items") or []
    model_confidence = _clamp_strength(data.get("confidence", 0.5))
    summary = str(data.get("summary", "")).strip()

    if allowed_evidence_ids is not None:
        if not isinstance(items_raw, list):
            raise ValueError(f"{agent} returned non-list items")
        items, dropped = parse_research_items(
            items_raw,
            agent=agent,
            direction=direction,
            allowed_ids=allowed_evidence_ids,
            registry=evidence_registry or {},
            item_refs_fn=_item_refs,
        )
        meta = build_research_provenance_meta(
            items,
            allowed_ids=allowed_evidence_ids,
            model_confidence=model_confidence,
            dedupe_dropped=dropped,
        )
        confidence = blend_research_confidence(model_confidence, meta)
    else:
        items: list[EvidenceItem] = []
        if isinstance(items_raw, list):
            for idx, row in enumerate(items_raw[:PAYLOAD_EVIDENCE_MAX]):
                if not isinstance(row, dict):
                    continue
                summary_text = str(row.get("summary", "")).strip()
                if not summary_text:
                    continue
                category = str(row.get("category", "structure"))
                refs = _item_refs(row, category)
                evidence_id = str(row.get("evidence_id") or "").strip() or f"{agent}:{idx}"
                items.append(
                    EvidenceItem(
                        category=category,
                        summary=summary_text,
                        strength=_clamp_strength(row.get("strength", 0.3)),
                        timeframe=row.get("timeframe"),
                        refs=refs,
                        evidence_id=evidence_id,
                    )
                )
        meta = build_research_provenance_meta(
            items,
            allowed_ids=set(),
            model_confidence=model_confidence,
        )
        confidence = blend_research_confidence(model_confidence, meta)

    if not summary:
        summary = f"LLM：共 {len(items)} 条证据，置信度 {confidence:.2f}"

    return AgentEvidence(
        agent=agent,
        direction=direction,
        items=items,
        confidence=confidence,
        summary=summary,
        provenance_meta=meta,
    )


def parse_research_debate(
    data: dict[str, Any],
    *,
    bullish: AgentEvidence,
    bearish: AgentEvidence,
) -> ResearchDebate:
    from src.agents.analysts.evidence_provenance import (
        blend_debate_consensus,
        build_debate_provenance_meta,
    )

    bias = str(data.get("consensus_bias", "neutral")).lower()
    if bias not in ("bullish", "bearish", "neutral"):
        bias = "neutral"

    model_strength = _clamp_strength(data.get("consensus_strength", 0.5))
    debate_meta = build_debate_provenance_meta(
        bullish.items,
        bearish.items,
        model_consensus_strength=model_strength,
    )
    strength = blend_debate_consensus(model_strength, debate_meta)
    debate_meta["consensus_strength"] = round(strength, 3)

    notes_raw = data.get("discussion_notes") or []
    notes: list[str] = []
    if isinstance(notes_raw, list):
        notes = [str(n).strip() for n in notes_raw if str(n).strip()]

    dissent = str(data.get("dissent", "")).strip()
    if dissent:
        notes.append(f"分歧：{dissent}")

    if not notes:
        notes = ["LLM 辩论：已生成共识"]

    return ResearchDebate(
        bullish=bullish,
        bearish=bearish,
        consensus_bias=bias,  # type: ignore[arg-type]
        consensus_strength=strength,
        discussion_notes=notes,
        debate_meta=debate_meta,
    )


def parse_level_proposals(data: dict[str, Any]) -> list[LevelProposal]:
    raw_setups = data.get("setups") or data.get("levels") or []
    if not isinstance(raw_setups, list):
        raise ValueError("level proposer returned non-list setups")

    proposals: list[LevelProposal] = []
    for idx, row in enumerate(raw_setups[:5]):
        if not isinstance(row, dict):
            continue
        direction = str(row.get("direction", "")).upper()
        if direction not in ("BUY", "SELL"):
            continue
        path_id = str(row.get("path_id") or row.get("path") or "").strip().upper()
        if path_id not in ("A", "B", "C"):
            raise ValueError(f"level proposal[{idx}] missing or invalid path_id (must be A/B/C)")

        entry_low = _float_field(row, "entry_low")
        entry_high = _float_field(row, "entry_high")
        if entry_low > entry_high:
            entry_low, entry_high = entry_high, entry_low

        tps_raw = row.get("take_profits") or row.get("targets") or []
        if not isinstance(tps_raw, list):
            tps_raw = [tps_raw]
        take_profits: list[float] = []
        for tp in tps_raw[:3]:
            try:
                take_profits.append(float(tp))
            except (TypeError, ValueError):
                continue
        if not take_profits:
            raise ValueError("level proposal missing take_profits")

        reason = str(row.get("reason", "")).strip()
        if not reason:
            reason = "LLM proposed level based on supplied market structure."

        proposals.append(
            LevelProposal(
                direction=direction,  # type: ignore[arg-type]
                entry_low=round(entry_low, 2),
                entry_high=round(entry_high, 2),
                stop_loss=round(_float_field(row, "stop_loss"), 2),
                take_profits=[round(tp, 2) for tp in take_profits],
                setup_type=str(row.get("setup_type", "llm_level")).strip() or "llm_level",
                reason=reason,
                confidence=_clamp_strength(row.get("confidence", 0.5)),
                invalidation=str(row.get("invalidation", "")).strip(),
                path_id=path_id,
            )
        )

    _validate_level_path_contract(proposals)
    return proposals


def _validate_level_path_contract(proposals: list[LevelProposal]) -> None:
    if len(proposals) != 3:
        raise ValueError(f"level proposer must return exactly 3 setups, got {len(proposals)}")
    paths = sorted(p.path_id for p in proposals)
    if paths != ["A", "B", "C"]:
        raise ValueError(f"path_id must be A,B,C exactly once, got {[p.path_id for p in proposals]}")


def parse_transaction_proposal(
    data: dict[str, Any],
    *,
    debate_bias: Bias,
    signal_count: int,
) -> TransactionProposal:
    direction = str(data.get("primary_direction", "wait")).lower()
    if direction not in ("long", "short", "wait"):
        direction = "wait"

    allowed = set(range(max(0, signal_count)))
    indices = _index_list(data.get("signal_indices"), allowed=allowed)
    if direction == "wait":
        indices = []

    rationale = _string_list(
        data.get("rationale") or data.get("reasons"),
        fallback=["LLM trader generated a transaction proposal."],
    )
    return TransactionProposal(
        primary_direction=direction,  # type: ignore[arg-type]
        signal_indices=indices,
        rationale=rationale,
        debate_bias=debate_bias,
    )


def parse_risk_reviews(
    data: dict[str, Any],
    *,
    proposal: TransactionProposal,
    signal_count: int,
) -> list[RiskReview]:
    raw_reviews = data.get("reviews") or data.get("risk_reviews") or []
    if not isinstance(raw_reviews, list):
        raise ValueError("risk stage returned non-list reviews")

    allowed_profiles: tuple[RiskProfile, ...] = ("aggressive", "neutral", "conservative")
    proposal_allowed = {idx for idx in proposal.signal_indices if 0 <= idx < signal_count}
    by_profile: dict[str, RiskReview] = {}
    for row in raw_reviews:
        if not isinstance(row, dict):
            continue
        profile = str(row.get("profile", "")).lower()
        if profile not in allowed_profiles:
            continue
        indices = _index_list(row.get("allowed_signal_indices"), allowed=proposal_allowed)
        scale = _clamp_strength(row.get("position_scale", 0.0))
        approved = bool(row.get("approved")) and bool(indices) and proposal.primary_direction != "wait"
        by_profile[profile] = RiskReview(
            profile=profile,  # type: ignore[arg-type]
            approved=approved,
            allowed_signal_indices=indices,
            position_scale=scale if approved else 0.0,
            notes=_string_list(row.get("notes"), fallback=[f"LLM {profile} 风控审核"]),
        )

    missing = [p for p in allowed_profiles if p not in by_profile]
    if missing:
        raise ValueError(f"risk stage missing profiles: {', '.join(missing)}")
    return [by_profile[p] for p in allowed_profiles]


def parse_manager_decision(
    data: dict[str, Any],
    *,
    proposal: TransactionProposal,
    reviews: list[RiskReview],
) -> ManagerDecision:
    action = str(data.get("action", "wait")).lower()
    if action not in ("execute", "reduce", "wait"):
        action = "wait"

    approved = {
        idx
        for review in reviews
        if review.approved
        for idx in review.allowed_signal_indices
    }
    selected = _index_list(data.get("selected_signal_indices"), allowed=approved)
    if action == "wait" or not selected:
        action = "wait"
        selected = []

    summary = str(data.get("summary", "")).strip()
    if not summary:
        summary = "LLM manager generated the final trade authorization."

    scale = 0.0
    if selected:
        scales = [
            review.position_scale
            for review in reviews
            if review.approved and set(review.allowed_signal_indices).intersection(selected)
        ]
        scale = min(scales) if scales else 0.0

    return ManagerDecision(
        action=action,  # type: ignore[arg-type]
        primary_direction=proposal.primary_direction,
        selected_signal_indices=selected,
        confidence=_clamp_strength(data.get("confidence", 0.0 if action == "wait" else 0.5)),
        summary=summary,
        position_scale=scale if action != "wait" else 0.0,
    )
