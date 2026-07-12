from __future__ import annotations

import pandas as pd

from src.analysis.report_engine import TradingSignal
from src.backtest.simulator import simulate_signal
from src.backtest.types import BacktestConfig


def _signal(direction: str = "BUY") -> TradingSignal:
    return TradingSignal(
        name="unit",
        direction=direction,
        direction_cn=direction,
        entry_low=100,
        entry_high=101,
        stop_loss=98 if direction == "BUY" else 103,
        take_profits=[104, 106, 108] if direction == "BUY" else [96, 94, 92],
        risk_reward="1:1",
        sentiment_bias_pct="50%",
        position_size="test",
        note="test",
        theme="long" if direction == "BUY" else "short",
        setup_type="unit_setup",
    )


def _df(rows: list[tuple[float, float, float, float]]) -> pd.DataFrame:
    idx = pd.date_range("2026-01-01", periods=len(rows), freq="5min", tz="UTC")
    return pd.DataFrame(rows, columns=["Open", "High", "Low", "Close"], index=idx).assign(Volume=100)


def test_buy_signal_hits_tp1() -> None:
    result = simulate_signal(
        _signal("BUY"),
        _df([(102, 103, 100.8, 102), (102, 104.5, 101.5, 104)]),
        pd.Timestamp("2026-01-01", tz="UTC"),
        BacktestConfig(),
    )
    assert result.exit_reason == "tp1"
    assert result.r_multiple > 0


def test_sell_signal_hits_stop() -> None:
    result = simulate_signal(
        _signal("SELL"),
        _df([(99, 100.5, 98.8, 99), (99, 103.5, 98, 103)]),
        pd.Timestamp("2026-01-01", tz="UTC"),
        BacktestConfig(),
    )
    assert result.exit_reason == "stop"
    assert result.r_multiple < 0


def test_same_bar_stop_first_is_conservative() -> None:
    result = simulate_signal(
        _signal("BUY"),
        _df([(100.5, 105, 97.5, 102)]),
        pd.Timestamp("2026-01-01", tz="UTC"),
        BacktestConfig(conservative_same_bar=True),
    )
    assert result.exit_reason == "stop"


def test_slippage_fill_must_be_inside_bar_range() -> None:
    result = simulate_signal(
        _signal("BUY"),
        _df([(100, 101, 99, 100.5)]),
        pd.Timestamp("2026-01-01", tz="UTC"),
        BacktestConfig(slippage_points=1.0),
    )
    assert result.exit_reason == "not_triggered"
    assert result.entry_time is None
