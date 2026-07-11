"""Market data fetcher — TradingView by default, optional MT5 when enabled."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Literal

import pandas as pd

from src.config import MT5_ENABLED, MT5_SYMBOL
from src.data import tradingview
from src.data.mt5 import fetch_multi_timeframe as fetch_mt5_multi_timeframe
from src.data.mt5 import get_mt5_provider
from src.log import get_logger

log = get_logger(__name__)

Timeframe = Literal["5m", "15m", "1h", "4h", "1d"]


def clear_cache() -> None:
    log.debug("clearing TradingView client cache")
    tradingview.reset_client()


def get_active_source() -> str:
    if MT5_ENABLED:
        provider = get_mt5_provider()
        return f"MT5 ({MT5_SYMBOL}, {provider.name})"
    return tradingview.source_label()


def fetch_multi_timeframe() -> dict[Timeframe, pd.DataFrame]:
    if MT5_ENABLED:
        log.info("fetch_multi_timeframe via MT5 symbol=%s", MT5_SYMBOL)
        return fetch_mt5_multi_timeframe()  # type: ignore[return-value]
    return tradingview.fetch_multi_timeframe()


def fetch_all() -> "DataFetchResult":
    """Unified fetch: bars + external. See ``src.data.fetch_pipeline``."""
    from src.data.fetch_pipeline import fetch_all_data

    return fetch_all_data()


def daily_metrics(df_1d: pd.DataFrame) -> dict:
    if len(df_1d) < 2:
        latest = df_1d.iloc[-1]
        price = float(latest["Close"])
        return {
            "current_price": price,
            "daily_change": 0.0,
            "daily_change_pct": 0.0,
            "daily_high": float(latest["High"]),
            "daily_low": float(latest["Low"]),
            "prev_close": price,
        }

    today = df_1d.iloc[-1]
    prev = df_1d.iloc[-2]
    price = float(today["Close"])
    prev_close = float(prev["Close"])
    change = price - prev_close
    change_pct = (change / prev_close) * 100 if prev_close else 0.0

    return {
        "current_price": price,
        "daily_change": change,
        "daily_change_pct": change_pct,
        "daily_high": float(today["High"]),
        "daily_low": float(today["Low"]),
        "prev_close": prev_close,
    }


def utc8_now() -> datetime:
    tz = timezone(timedelta(hours=8))
    return datetime.now(tz)
