"""TradingView fetch retry and progress reporting."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from src.core.progress import ProgressReporter, reset_progress, set_progress
from src.data import tradingview


def _sample_df() -> pd.DataFrame:
    idx = pd.date_range("2026-01-01", periods=3, freq="5min", tz="UTC")
    return pd.DataFrame(
        {
            "open": [1.0, 2.0, 3.0],
            "high": [1.1, 2.1, 3.1],
            "low": [0.9, 1.9, 2.9],
            "close": [1.0, 2.0, 3.0],
            "volume": [10, 10, 10],
        },
        index=idx,
    )


def test_fetch_bars_retries_then_succeeds(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(tradingview, "TV_FETCH_RETRIES", 2)
    monkeypatch.setattr(tradingview, "TV_FETCH_RETRY_BASE_S", 0.0)
    calls = {"n": 0}

    def fake_get_hist(*_args, **_kwargs):
        calls["n"] += 1
        if calls["n"] < 3:
            return pd.DataFrame()
        return _sample_df()

    tv = MagicMock()
    tv.get_hist.side_effect = fake_get_hist
    monkeypatch.setattr(tradingview, "_get_client", lambda: tv)

    resets: list[str] = []
    monkeypatch.setattr(tradingview, "reset_client", lambda: resets.append("reset"))

    reporter = ProgressReporter()
    reporter.start("fetch", "拉取多周期行情", "test")
    token = set_progress(reporter)
    try:
        from tvDatafeed import Interval

        result = tradingview._fetch_bars(Interval.in_5_minute, 100, label="5m", retries=2)
    finally:
        reset_progress(token)

    assert len(result) == 3
    assert calls["n"] == 3
    assert len(resets) == 2
    details = [s["detail"] for s in reporter.snapshot() if s["id"] == "fetch"]
    assert any("5m" in d for d in details)
    assert any("完成" in d for d in details)


def test_fetch_bars_exhausted_raises(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(tradingview, "TV_FETCH_RETRY_BASE_S", 0.0)
    tv = MagicMock()
    tv.get_hist.return_value = pd.DataFrame()
    monkeypatch.setattr(tradingview, "_get_client", lambda: tv)
    monkeypatch.setattr(tradingview, "reset_client", lambda: None)

    from tvDatafeed import Interval

    with pytest.raises(RuntimeError, match="5m 拉取失败"):
        tradingview._fetch_bars(Interval.in_5_minute, 100, label="5m", retries=1)
