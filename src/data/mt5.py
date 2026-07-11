"""Optional MetaTrader 5 bridge.

This module reserves the MT5 integration boundary without making MT5 a required
dependency. The rest of the app can ask for a provider and will receive either a
disabled provider or a real MetaTrader5-backed provider when configured.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, runtime_checkable

import pandas as pd

from src.config import MT5_ENABLED, MT5_LOGIN, MT5_PASSWORD, MT5_PATH, MT5_SERVER, MT5_SYMBOL


@dataclass(frozen=True)
class MT5Config:
    enabled: bool = MT5_ENABLED
    symbol: str = MT5_SYMBOL
    login: str = MT5_LOGIN
    password: str = MT5_PASSWORD
    server: str = MT5_SERVER
    path: str = MT5_PATH


@runtime_checkable
class MT5Provider(Protocol):
    name: str

    def is_available(self) -> bool:
        ...

    def account_info(self) -> dict[str, object]:
        ...

    def fetch_rates(self, timeframe: str, n_bars: int) -> pd.DataFrame:
        ...

    def shutdown(self) -> None:
        ...


class MT5UnavailableError(RuntimeError):
    """Raised when MT5 is requested but not available or not configured."""


class DisabledMT5Provider:
    name = "mt5_disabled"

    def __init__(self, reason: str = "MT5_ENABLED=false") -> None:
        self.reason = reason

    def is_available(self) -> bool:
        return False

    def account_info(self) -> dict[str, object]:
        raise MT5UnavailableError(self.reason)

    def fetch_rates(self, timeframe: str, n_bars: int) -> pd.DataFrame:
        raise MT5UnavailableError(self.reason)

    def shutdown(self) -> None:
        return None


class MetaTrader5Provider:
    name = "mt5"

    _TIMEFRAMES = {
        "1m": "TIMEFRAME_M1",
        "5m": "TIMEFRAME_M5",
        "15m": "TIMEFRAME_M15",
        "30m": "TIMEFRAME_M30",
        "1h": "TIMEFRAME_H1",
        "4h": "TIMEFRAME_H4",
        "1d": "TIMEFRAME_D1",
    }

    def __init__(self, config: MT5Config | None = None) -> None:
        self.config = config or MT5Config()
        try:
            import MetaTrader5 as mt5
        except ImportError as exc:
            raise MT5UnavailableError("MetaTrader5 package is not installed") from exc
        self._mt5 = mt5
        self._initialized = False

    def is_available(self) -> bool:
        try:
            self._ensure_initialized()
        except MT5UnavailableError:
            return False
        return True

    def account_info(self) -> dict[str, object]:
        self._ensure_initialized()
        info = self._mt5.account_info()
        if info is None:
            code, message = self._mt5.last_error()
            raise MT5UnavailableError(f"MT5 account_info failed: {code} {message}")
        data = info._asdict()
        return {
            "login": data.get("login"),
            "server": data.get("server"),
            "name": data.get("name"),
            "currency": data.get("currency"),
            "balance": data.get("balance"),
            "equity": data.get("equity"),
            "leverage": data.get("leverage"),
            "trade_mode": data.get("trade_mode"),
        }

    def fetch_rates(self, timeframe: str, n_bars: int) -> pd.DataFrame:
        self._ensure_initialized()
        if n_bars <= 0:
            raise ValueError("n_bars must be positive")
        tf_name = self._TIMEFRAMES.get(timeframe)
        if not tf_name:
            raise ValueError(f"Unsupported MT5 timeframe: {timeframe}")
        rates = self._mt5.copy_rates_from_pos(
            self.config.symbol,
            getattr(self._mt5, tf_name),
            0,
            n_bars,
        )
        if rates is None or len(rates) == 0:
            raise MT5UnavailableError(f"MT5 returned no rates for {self.config.symbol} {timeframe}")
        df = pd.DataFrame(rates)
        df["time"] = pd.to_datetime(df["time"], unit="s", utc=True)
        df = df.set_index("time")
        return df.rename(
            columns={
                "open": "Open",
                "high": "High",
                "low": "Low",
                "close": "Close",
                "tick_volume": "Volume",
            }
        )[["Open", "High", "Low", "Close", "Volume"]].copy()

    def shutdown(self) -> None:
        if self._initialized:
            self._mt5.shutdown()
            self._initialized = False

    def _ensure_initialized(self) -> None:
        if self._initialized:
            return
        kwargs = {}
        if self.config.path:
            kwargs["path"] = self.config.path
        if self.config.login:
            kwargs["login"] = int(self.config.login)
        if self.config.password:
            kwargs["password"] = self.config.password
        if self.config.server:
            kwargs["server"] = self.config.server
        if not self._mt5.initialize(**kwargs):
            code, message = self._mt5.last_error()
            raise MT5UnavailableError(f"MT5 initialize failed: {code} {message}")
        if not self._mt5.symbol_select(self.config.symbol, True):
            code, message = self._mt5.last_error()
            self._mt5.shutdown()
            raise MT5UnavailableError(f"MT5 symbol_select failed: {code} {message}")
        self._initialized = True


def _resample_ohlcv(df: pd.DataFrame, rule: str) -> pd.DataFrame:
    ohlcv = df.resample(rule).agg(
        {"Open": "first", "High": "max", "Low": "min", "Close": "last", "Volume": "sum"}
    )
    return ohlcv.dropna()


def fetch_multi_timeframe(provider: MT5Provider | None = None) -> dict[str, pd.DataFrame]:
    """Fetch the app's standard OHLCV bundle from MT5.

    The pipeline needs 5m, 15m, 1h, 4h and 1d bars. MT5 supplies 5m and 1d
    directly; the middle timeframes are locally aggregated to keep the data
    contract identical to the TradingView path.
    """
    p = provider or get_mt5_provider()
    df_5m = p.fetch_rates("5m", 5000)
    df_1d = p.fetch_rates("1d", 365)
    return {
        "5m": df_5m,
        "15m": _resample_ohlcv(df_5m, "15min"),
        "1h": _resample_ohlcv(df_5m, "1h"),
        "4h": _resample_ohlcv(df_5m, "4h"),
        "1d": df_1d,
    }


def get_mt5_provider(config: MT5Config | None = None) -> MT5Provider:
    cfg = config or MT5Config()
    if not cfg.enabled:
        return DisabledMT5Provider()
    try:
        return MetaTrader5Provider(cfg)
    except MT5UnavailableError as exc:
        return DisabledMT5Provider(str(exc))
