"""Unified data fetch — TradingView bars + external feeds at pipeline start."""

from __future__ import annotations

import json
import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass

import pandas as pd

from src.config import MT5_ENABLED, MT5_SYMBOL, TV_EXCHANGE, TV_SYMBOL
from src.core.progress import get_progress
from src.core.types import ExternalFactors
from src.data.aggregator import merge_external
from src.data.fetcher import fetch_multi_timeframe, get_active_source
from src.data.sources import FundamentalsDataSource, NewsDataSource, SocialDataSource
from src.log import get_logger

log = get_logger(__name__)

Timeframe = str


@dataclass
class DataFetchResult:
    """All raw inputs fetched before indicators / ICT / agents."""

    raw: dict[str, pd.DataFrame]
    external: ExternalFactors
    source_label: str

    @property
    def bars_summary(self) -> dict[str, int]:
        return {tf: len(df) for tf, df in self.raw.items()}

    def external_preview(self) -> dict:
        ext = self.external
        return {
            "source_label": self.source_label,
            "dxy_impact": ext.dxy_impact,
            "risk_events": ext.risk_events,
            "news_headlines": ext.news_headlines[:12],
            "headline_count": len(ext.news_headlines),
            "structured_headlines": len(ext.headline_items),
            "calendar_events": len(ext.calendar_events),
            "macro_quotes": len(ext.macro_quotes),
            "social_sentiment": ext.social_sentiment,
            "social_post_count": len(ext.social_posts),
            "sources": ext.sources,
        }


def _fetch_news_external() -> ExternalFactors:
    return NewsDataSource().fetch_external()


def _fetch_social_external() -> ExternalFactors:
    return SocialDataSource().fetch_external()


def _fetch_fundamentals_external() -> ExternalFactors:
    return FundamentalsDataSource().fetch_external()


def fetch_external_bundle(*, parallel_http: bool = True) -> ExternalFactors:
    """News + social + fundamentals (DXY/US10Y). All three HTTP sources run in parallel when enabled."""
    if parallel_http:
        with ThreadPoolExecutor(max_workers=3) as pool:
            fut_news = pool.submit(_fetch_news_external)
            fut_social = pool.submit(_fetch_social_external)
            fut_fund = pool.submit(_fetch_fundamentals_external)
            news_ext = fut_news.result()
            social_ext = fut_social.result()
            fund_ext = fut_fund.result()
    else:
        news_ext = _fetch_news_external()
        fund_ext = _fetch_fundamentals_external()
        social_ext = _fetch_social_external()
    return merge_external(news_ext, fund_ext, social_ext)


def fetch_all_data() -> DataFetchResult:
    """
    Pull everything up front:
    1. Market multi-timeframe OHLCV (TradingView by default, MT5 when enabled)
    2. News / calendar / DXY / TV social
    """
    prog = get_progress()
    t0 = time.perf_counter()

    market_symbol = f"MT5:{MT5_SYMBOL}" if MT5_ENABLED else f"{TV_EXCHANGE}:{TV_SYMBOL}"
    market_task = "mt5_bars" if MT5_ENABLED else "tradingview_bars"

    prog.start("fetch", "数据拉取", f"K线 · {market_symbol}")
    try:
        raw = fetch_multi_timeframe()
    except RuntimeError as exc:
        prog.fail("fetch", str(exc)[:240])
        raise

    prog.update("fetch", detail="外部 · 新闻 / DXY / 社媒")
    external = fetch_external_bundle()
    source_label = get_active_source()

    elapsed_ms = int((time.perf_counter() - t0) * 1000)
    bars = {tf: len(df) for tf, df in raw.items()}
    ext_bits: list[str] = [f"{len(bars)} 周期 · 5m {bars.get('5m', 0)} 根"]
    if external.dxy_impact != "—":
        ext_bits.append("DXY")
    if external.news_headlines:
        ext_bits.append(f"{len(external.news_headlines)} 条新闻")
    if external.social_sentiment != "—":
        ext_bits.append("社媒")
    if external.sources:
        ext_bits.append(f"来源 {len(external.sources)}")

    result = DataFetchResult(raw=raw, external=external, source_label=source_label)

    prog.stage_io(
        "fetch",
        input_text=json.dumps(
            {
                "symbol": market_symbol,
                "market_symbol": market_symbol,
                "tasks": [market_task, "jin10_mcp", "dxy", "tv_social"],
            },
            ensure_ascii=False,
            indent=2,
        ),
        output_text=json.dumps(
            {"bars": bars, **result.external_preview()},
            ensure_ascii=False,
            indent=2,
        ),
        latency_ms=elapsed_ms,
        label="数据拉取",
    )
    prog.done("fetch", " · ".join(ext_bits))
    log.info(
        "fetch_all_data bars=%s external_sources=%s elapsed=%dms",
        bars,
        external.sources,
        elapsed_ms,
    )
    return result
