"""News data source — Finnhub + Google News RSS."""

from __future__ import annotations

from src.core.types import EvidenceItem, ExternalFactors
from src.data.sources.news_feed import fetch_news_bundle


class NewsDataSource:
    name = "news"

    def fetch_external(self) -> ExternalFactors:
        headlines, risk_events, refs = fetch_news_bundle()
        sources = list(refs.get("sources") or [])
        return ExternalFactors(
            risk_events=risk_events,
            news_headlines=headlines,
            sources=sources,
        )

    def fetch_evidence(self) -> list[EvidenceItem]:
        headlines, risk_events, refs = fetch_news_bundle()
        items: list[EvidenceItem] = []
        is_live = refs.get("source") in ("live", "partial")

        for headline in headlines[:8]:
            items.append(
                EvidenceItem(
                    category="external",
                    summary=headline,
                    strength=0.55 if is_live else 0.45,
                    refs={"source": "news", **refs},
                )
            )

        if risk_events and risk_events != "—":
            items.append(
                EvidenceItem(
                    category="external",
                    summary=risk_events if risk_events.startswith("近") else f"事件风险：{risk_events}",
                    strength=0.45 if is_live else 0.3,
                    refs={"source": "te_calendar_scrape" if "te_calendar" in str(refs.get("sources")) else refs.get("source", "news"), **refs},
                )
            )

        if not items:
            return [
                EvidenceItem(
                    category="external",
                    summary="美盘数据/讲话 → 波动放大（占位）",
                    strength=0.3,
                    refs={"source": "placeholder"},
                )
            ]
        return items
