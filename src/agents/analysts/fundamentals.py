"""Fundamentals Analyst — DXY / US10Y macro drivers for gold."""

from __future__ import annotations

from src.core.types import AnalystReport, Bias, MarketContext
from src.data.sources.fundamentals import external_macro_evidence

from src.agents.analysts.base import build_report


def _bias_from_quotes(ctx: MarketContext) -> Bias:
    votes = {"bullish": 0, "bearish": 0, "neutral": 0}
    for q in ctx.external.macro_quotes:
        votes[q.bias] = votes.get(q.bias, 0) + 1
    if votes["bullish"] > votes["bearish"]:
        return "bullish"
    if votes["bearish"] > votes["bullish"]:
        return "bearish"
    text = ctx.external.dxy_impact
    if any(k in text for k in ("利空黄金", "偏强")):
        return "bearish"
    if any(k in text for k in ("利好黄金", "偏弱")):
        return "bullish"
    return "neutral"


def run_fundamentals_analyst(ctx: MarketContext) -> AnalystReport:
    ext = ctx.external
    items = external_macro_evidence(ext)
    bias = _bias_from_quotes(ctx)

    live = any(i.refs.get("source") == "tradingview" for i in items)
    names = [q.name for q in ext.macro_quotes] or ["DXY"]
    summary = f"基本面：{' + '.join(names)} · {ext.dxy_impact[:60]}"
    if not live and "占位" in ext.dxy_impact:
        summary = f"基本面：{ext.dxy_impact}"

    return build_report(agent="fundamentals_analyst", items=items, bias=bias, summary=summary)
