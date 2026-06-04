"""TradingView historical data via tvDatafeed (unofficial WebSocket API)."""

from __future__ import annotations

import os
import time
from typing import TYPE_CHECKING

import pandas as pd

from src.config import TV_EXCHANGE, TV_PASSWORD, TV_SYMBOL, TV_USERNAME
from src.log import get_logger

log = get_logger(__name__)

if TYPE_CHECKING:
    from tvDatafeed import Interval

_tv_client = None
_last_error: str | None = None


def _read_system_proxy() -> str | None:
    """Detect system HTTP proxy from env var or Windows registry."""
    for key in ("HTTPS_PROXY", "https_proxy", "HTTP_PROXY", "http_proxy"):
        if val := os.environ.get(key):
            return val

    try:
        import winreg
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Internet Settings",
        )
        try:
            enable, _ = winreg.QueryValueEx(key, "ProxyEnable")
            if enable:
                server, _ = winreg.QueryValueEx(key, "ProxyServer")
                winreg.CloseKey(key)
                server = server.split(";")[0].strip()
                return f"http://{server}" if "://" not in server else server
        except Exception:
            pass
        winreg.CloseKey(key)
    except Exception:
        pass

    return None


def _setup_proxy() -> None:
    """Configure proxy for WebSocket connections from system settings."""
    proxy = _read_system_proxy()
    if proxy:
        os.environ.setdefault("http_proxy", proxy)
        os.environ.setdefault("https_proxy", proxy)
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


def _fetch_bars(interval: "Interval", n_bars: int, retries: int = 2) -> pd.DataFrame:
    global _last_error
    tv = _get_client()
    last_exc: Exception | None = None

    for attempt in range(retries + 1):
        try:
            log.debug(
                "fetch %s:%s interval=%s n_bars=%d attempt=%d",
                TV_EXCHANGE,
                TV_SYMBOL,
                interval,
                n_bars,
                attempt + 1,
            )
            df = tv.get_hist(
                symbol=TV_SYMBOL,
                exchange=TV_EXCHANGE,
                interval=interval,
                n_bars=n_bars,
            )
            result = _normalize(df)
            log.info(
                "fetch ok %s:%s interval=%s bars=%d range=%s → %s",
                TV_EXCHANGE,
                TV_SYMBOL,
                interval,
                len(result),
                result.index[0].strftime("%Y-%m-%d"),
                result.index[-1].strftime("%Y-%m-%d"),
            )
            return result
        except Exception as exc:
            last_exc = exc
            _last_error = str(exc)
            log.warning(
                "fetch failed %s:%s interval=%s attempt=%d: %s",
                TV_EXCHANGE,
                TV_SYMBOL,
                interval,
                attempt + 1,
                exc,
            )
            if attempt < retries:
                time.sleep(1.5 * (attempt + 1))

    raise RuntimeError(
        f"TradingView fetch failed for {TV_EXCHANGE}:{TV_SYMBOL} — {last_exc}. "
        "若在国内网络，可能需要代理/VPN 才能连接 TradingView WebSocket。"
    ) from last_exc


def fetch_multi_timeframe() -> dict[str, pd.DataFrame]:
    """Fetch all timeframes with minimal TradingView requests (2 calls)."""
    from tvDatafeed import Interval

    log.info("fetch_multi_timeframe start %s:%s", TV_EXCHANGE, TV_SYMBOL)
    df_5m = _fetch_bars(Interval.in_5_minute, n_bars=5000)
    time.sleep(0.8)

    df_1d = _fetch_bars(Interval.in_daily, n_bars=365)

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


def source_label() -> str:
    auth = "已登录" if TV_USERNAME else "匿名"
    return f"TradingView ({TV_EXCHANGE}:{TV_SYMBOL}, {auth})"
