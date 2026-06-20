"""TradingView historical data via tvDatafeed (unofficial WebSocket API)."""

from __future__ import annotations

import os
import time
from typing import TYPE_CHECKING

import pandas as pd

from src.config import (
    TV_EXCHANGE,
    TV_FETCH_RETRIES,
    TV_FETCH_RETRY_BASE_S,
    TV_FETCH_ROUND_RETRIES,
    TV_PASSWORD,
    TV_SYMBOL,
    TV_USERNAME,
)
from src.core.progress import get_progress
from src.log import get_logger

log = get_logger(__name__)

if TYPE_CHECKING:
    from tvDatafeed import Interval

_tv_client = None
_last_error: str | None = None


from src.data.proxy_env import apply_system_proxy, read_system_proxy


def _read_system_proxy() -> str | None:
    return read_system_proxy()


def _setup_proxy() -> None:
    """Configure proxy for WebSocket connections from system settings."""
    proxy = apply_system_proxy()
    if proxy:
        log.info("using proxy %s", proxy)


# Apply proxy at module import time (before tvDatafeed/websocket-client is loaded)
_setup_proxy()


def get_last_error() -> str | None:
    return _last_error


def reset_client() -> None:
    global _tv_client, _last_error
    log.debug("TradingView client reset")
    _tv_client = None
    _last_error = None


def _report_fetch(detail: str) -> None:
    get_progress().update("fetch", detail=detail)


def _get_client():
    global _tv_client
    if _tv_client is None:
        from tvDatafeed import TvDatafeed

        if TV_USERNAME and TV_PASSWORD:
            log.info("TradingView client: authenticated user")
            _tv_client = TvDatafeed(TV_USERNAME, TV_PASSWORD)
        else:
            log.info("TradingView client: anonymous access")
            _tv_client = TvDatafeed()
    return _tv_client


def _normalize(df: pd.DataFrame | None) -> pd.DataFrame:
    if df is None or df.empty:
        raise ValueError("TradingView returned empty data")

    out = df.copy()
    out.index = pd.to_datetime(out.index, utc=True)
    rename = {
        "open": "Open",
        "high": "High",
        "low": "Low",
        "close": "Close",
        "volume": "Volume",
    }
    out = out.rename(columns={k: v for k, v in rename.items() if k in out.columns})
    required = ["Open", "High", "Low", "Close", "Volume"]
    for col in required:
        if col not in out.columns:
            if col == "Volume":
                out[col] = 0
            else:
                raise ValueError(f"TradingView data missing column: {col}")
    return out[required].copy()


def _resample(df: pd.DataFrame, rule: str) -> pd.DataFrame:
    ohlcv = df.resample(rule).agg(
        {"Open": "first", "High": "max", "Low": "min", "Close": "last", "Volume": "sum"}
    )
    return ohlcv.dropna()


def compute_price_drift_1d(df_5m: pd.DataFrame, df_1d: pd.DataFrame) -> float:
    """Difference between independent 1d close and 5m-resampled 1d close (F-005)."""
    if df_5m.empty or df_1d.empty:
        return 0.0
    resampled_close = float(_resample(df_5m, "1d")["Close"].iloc[-1])
    independent_close = float(df_1d["Close"].iloc[-1])
    return round(independent_close - resampled_close, 4)


def _fetch_bars(
    interval: "Interval",
    n_bars: int,
    *,
    label: str,
    retries: int | None = None,
    exchange: str | None = None,
    symbol: str | None = None,
    report_progress: bool = True,
) -> pd.DataFrame:
    global _last_error
    max_attempts = (retries if retries is not None else TV_FETCH_RETRIES) + 1
    last_exc: Exception | None = None
    ex = exchange or TV_EXCHANGE
    sym = symbol or TV_SYMBOL

    for attempt in range(max_attempts):
        attempt_no = attempt + 1
        if report_progress:
            _report_fetch(f"{label} · 第 {attempt_no}/{max_attempts} 次请求 TradingView…")
        try:
            log.debug(
                "fetch %s:%s interval=%s n_bars=%d attempt=%d",
                ex,
                sym,
                interval,
                n_bars,
                attempt_no,
            )
            df = _get_client().get_hist(
                symbol=sym,
                exchange=ex,
                interval=interval,
                n_bars=n_bars,
            )
            result = _normalize(df)
            log.info(
                "fetch ok %s:%s interval=%s bars=%d range=%s → %s",
                ex,
                sym,
                interval,
                len(result),
                result.index[0].strftime("%Y-%m-%d"),
                result.index[-1].strftime("%Y-%m-%d"),
            )
            if report_progress:
                _report_fetch(f"{label} · 完成 {len(result)} 根 K 线")
            return result
        except Exception as exc:
            last_exc = exc
            _last_error = str(exc)
            log.warning(
                "fetch failed %s:%s interval=%s attempt=%d: %s",
                ex,
                sym,
                interval,
                attempt_no,
                exc,
            )
            if attempt < max_attempts - 1:
                wait = TV_FETCH_RETRY_BASE_S * (2**attempt)
                if report_progress:
                    _report_fetch(
                        f"{label} · 失败（{exc}）· {wait:.0f}s 后重连重试 ({attempt_no}/{max_attempts})"
                    )
                reset_client()
                time.sleep(wait)

    raise RuntimeError(
        f"{label} 拉取失败（已重试 {max_attempts} 次）: {last_exc}. "
        "若在国内网络，可能需要代理/VPN 才能连接 TradingView WebSocket。"
    ) from last_exc


def fetch_symbol_daily(
    exchange: str,
    symbol: str,
    *,
    n_bars: int = 5,
    label: str | None = None,
) -> pd.DataFrame:
    """Fetch daily bars for a non-primary symbol (e.g. DXY) without pipeline fetch progress noise."""
    from tvDatafeed import Interval

    return _fetch_bars(
        Interval.in_daily,
        n_bars,
        label=label or symbol,
        exchange=exchange,
        symbol=symbol,
        retries=1,
        report_progress=False,
    )


def _fetch_multi_timeframe_once() -> dict[str, pd.DataFrame]:
    from tvDatafeed import Interval

    _report_fetch("① 5m K 线 (5000 bars) · TradingView WebSocket")
    df_5m = _fetch_bars(Interval.in_5_minute, n_bars=5000, label="5m")
    time.sleep(0.8)

    _report_fetch("② 1d K 线 (365 bars) · TradingView WebSocket")
    df_1d = _fetch_bars(Interval.in_daily, n_bars=365, label="1d")

    _report_fetch("③ 本地聚合 15m / 1h / 4h")
    out = {
        "5m": df_5m,
        "15m": _resample(df_5m, "15min"),
        "1h": _resample(df_5m, "1h"),
        "4h": _resample(df_5m, "4h"),
        "1d": df_1d,
    }
    log.info(
        "fetch_multi_timeframe done close_5m=%.2f bars=%s",
        float(df_5m["Close"].iloc[-1]),
        {k: len(v) for k, v in out.items()},
    )
    return out


def fetch_multi_timeframe() -> dict[str, pd.DataFrame]:
    """Fetch all timeframes with minimal TradingView requests (2 calls)."""
    log.info("fetch_multi_timeframe start %s:%s", TV_EXCHANGE, TV_SYMBOL)
    _report_fetch(f"连接 TradingView · {TV_EXCHANGE}:{TV_SYMBOL}")

    last_exc: Exception | None = None
    rounds = TV_FETCH_ROUND_RETRIES + 1
    for round_idx in range(rounds):
        if round_idx > 0:
            wait = TV_FETCH_RETRY_BASE_S * (2**round_idx)
            _report_fetch(
                f"整轮重试 {round_idx + 1}/{rounds} · 重置 WebSocket · {wait:.0f}s 后重试…"
            )
            reset_client()
            time.sleep(wait)
        try:
            return _fetch_multi_timeframe_once()
        except RuntimeError as exc:
            last_exc = exc
            log.warning("fetch_multi_timeframe round %d/%d failed: %s", round_idx + 1, rounds, exc)

    raise RuntimeError(
        f"TradingView fetch failed for {TV_EXCHANGE}:{TV_SYMBOL} — {last_exc}. "
        "若在国内网络，可能需要代理/VPN 才能连接 TradingView WebSocket。"
    ) from last_exc


def source_label() -> str:
    auth = "已登录" if TV_USERNAME else "匿名"
    return f"TradingView ({TV_EXCHANGE}:{TV_SYMBOL}, {auth})"
