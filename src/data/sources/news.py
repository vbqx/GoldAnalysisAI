"""News data source — Jin10 MCP flash, articles, calendar."""

from __future__ import annotations

from src.core.types import EvidenceItem, ExternalFactors
from src.data.sources.jin10_feed import Jin10NewsBundle, fetch_jin10_bundle

_PLACEHOLDER_EVENTS = "美盘数据/讲话 → 波动放大（占位）"


def _bundle_to_external(bundle: Jin10NewsBundle) -> ExternalFactors:
    risk = bundle.risk_events
    if risk == "—":
        if bundle.headlines:
            risk = "黄金相关宏观日历暂不可用（金十 MCP 日历拉取失败，详见 fetch_errors）"
        else:
            risk = _PLACEHOLDER_EVENTS

    return ExternalFactors(
        risk_events=risk,
        news_headlines=bundle.headlines,
        sources=list(bundle.sources),
        fetch_errors=list(bundle.errors),
    )


class NewsDataSource:
    name = "news"

    def fetch_external(self) -> ExternalFactors:
        return _bundle_to_external(fetch_jin10_bundle())

    def fetch_evidence(self) -> list[EvidenceItem]:
        bundle = fetch_jin10_bundle()
        items: list[EvidenceItem] = []
        is_live = bundle.is_live
        strength = 0.55 if is_live else 0.45

        for headline in bundle.articles[:8]:
            items.append(
                EvidenceItem(
                    category="external",
                    summary=headline,
                    strength=strength,
                    refs={"source": "jin10_news"},
                )
            )

        for headline in bundle.flash[:8]:
            items.append(
                EvidenceItem(
                    category="external",
                    summary=headline,
                    strength=strength,
                    refs={"source": "jin10_flash"},
                )
            )

        risk = bundle.risk_events
        if risk and risk != "—" and "占位" not in risk:
            items.append(
                EvidenceItem(
                    category="external",
                    summary=f"事件风险：{risk}",
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
