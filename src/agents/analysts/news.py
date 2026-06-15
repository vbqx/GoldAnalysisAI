"""News Analyst — macro headlines and event risk."""

from __future__ import annotations

from src.agents.analysts.news_bias import infer_news_bias
from src.core.types import AnalystReport, EvidenceItem, MarketContext
from src.data.sources.news import external_to_evidence

from src.agents.analysts.base import build_report


def run_news_analyst(ctx: MarketContext) -> AnalystReport:
    ext = ctx.external
    is_live = any(
        s in (ext.sources or []) for s in ("jin10_flash", "jin10_news", "jin10_calendar")
    )
    items = external_to_evidence(ext, is_live=is_live)

    bias = infer_news_bias(ext.headline_items, ext.calendar_events, risk_text=ext.risk_events)

    if ext.news_headlines:
        summary = (
            f"新闻：{len(ext.headline_items)} 条"
            f"（快讯 {sum(1 for h in ext.headline_items if h.source == 'jin10_flash')} · "
            f"资讯 {sum(1 for h in ext.headline_items if h.source == 'jin10_news')}）"
            f" · 日历 {len(ext.calendar_events)} · bias {bias}"
        )
    elif ext.risk_events != "—":
        summary = f"新闻：{ext.risk_events[:80]}"
    else:
        summary = "新闻：暂无头条数据"

    return build_report(agent="news_analyst", items=items, bias=bias, summary=summary)
