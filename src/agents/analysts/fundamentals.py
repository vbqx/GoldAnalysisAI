"""Fundamentals Analyst — DXY / macro drivers for gold."""

from __future__ import annotations

from src.core.types import AnalystReport, Bias, EvidenceItem
from src.data.sources.fundamentals import FundamentalsDataSource

from src.agents.analysts.base import build_report


def _bias_from_dxy(text: str) -> Bias:
    lower = text.lower()
    if any(k in text for k in ("利空黄金", "压制黄金", "偏强")) or "bearish" in lower:
        return "bearish"
    if any(k in text for k in ("利好黄金", "支撑黄金", "偏弱")) or "bullish" in lower:
        return "bullish"
    return "neutral"


def run_fundamentals_analyst(ctx) -> AnalystReport:
    ext = ctx.external if ctx.external.dxy_impact != "—" else FundamentalsDataSource().fetch_external()
    ds = FundamentalsDataSource()
    items = ds.fetch_evidence()
    bias = _bias_from_dxy(ext.dxy_impact)

    live = any(i.refs.get("source") == "tradingview" for i in items)
    if ext.dxy_impact != "—" and not any(i.category == "fundamentals" for i in items):
        items.append(
            EvidenceItem(
                category="fundamentals",
                summary=f"宏观：{ext.dxy_impact}",
                strength=0.55 if bias != "neutral" else 0.35,
                refs={"dxy_impact": ext.dxy_impact, "source": "tradingview" if live else "placeholder"},
            )
        )

    summary = f"基本面：美元指数 {ext.dxy_impact}"
    if not live and "占位" in ext.dxy_impact:
        summary = f"基本面：{ext.dxy_impact}"
    return build_report(agent="fundamentals_analyst", items=items, bias=bias, summary=summary)
