"""MT5 bridge boundary tests."""

from __future__ import annotations

import importlib

import pytest

from src.data.mt5 import MT5Config, MT5UnavailableError, get_mt5_provider


def test_mt5_provider_disabled_by_default_config() -> None:
    provider = get_mt5_provider(MT5Config(enabled=False))

    assert provider.is_available() is False
    with pytest.raises(MT5UnavailableError):
        provider.account_info()


def test_mt5_account_env_feeds_config(monkeypatch: pytest.MonkeyPatch) -> None:
    import src.config as config

    monkeypatch.setenv("MT5_ACCOUNT", "277790660")
    reloaded = importlib.reload(config)
    try:
        assert reloaded.MT5_ACCOUNT == "277790660"
    finally:
        importlib.reload(config)
