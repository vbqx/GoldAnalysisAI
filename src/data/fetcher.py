"""Market data fetcher — TradingView (via tvDatafeed)."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Literal

import pandas as pd

from src.data import tradingview

Timeframe = Literal["5m", "15m", "1h", "4h", "1d"]


def clear_cache() -> None:
    tradingview.reset_client()


def get_active_source() -> str:
    return tradingview.source_label()


def fetch_multi_timeframe() -> dict[Timeframe, pd.DataFrame]:
    return tradingview.fetch_multi_timeframe()


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
