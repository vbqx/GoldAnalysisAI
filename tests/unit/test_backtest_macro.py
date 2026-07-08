from __future__ import annotations

import pandas as pd

from src.backtest.macro import macro_state_at


def _dxy(values: list[float]) -> pd.DataFrame:
    idx = pd.date_range("2026-01-01", periods=len(values), freq="1d", tz="UTC")
    return pd.DataFrame(
        {
            "Open": values,
            "High": values,
            "Low": values,
            "Close": values,
            "Volume": [1] * len(values),
        },
        index=idx,
    )


def test_macro_state_uses_only_bars_at_or_before_replay_time() -> None:
    state = macro_state_at(_dxy([100, 101, 80]), pd.Timestamp("2026-01-02 12:00", tz="UTC"))
    assert state.dxy_time == pd.Timestamp("2026-01-02", tz="UTC")
    assert state.dxy_close == 101
    assert state.dxy_change_1d == 1.0
    assert state.gold_bias == "bearish"


def test_macro_state_falling_dxy_is_gold_bullish() -> None:
    state = macro_state_at(_dxy([100, 99]), pd.Timestamp("2026-01-03", tz="UTC"))
    assert state.gold_bias == "bullish"
    assert state.confidence > 0
