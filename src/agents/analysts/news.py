"""News Analyst — macro headlines and event risk."""

from __future__ import annotations

from src.core.types import AnalystReport, Bias, EvidenceItem
from src.data.sources.news import NewsDataSource

from src.agents.analysts.base import build_report


def run_news_analyst(ctx) -> AnalystReport:
    ext = NewsDataSource().fetch_external()
    items = NewsDataSource().fetch_evidence()

    for headline in ext.news_headlines[:5]:
        items.append(
            EvidenceItem(
                category="news",
                summary=headline,
                strength=0.5,
                refs={"source": "news"},
            )
        )

    # Event risk is direction-agnostic but raises volatility — neutral bias
    bias: Bias = "neutral"
    if ext.risk_events and ext.risk_events != "—":
        items.append(
            EvidenceItem(
                category="news",
                summary=f"事件风险：{ext.risk_events}",
                strength=0.4,
                refs={"placeholder": not ext.news_headlines},
            )
        )

    if ext.news_headlines:
        summary = f"新闻：{len(ext.news_headlines)} 条头条，事件风险需结合盘面"
    elif ext.risk_events != "—":
        summary = f"新闻：{ext.risk_events}（占位规则）"
    else:
        summary = "新闻：暂无头条数据（占位）"

    return build_report(agent="news_analyst", items=items, bias=bias, summary=summary)
