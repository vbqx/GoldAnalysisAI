"""Bearish researcher — structure + Analyst Team evidence for sell side."""

from __future__ import annotations

from src.agents.analysts.base import items_for_direction
from src.analysis.ict_pa import TimeframeAnalysis
from src.core.types import AgentEvidence, AnalystTeam, EvidenceItem, MarketContext

_TF_WEIGHT = {"4h": 0.35, "1h": 0.30, "15m": 0.20, "5m": 0.15}


def _structure_items(analyses: dict[str, TimeframeAnalysis]) -> list[EvidenceItem]:
    items: list[EvidenceItem] = []
    for tf, weight in _TF_WEIGHT.items():
        a = analyses[tf]
        if a.trend == "bearish":
            items.append(
                EvidenceItem(
                    category="structure",
                    summary=f"{tf} 趋势偏空",
                    strength=weight,
                    timeframe=tf,
                    refs={"trend": a.trend},
                )
            )
        for ev in a.events:
            if ev.direction == "bearish":
                items.append(
                    EvidenceItem(
                        category="structure",
                        summary=f"{tf} {ev.kind} 看空 @ {ev.price:.2f}",
                        strength=weight * 0.9,
                        timeframe=tf,
                        refs={"kind": ev.kind, "price": ev.price},
                    )
                )
        if a.premium_discount == "premium":
            items.append(
                EvidenceItem(
                    category="structure",
                    summary=f"{tf} 溢价区 — 潜在做空区域",
                    strength=weight * 0.7,
                    timeframe=tf,
                )
            )
        for fvg in a.active_fvgs:
            if fvg.direction == "bearish":
                items.append(
                    EvidenceItem(
                        category="structure",
                        summary=f"{tf} 看跌 FVG {fvg.low:.0f}-{fvg.high:.0f}",
                        strength=weight * 0.8,
                        timeframe=tf,
                    )
                )
        for ob in a.order_blocks:
            if ob.direction == "bearish":
                items.append(
                    EvidenceItem(
                        category="structure",
                        summary=f"{tf} 看跌订单块 {ob.low:.0f}-{ob.high:.0f}",
                        strength=weight * 0.75,
                        timeframe=tf,
                    )
                )
        for lz in a.liquidity:
            if lz.kind != "swing_high":
                continue
                items.append(
                    EvidenceItem(
                        category="liquidity",
                        summary=f"{tf} {lz.label}: {lz.price:.2f}",
                        strength=weight * 0.6,
                        timeframe=tf,
                    )
                )
    return items


def run_bearish_researcher(ctx: MarketContext, team: AnalystTeam | None = None) -> AgentEvidence:
    items = _structure_items(ctx.analyses)
    if team:
        items = items + items_for_direction(team.reports, "bearish")
    score = sum(i.strength for i in items) / max(len(items), 1)
    summary = f"共 {len(items)} 条看空证据，加权强度 {score:.2f}" if items else "暂无明确看空结构证据"
    return AgentEvidence(
        agent="bearish_researcher",
        direction="bearish",
        items=items,
        confidence=min(score, 1.0),
        summary=summary,
    )
