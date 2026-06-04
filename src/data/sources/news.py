"""News data source — placeholder until real API wired."""

from __future__ import annotations

from src.core.types import EvidenceItem, ExternalFactors


class NewsDataSource:
    name = "news"

    def fetch_external(self) -> ExternalFactors:
        # TODO: FinHub / RSS / calendar API
        return ExternalFactors(
            risk_events="美盘数据/讲话 → 波动放大",
            news_headlines=[],
        )

    def fetch_evidence(self) -> list[EvidenceItem]:
        ext = self.fetch_external()
        if not ext.news_headlines:
            return [
                EvidenceItem(
                    category="external",
                    summary=ext.risk_events,
                    strength=0.3,
                    refs={"source": "placeholder"},
                )
            ]
        return [
            EvidenceItem(
                category="external",
                summary=h,
                strength=0.5,
                refs={"source": "news"},
            )
            for h in ext.news_headlines[:5]
        ]
