"""Technical Analyst — indicators + ICT structure summary."""

from __future__ import annotations

from src.agents.analysts.structure_zones import ict_zone_evidence
from src.analysis.ict_pa import TimeframeAnalysis, sentiment_score
from src.core.types import AnalystReport, Bias, EvidenceItem, MarketContext
from src.data.sources.market import MarketDataSource
from src.indicators.technical import ema_relation

from src.agents.analysts.base import build_report

_TF_WEIGHT = {"4h": 0.35, "1h": 0.30, "15m": 0.20, "5m": 0.15}


def _structure_bias(analyses: dict[str, TimeframeAnalysis]) -> tuple[Bias, list[EvidenceItem]]:
    items: list[EvidenceItem] = []
    bull = bear = 0.0
    for tf, weight in _TF_WEIGHT.items():
        a = analyses.get(tf)
        if not a:
            continue
        if a.trend == "bullish":
            bull += weight
            items.append(
                EvidenceItem(
                    category="technical",
                    summary=f"{tf} 结构趋势偏多",
                    strength=weight,
                    timeframe=tf,
                )
            )
        elif a.trend == "bearish":
            bear += weight
            items.append(
                EvidenceItem(
                    category="technical",
                    summary=f"{tf} 结构趋势偏空",
                    strength=weight,
                    timeframe=tf,
                )
            )
        if a.bos:
            items.append(
                EvidenceItem(
                    category="technical",
                    summary=f"{tf} {a.bos}",
                    strength=weight * 0.85,
                    timeframe=tf,
                )
            )
        if a.choch:
            items.append(
                EvidenceItem(
                    category="technical",
                    summary=f"{tf} {a.choch}",
                    strength=weight * 0.9,
                    timeframe=tf,
                )
            )

    if bull > bear + 0.1:
        return "bullish", items
    if bear > bull + 0.1:
        return "bearish", items
    return "neutral", items


def run_technical_analyst(ctx: MarketContext) -> AnalystReport:
    market_items = MarketDataSource(ctx.enriched).fetch_evidence()
    struct_bias, struct_items = _structure_bias(ctx.analyses)

    ema_items: list[EvidenceItem] = []
    last = ctx.enriched["5m"].iloc[-1]
    relations = ema_relation(ctx.price, last)
    above = sum(1 for v in relations.values() if v == "上方")
    below = sum(1 for v in relations.values() if v == "下方")
    for col, rel in relations.items():
        if rel == "N/A":
            continue
        ema_items.append(
            EvidenceItem(
                category="technical",
                summary=f"价格位于 {col} {rel}",
                strength=0.45,
                timeframe="5m",
                refs={col: rel},
            )
        )

    ema_bias: Bias = "neutral"
    if above > below:
        ema_bias = "bullish"
    elif below > above:
        ema_bias = "bearish"

    vote = sentiment_score(ctx.analyses)
    zone_items = ict_zone_evidence(ctx)
    items = market_items + struct_items + ema_items + zone_items

    biases = [struct_bias, ema_bias]
    if vote["bullish"] > vote["bearish"] + 8:
        biases.append("bullish")
    elif vote["bearish"] > vote["bullish"] + 8:
        biases.append("bearish")
    else:
        biases.append("neutral")

    bull_votes = biases.count("bullish")
    bear_votes = biases.count("bearish")
    if bull_votes > bear_votes:
        bias: Bias = "bullish"
    elif bear_votes > bull_votes:
        bias = "bearish"
    else:
        bias = "neutral"

    summary = (
        f"技术：结构 {struct_bias} / EMA {ema_bias} / 多周期投票 "
        f"多 {vote['bullish']:.0f}% 空 {vote['bearish']:.0f}%"
    )
    return build_report(agent="technical_analyst", items=items, bias=bias, summary=summary)
