"""News data source — Jin10 MCP flash, articles, calendar."""

from __future__ import annotations

from src.core.types import CalendarEvent, EvidenceItem, ExternalFactors, HeadlineItem
from src.data.external_format import headlines_to_strings, sync_external_legacy_fields
from src.data.sources.jin10_feed import Jin10NewsBundle, fetch_jin10_bundle

_PLACEHOLDER_EVENTS = "美盘数据/讲话 → 波动放大（占位）"


def _bundle_to_external(bundle: Jin10NewsBundle) -> ExternalFactors:
    risk = bundle.risk_events
    if risk == "—":
        if bundle.headline_items:
            risk = "黄金相关宏观日历暂不可用（金十 MCP 日历拉取失败，详见 fetch_errors）"
        else:
            risk = _PLACEHOLDER_EVENTS

    ext = ExternalFactors(
        risk_events=risk,
        news_headlines=headlines_to_strings(bundle.headline_items),
        headline_items=list(bundle.headline_items),
        calendar_events=list(bundle.calendar_events),
        sources=list(bundle.sources),
        fetch_errors=list(bundle.errors),
    )
    sync_external_legacy_fields(ext)
    return ext


def external_to_evidence(ext: ExternalFactors, *, is_live: bool) -> list[EvidenceItem]:
    """Build news evidence from pre-fetched ExternalFactors (no re-fetch)."""
    strength = 0.55 if is_live else 0.45
    items: list[EvidenceItem] = []

    for item in ext.headline_items:
        if item.source == "jin10_news":
            items.append(
                EvidenceItem(
                    category="news",
                    summary=item.text,
                    strength=strength,
                    refs={"source": item.source, "time": item.time, "url": item.url},
                )
            )
    for item in ext.headline_items:
        if item.source == "jin10_flash":
            items.append(
                EvidenceItem(
                    category="news",
                    summary=item.text,
                    strength=strength * 0.95,
                    refs={"source": item.source, "time": item.time, "url": item.url},
                )
            )

    for ev in ext.calendar_events:
        items.append(
            EvidenceItem(
                category="news",
                summary=f"日历 · {ev.display()}",
                strength=0.4 + min(ev.importance / 10, 0.35),
                refs={"source": "jin10_calendar", "importance": ev.importance},
            )
        )

    if ext.risk_events and ext.risk_events != "—" and "占位" not in ext.risk_events:
        if not any(ext.risk_events[:24] in i.summary for i in items):
            items.append(
                EvidenceItem(
                    category="news",
                    summary=f"事件风险汇总：{ext.risk_events[:320]}",
                    strength=0.45 if is_live else 0.3,
                    refs={"source": "jin10_calendar"},
                )
            )

    if not items:
        return [
            EvidenceItem(
                category="external",
                summary=_PLACEHOLDER_EVENTS,
                strength=0.3,
                refs={"source": "placeholder"},
            )
        ]
    return items


class NewsDataSource:
    name = "news"

    def fetch_external(self) -> ExternalFactors:
        return _bundle_to_external(fetch_jin10_bundle())

    def fetch_evidence(self) -> list[EvidenceItem]:
        bundle = fetch_jin10_bundle()
        ext = _bundle_to_external(bundle)
        return external_to_evidence(ext, is_live=bundle.is_live)
