"""Parse LLM JSON into pipeline domain types."""

from __future__ import annotations

from typing import Any

from src.config import ANALYST_TEAM_ITEMS_MAX, LLM_MIN_ANALYST_ITEMS, PAYLOAD_EVIDENCE_MAX
from src.core.types import AgentEvidence, AnalystReport, Bias, EvidenceItem, LevelProposal, ResearchDebate

_DEFAULT_ITEM_SOURCE = {
    "technical": "tradingview_ict",
    "structure": "tradingview_ict",
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
        for row in items_raw[:ANALYST_TEAM_ITEMS_MAX]:
            if not isinstance(row, dict):
                continue
            summary = str(row.get("summary", "")).strip()
            if not summary:
                continue
            category = str(row.get("category", "external"))
            refs = _item_refs(row, category)
            items.append(
                EvidenceItem(
                    category=category,
                    summary=summary,
                    strength=_clamp_strength(row.get("strength", 0.3)),
                    timeframe=row.get("timeframe"),
                    refs=refs,
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


def parse_agent_evidence(data: dict[str, Any], *, agent: str, direction: Bias) -> AgentEvidence:
    items_raw = data.get("items") or []
    items: list[EvidenceItem] = []
    if isinstance(items_raw, list):
        for row in items_raw[:PAYLOAD_EVIDENCE_MAX]:
            if not isinstance(row, dict):
                continue
            summary = str(row.get("summary", "")).strip()
            if not summary:
                continue
            items.append(
                EvidenceItem(
                    category=str(row.get("category", "structure")),
                    summary=summary,
                    strength=_clamp_strength(row.get("strength", 0.3)),
                    timeframe=row.get("timeframe"),
                )
            )

    confidence = _clamp_strength(data.get("confidence", 0.5))
    summary = str(data.get("summary", "")).strip()
    if not summary:
        summary = f"LLM：共 {len(items)} 条证据，置信度 {confidence:.2f}"

    return AgentEvidence(
        agent=agent,
        direction=direction,
        items=items,
        confidence=confidence,
        summary=summary,
    )


def parse_research_debate(
    data: dict[str, Any],
    *,
    bullish: AgentEvidence,
    bearish: AgentEvidence,
) -> ResearchDebate:
    bias = str(data.get("consensus_bias", "neutral")).lower()
    if bias not in ("bullish", "bearish", "neutral"):
        bias = "neutral"

    strength = _clamp_strength(data.get("consensus_strength", 0.5))
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
    )


def parse_level_proposals(data: dict[str, Any]) -> list[LevelProposal]:
    raw_setups = data.get("setups") or data.get("levels") or []
    if not isinstance(raw_setups, list):
        raise ValueError("level proposer returned non-list setups")

    proposals: list[LevelProposal] = []
    for row in raw_setups[:5]:
        if not isinstance(row, dict):
            continue
        direction = str(row.get("direction", "")).upper()
        if direction not in ("BUY", "SELL"):
            continue

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
            )
        )

    return proposals
