"""Market data fetcher — TradingView (via tvDatafeed)."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Literal

import pandas as pd

from src.data import tradingview
from src.log import get_logger

log = get_logger(__name__)

Timeframe = Literal["5m", "15m", "1h", "4h", "1d"]


def clear_cache() -> None:
    log.debug("clearing TradingView client cache")
    tradingview.reset_client()


def get_active_source() -> str:
    return tradingview.source_label()


def fetch_multi_timeframe() -> dict[Timeframe, pd.DataFrame]:
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


def market_metrics(df_1d: pd.DataFrame, df_5m: pd.DataFrame) -> dict:
    """Daily metrics anchored to the same latest 5m snapshot as the report."""
    metrics = daily_metrics(df_1d)
    if df_5m.empty:
        return metrics

    latest_5m = df_5m.iloc[-1]
    current_price = float(latest_5m["Close"])
    last_5m_date = pd.Timestamp(df_5m.index[-1]).date()
    last_1d_date = pd.Timestamp(df_1d.index[-1]).date()
    if last_1d_date < last_5m_date:
        # The daily feed only has the completed session. Its latest close is
        # therefore today's comparison close, while today's range comes from 5m.
        prev_close = float(df_1d.iloc[-1]["Close"])
        same_session = [pd.Timestamp(idx).date() == last_5m_date for idx in df_5m.index]
        session = df_5m.loc[same_session]
        daily_high = float(session["High"].max()) if not session.empty else float(latest_5m["High"])
        daily_low = float(session["Low"].min()) if not session.empty else float(latest_5m["Low"])
    else:
        prev_close = float(metrics["prev_close"])
        daily_high = max(float(metrics["daily_high"]), float(latest_5m["High"]), current_price)
        daily_low = min(float(metrics["daily_low"]), float(latest_5m["Low"]), current_price)

    change = current_price - prev_close
    metrics.update(
        {
            "current_price": current_price,
            "daily_change": change,
            "daily_change_pct": (change / prev_close) * 100 if prev_close else 0.0,
            "daily_high": max(daily_high, current_price),
            "daily_low": min(daily_low, current_price),
            "prev_close": prev_close,
        }
    )
    return metrics


UTC8 = timezone(timedelta(hours=8))


def utc8_now() -> datetime:
    return datetime.now(UTC8)


def format_utc8(iso_value: object, *, fmt: str = "%Y-%m-%d %H:%M") -> str:
    """Format an ISO UTC timestamp for UI display in Beijing time (UTC+8)."""
    raw = str(iso_value or "").strip()
    if not raw:
        return "—"
    if len(raw) >= 16 and raw[0].isdigit() and "T" in raw[:20]:
        compact = raw.rstrip("Z")[:15]
        try:
            dt = datetime.strptime(compact, "%Y%m%dT%H%M%S").replace(tzinfo=timezone.utc)
            local = dt.astimezone(UTC8)
            return f"{local.strftime(fmt)} (UTC+8)"
        except ValueError:
            pass
    try:
        normalized = raw.replace("Z", "+00:00")
        dt = datetime.fromisoformat(normalized)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        local = dt.astimezone(UTC8)
        return f"{local.strftime(fmt)} (UTC+8)"
    except ValueError:
        return raw[:19].replace("T", " ")
