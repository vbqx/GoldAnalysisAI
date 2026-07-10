"""MT5 bridge boundary tests."""

from __future__ import annotations

import pytest

from src.data.mt5 import MT5Config, MT5UnavailableError, get_mt5_provider


def test_mt5_provider_disabled_by_default_config() -> None:
    provider = get_mt5_provider(MT5Config(enabled=False))

    assert provider.is_available() is False
    with pytest.raises(MT5UnavailableError):
        provider.fetch_rates("5m", 10)
