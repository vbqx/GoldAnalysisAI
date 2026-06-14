"""Parse LLM JSON into pipeline domain types."""

from __future__ import annotations

from typing import Any

from src.core.types import AgentEvidence, AnalystReport, Bias, EvidenceItem, ResearchDebate


def _clamp_strength(v: Any) -> float:
    try:
        f = float(v)
    except (TypeError, ValueError):
        return 0.3
    return max(0.0, min(1.0, f))


def parse_analyst_report(data: dict[str, Any], *, agent: str) -> AnalystReport:
    bias = str(data.get("bias", "neutral")).lower()
    if bias not in ("bullish", "bearish", "neutral"):
        bias = "neutral"

    items_raw = data.get("items") or []
    items: list[EvidenceItem] = []
    if isinstance(items_raw, list):
        for row in items_raw[:12]:
            if not isinstance(row, dict):
                continue
            summary = str(row.get("summary", "")).strip()
            if not summary:
                continue
            items.append(
                EvidenceItem(
                    category=str(row.get("category", "external")),
                    summary=summary,
                    strength=_clamp_strength(row.get("strength", 0.3)),
                    timeframe=row.get("timeframe"),
                )
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
        for row in items_raw[:15]:
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
