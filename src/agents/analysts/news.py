"""News Analyst — macro headlines and event risk."""

from __future__ import annotations

from src.core.types import AnalystReport, Bias, EvidenceItem
from src.data.sources.news import NewsDataSource

from src.agents.analysts.base import build_report


def run_news_analyst(ctx) -> AnalystReport:
    ext = ctx.external
    items = NewsDataSource().fetch_evidence()

    for headline in ext.news_headlines[:5]:
        if not any(headline in i.summary for i in items):
            items.append(
                EvidenceItem(
                    category="news",
                    summary=headline,
                    strength=0.5,
                    refs={"source": "news"},
                )
            )

    bias: Bias = "neutral"
    if ext.risk_events and ext.risk_events != "—":
        if not any(ext.risk_events[:20] in i.summary for i in items):
            live = "finnhub" in ext.risk_events or ext.risk_events.startswith("近")
            items.append(
                EvidenceItem(
                    category="news",
                    summary=f"事件风险：{ext.risk_events}",
                    strength=0.45 if live else 0.35,
                    refs={"source": "calendar" if live else "placeholder"},
                )
            )

    if ext.news_headlines:
        summary = f"新闻：{len(ext.news_headlines)} 条头条 · {ext.risk_events[:40]}"
    elif ext.risk_events != "—":
        summary = f"新闻：{ext.risk_events[:80]}"
    else:
        summary = "新闻：暂无头条数据"

    return build_report(agent="news_analyst", items=items, bias=bias, summary=summary)
