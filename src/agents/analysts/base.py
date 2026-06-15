"""Shared helpers for the Analyst Team."""

from __future__ import annotations

from src.config import PAYLOAD_EVIDENCE_MAX
from src.core.types import AnalystReport, Bias, EvidenceItem


def confidence_from_items(items: list[EvidenceItem]) -> float:
    if not items:
        return 0.0
    return min(sum(i.strength for i in items) / len(items), 1.0)


def build_report(
    *,
    agent: str,
    items: list[EvidenceItem],
    bias: Bias,
    summary: str | None = None,
) -> AnalystReport:
    conf = confidence_from_items(items)
    if summary is None:
        if not items:
            summary = "暂无可用数据"
        else:
            summary = f"共 {len(items)} 条证据，偏向 {bias}，置信 {conf:.0%}"
    return AnalystReport(
        agent=agent,
        bias=bias,
        items=items,
        confidence=conf,
        summary=summary,
    )


def items_for_direction(team_reports: list[AnalystReport], direction: Bias) -> list[EvidenceItem]:
    """Pull evidence from specialist reports aligned with a researcher direction."""
    merged: list[EvidenceItem] = []
    for report in team_reports:
        if report.bias != direction or not report.items:
            continue
        label = report.agent.replace("_", " ")
        for item in report.items:
            merged.append(
                EvidenceItem(
                    category=f"analyst_{report.agent}",
                    summary=f"[{label}] {item.summary}",
                    strength=min(item.strength * max(report.confidence, 0.35), 1.0),
                    timeframe=item.timeframe,
                    refs={**item.refs, "analyst": report.agent},
                )
            )
    merged.sort(key=lambda i: i.strength, reverse=True)
    return merged[:PAYLOAD_EVIDENCE_MAX]
