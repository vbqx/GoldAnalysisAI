"""News Analyst — macro headlines and event risk."""

from __future__ import annotations

from src.agents.analysts.news_bias import infer_news_bias
from src.core.types import AnalystReport, EvidenceItem, MarketContext
from src.data.sources.news import external_to_evidence

from src.agents.analysts.base import build_report


def _news_context_evidence(ctx: MarketContext, *, is_live: bool) -> list[EvidenceItem]:
    ext = ctx.external
    items: list[EvidenceItem] = []
    flash = sum(1 for h in ext.headline_items if h.source == "jin10_flash")
    articles = sum(1 for h in ext.headline_items if h.source == "jin10_news")

    if ext.headline_items or ext.calendar_events:
        items.append(
            EvidenceItem(
                category="news",
                summary=(
                    f"新闻输入密度：快讯 {flash} · 资讯 {articles} · "
                    f"日历 {len(ext.calendar_events)}"
                ),
                strength=0.4 + min((flash + articles + len(ext.calendar_events)) / 40, 0.3),
                refs={
                    "source": "input_density",
                    "flash": flash,
                    "articles": articles,
                    "calendar_events": len(ext.calendar_events),
                    "is_live": is_live,
                },
            )
        )

    for topic in ctx.derived.get("news_topics", [])[:3]:
        samples = topic.get("samples") or []
        sample = str(samples[0])[:100] if samples else ""
        items.append(
            EvidenceItem(
                category="news",
                summary=f"新闻主题：{topic.get('topic')} · {topic.get('count')} 条" + (f" · {sample}" if sample else ""),
                strength=0.5 + min(int(topic.get("count") or 0) * 0.05, 0.2),
                refs={"source": "news_topics", "topic": topic.get("topic"), "count": topic.get("count")},
            )
        )

    jin10_errors = [err for err in ext.fetch_errors if "jin10" in err.lower()]
    if jin10_errors:
        items.append(
            EvidenceItem(
                category="news",
                summary=f"新闻数据源告警：{jin10_errors[0][:160]}",
                strength=0.2,
                refs={"source": "fetch_errors", "errors": jin10_errors[:3]},
            )
        )
    elif ext.sources:
        live_sources = [
            s for s in ext.sources if s in ("jin10_flash", "jin10_news", "jin10_calendar")
        ]
        if live_sources:
            items.append(
                EvidenceItem(
                    category="news",
                    summary=f"新闻来源覆盖：{' + '.join(live_sources)}",
                    strength=0.35,
                    refs={"source": "input_density", "live_sources": live_sources},
                )
            )

    return items


def run_news_analyst(ctx: MarketContext) -> AnalystReport:
    ext = ctx.external
    is_live = any(
        s in (ext.sources or []) for s in ("jin10_flash", "jin10_news", "jin10_calendar")
    )
    items = external_to_evidence(ext, is_live=is_live) + _news_context_evidence(ctx, is_live=is_live)

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
