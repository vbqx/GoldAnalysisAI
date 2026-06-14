"""Aggregate all data sources into a unified context slice."""

from __future__ import annotations

import pandas as pd

from src.analysis.ict_pa import TimeframeAnalysis
from src.core.progress import get_progress
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
        merged.social_posts.extend(p.social_posts)
        merged.fetch_errors.extend(p.fetch_errors)
        for src in p.sources:
            if src and src not in merged.sources:
                merged.sources.append(src)
    return merged


def collect_evidence(enriched: dict[str, pd.DataFrame]) -> list[EvidenceItem]:
    items: list[EvidenceItem] = []
    items.extend(MarketDataSource(enriched).fetch_evidence())
    items.extend(NewsDataSource().fetch_evidence())
    items.extend(SocialDataSource().fetch_evidence())
    items.extend(FundamentalsDataSource().fetch_evidence())
    return items


def assemble_market_context(
    enriched: dict[str, pd.DataFrame],
    analyses: dict[str, TimeframeAnalysis],
    external: ExternalFactors,
    source_label: str,
) -> MarketContext:
    """Bind pre-fetched external data with enriched bars and ICT analyses."""
    metrics = daily_metrics(enriched["1d"])
    ctx = MarketContext(
        enriched=enriched,
        analyses=analyses,
        metrics=metrics,
        price=float(metrics["current_price"]),
        external=external,
        source_label=source_label,
    )
    log.debug(
        "market context assembled price=%.2f dxy=%r headlines=%d",
        ctx.price,
        external.dxy_impact,
        len(external.news_headlines),
    )
    return ctx


def build_market_context(
    enriched: dict[str, pd.DataFrame],
    analyses: dict[str, TimeframeAnalysis],
) -> MarketContext:
    """Legacy entry — fetches external again. Prefer fetch_all_data + assemble_market_context."""
    from src.data.fetch_pipeline import fetch_external_bundle

    external = fetch_external_bundle(parallel_http=False)
    return assemble_market_context(enriched, analyses, external, get_active_source())
