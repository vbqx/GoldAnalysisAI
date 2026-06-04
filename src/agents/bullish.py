"""Bullish researcher — extracts buy-side evidence from structure + data."""

from __future__ import annotations

from src.analysis.ict_pa import TimeframeAnalysis
from src.core.types import AgentEvidence, EvidenceItem, MarketContext

_TF_WEIGHT = {"4h": 0.35, "1h": 0.30, "15m": 0.20, "5m": 0.15}


def _structure_items(analyses: dict[str, TimeframeAnalysis]) -> list[EvidenceItem]:
    items: list[EvidenceItem] = []
    for tf, weight in _TF_WEIGHT.items():
        a = analyses[tf]
        if a.trend == "bullish":
            items.append(
                EvidenceItem(
                    category="structure",
                    summary=f"{tf} 趋势偏多",
                    strength=weight,
                    timeframe=tf,
                    refs={"trend": a.trend},
                )
            )
        for ev in a.events:
            if ev.direction == "bullish":
                items.append(
                    EvidenceItem(
                        category="structure",
                        summary=f"{tf} {ev.kind} 看多 @ {ev.price:.2f}",
                        strength=weight * 0.9,
                        timeframe=tf,
                        refs={"kind": ev.kind, "price": ev.price},
                    )
                )
        if a.premium_discount == "discount":
            items.append(
                EvidenceItem(
                    category="structure",
                    summary=f"{tf} 折价区 — 潜在做多区域",
                    strength=weight * 0.7,
                    timeframe=tf,
                )
            )
        for ob in a.order_blocks:
            if ob.direction == "bullish":
                items.append(
                    EvidenceItem(
                        category="structure",
                        summary=f"{tf} 看涨订单块 {ob.low:.0f}-{ob.high:.0f}",
                        strength=weight * 0.75,
                        timeframe=tf,
                    )
                )
        for lz in a.liquidity:
            if "Low" in lz.label or "买方" in lz.label:
                items.append(
                    EvidenceItem(
                        category="liquidity",
                        summary=f"{tf} {lz.label}: {lz.price:.2f}",
                        strength=weight * 0.6,
                        timeframe=tf,
                    )
                )
    return items


def run_bullish_researcher(ctx: MarketContext) -> AgentEvidence:
    items = _structure_items(ctx.analyses)
    score = sum(i.strength for i in items) / max(len(items), 1)
    summary = f"共 {len(items)} 条看多证据，加权强度 {score:.2f}" if items else "暂无明确看多结构证据"
    return AgentEvidence(
        agent="bullish_researcher",
        direction="bullish",
        items=items,
        confidence=min(score, 1.0),
        summary=summary,
    )
