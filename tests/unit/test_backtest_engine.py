from __future__ import annotations

import pandas as pd

from src.backtest.engine import make_multitimeframe, normalize_ohlcv


def test_normalize_ohlcv_accepts_lowercase_datetime_column() -> None:
    raw = pd.DataFrame(
        {
            "datetime": pd.date_range("2026-01-01", periods=4, freq="5min"),
            "open": [1, 2, 3, 4],
            "high": [2, 3, 4, 5],
            "low": [0, 1, 2, 3],
            "close": [1.5, 2.5, 3.5, 4.5],
        }
    )
    out = normalize_ohlcv(raw)
    assert list(out.columns) == ["Open", "High", "Low", "Close", "Volume"]
    assert str(out.index.tz) == "UTC"


def test_make_multitimeframe_resamples_from_5m() -> None:
    idx = pd.date_range("2026-01-01", periods=24, freq="5min", tz="UTC")
    df = pd.DataFrame(
        {
            "Open": range(24),
            "High": range(1, 25),
            "Low": range(24),
            "Close": range(1, 25),
            "Volume": [1] * 24,
        },
        index=idx,
    )
    data = make_multitimeframe(df)
    assert len(data["15m"]) == 8
    assert len(data["1h"]) == 2
