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
    ext = FundamentalsDataSource().fetch_external()
    items = FundamentalsDataSource().fetch_evidence()
    bias = _bias_from_dxy(ext.dxy_impact)

    if ext.dxy_impact != "—":
        items.append(
            EvidenceItem(
                category="fundamentals",
                summary=f"宏观：{ext.dxy_impact}",
                strength=0.55 if bias != "neutral" else 0.35,
                refs={"dxy_impact": ext.dxy_impact, "placeholder": True},
            )
        )

    summary = f"基本面：美元指数影响 {ext.dxy_impact}"
    if not items:
        summary = "基本面：暂无实时宏观数据（占位）"
    return build_report(agent="fundamentals_analyst", items=items, bias=bias, summary=summary)
