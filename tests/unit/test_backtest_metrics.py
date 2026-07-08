from __future__ import annotations

import pandas as pd

from src.backtest.metrics import summarize_trades
from src.backtest.types import TradeResult


def _trade(r: float, reason: str = "tp1") -> TradeResult:
    ts = pd.Timestamp("2026-01-01", tz="UTC")
    return TradeResult(
        signal_time=ts,
        entry_time=ts,
        exit_time=ts,
        direction="BUY",
        setup_type="unit",
        signal_name="unit",
        entry_price=100,
        stop_loss=98,
        take_profits=[104],
        exit_price=104 if r > 0 else 98,
        exit_reason=reason,  # type: ignore[arg-type]
        r_multiple=r,
        pnl_points=r * 2,
        holding_bars=1,
    )


def test_summary_uses_r_multiple_and_drawdown() -> None:
    summary = summarize_trades([_trade(1.5), _trade(-1.0, "stop"), _trade(0.5)])
    assert summary["closed"] == 3
    assert summary["win_rate"] == 0.6667
    assert summary["total_r"] == 1.0
    assert summary["profit_factor"] == 2.0
    assert summary["max_drawdown_r"] == -1.0
