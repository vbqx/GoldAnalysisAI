"""Aggregate all data sources into a unified context slice."""

from __future__ import annotations

import pandas as pd

from src.analysis.ict_pa import TimeframeAnalysis
from src.core.types import EvidenceItem, ExternalFactors, MarketContext
from src.data.fetcher import daily_metrics, get_active_source
from src.data.sources import (
    FundamentalsDataSource,
    MarketDataSource,
    NewsDataSource,
    SocialDataSource,
)
from src.log import get_logger

log = get_logger(__name__)


def merge_external(*parts: ExternalFactors) -> ExternalFactors:
    merged = ExternalFactors()
    for p in parts:
        if p.dxy_impact != "—":
            merged.dxy_impact = p.dxy_impact
        if p.risk_events != "—":
            merged.risk_events = p.risk_events
        merged.news_headlines.extend(p.news_headlines)
        if p.social_sentiment != "—":
            merged.social_sentiment = p.social_sentiment
    return merged


def collect_evidence(enriched: dict[str, pd.DataFrame]) -> list[EvidenceItem]:
    items: list[EvidenceItem] = []
    items.extend(MarketDataSource(enriched).fetch_evidence())
    items.extend(NewsDataSource().fetch_evidence())
    items.extend(SocialDataSource().fetch_evidence())
    items.extend(FundamentalsDataSource().fetch_evidence())
    return items


def build_market_context(
    enriched: dict[str, pd.DataFrame],
    analyses: dict[str, TimeframeAnalysis],
) -> MarketContext:
    metrics = daily_metrics(enriched["1d"])
    external = merge_external(
        NewsDataSource().fetch_external(),
        FundamentalsDataSource().fetch_external(),
    )
    ctx = MarketContext(
        enriched=enriched,
        analyses=analyses,
        metrics=metrics,
        price=float(metrics["current_price"]),
        external=external,
        source_label=get_active_source(),
    )
    log.debug(
        "external factors dxy=%r risk=%r evidence_items=%d",
        external.dxy_impact,
        external.risk_events,
        len(collect_evidence(enriched)),
    )
    return ctx
