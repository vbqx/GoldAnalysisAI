"""MT5 bridge boundary tests."""

from __future__ import annotations

import pandas as pd
import pytest

from src.data.mt5 import MT5Config, MT5UnavailableError, fetch_multi_timeframe, get_mt5_provider


def test_mt5_provider_disabled_by_default_config() -> None:
    provider = get_mt5_provider(MT5Config(enabled=False))

    assert provider.is_available() is False
    with pytest.raises(MT5UnavailableError):
        provider.account_info()
    with pytest.raises(MT5UnavailableError):
        provider.fetch_rates("5m", 10)


class _FakeMT5Provider:
    name = "fake_mt5"

    def is_available(self) -> bool:
        return True

    def account_info(self) -> dict[str, object]:
        return {"login": 123, "server": "demo"}

    def fetch_rates(self, timeframe: str, n_bars: int) -> pd.DataFrame:
        if timeframe == "1d":
            idx = pd.date_range("2026-01-01", periods=3, freq="1D", tz="UTC")
        else:
            idx = pd.date_range("2026-01-01", periods=48, freq="5min", tz="UTC")
        return pd.DataFrame(
            {
                "Open": [1.0] * len(idx),
                "High": [2.0] * len(idx),
                "Low": [0.5] * len(idx),
                "Close": [1.5] * len(idx),
                "Volume": [10] * len(idx),
            },
            index=idx,
        )

    def shutdown(self) -> None:
        return None


def test_mt5_fetch_multi_timeframe_aggregates_middle_frames() -> None:
    data = fetch_multi_timeframe(_FakeMT5Provider())

    assert set(data) == {"5m", "15m", "1h", "4h", "1d"}
    assert len(data["5m"]) == 48
    assert len(data["15m"]) > 0
    assert len(data["1h"]) > 0
    assert len(data["4h"]) > 0
    assert len(data["1d"]) == 3


def test_fetcher_uses_mt5_when_enabled(monkeypatch: pytest.MonkeyPatch) -> None:
    from src.data import fetcher

    expected = {"5m": pd.DataFrame({"Open": [1.0], "High": [1.0], "Low": [1.0], "Close": [1.0], "Volume": [1]})}
    monkeypatch.setattr(fetcher, "MT5_ENABLED", True)
    monkeypatch.setattr(fetcher, "MT5_SYMBOL", "XAUUSD")
    monkeypatch.setattr(fetcher, "fetch_mt5_multi_timeframe", lambda: expected)

    assert fetcher.fetch_multi_timeframe() is expected
    assert "MT5" in fetcher.get_active_source()
