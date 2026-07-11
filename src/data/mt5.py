"""Optional MetaTrader 5 execution bridge.

This module keeps MT5 behind an optional account/execution boundary without
making the MetaTrader5 package a required dependency. Market bars still come
from the normal TradingView data path; MT5 is reserved for account checks and
future order execution.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, runtime_checkable

from src.config import (
    MT5_ACCOUNT,
    MT5_ENABLED,
    MT5_PASSWORD,
    MT5_PATH,
    MT5_SERVER,
    MT5_SYMBOL,
    MT5_TIMEOUT_MS,
)


@dataclass(frozen=True)
class MT5Config:
    enabled: bool = MT5_ENABLED
    symbol: str = MT5_SYMBOL
    account: str = MT5_ACCOUNT
    password: str = MT5_PASSWORD
    server: str = MT5_SERVER
    path: str = MT5_PATH
    timeout_ms: int = MT5_TIMEOUT_MS


@runtime_checkable
class MT5Provider(Protocol):
    name: str

    def is_available(self) -> bool:
        ...

    def account_info(self) -> dict[str, object]:
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

    def shutdown(self) -> None:
        return None


class MetaTrader5Provider:
    name = "mt5"

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
        if self.config.account:
            kwargs["login"] = int(self.config.account)
        if self.config.password:
            kwargs["password"] = self.config.password
        if self.config.server:
            kwargs["server"] = self.config.server
        kwargs["timeout"] = self.config.timeout_ms
        if not self._mt5.initialize(**kwargs):
            code, message = self._mt5.last_error()
            raise MT5UnavailableError(f"MT5 initialize failed: {code} {message}")
        self._initialized = True


def get_mt5_provider(config: MT5Config | None = None) -> MT5Provider:
    cfg = config or MT5Config()
    if not cfg.enabled:
        return DisabledMT5Provider()
    try:
        return MetaTrader5Provider(cfg)
    except MT5UnavailableError as exc:
        return DisabledMT5Provider(str(exc))
