"""Backtesting primitives for the rule-based XAUUSD analysis system."""

from src.backtest.types import BacktestConfig, BacktestMode, BacktestResult, MacroReplayState, TradeResult

__all__ = [
    "BacktestConfig",
    "BacktestMode",
    "BacktestResult",
    "MacroReplayState",
    "TradeResult",
    "run_backtest",
    "run_random_window_backtest",
]


def __getattr__(name: str):
    if name in {"run_backtest", "run_random_window_backtest"}:
        from src.backtest.engine import run_backtest, run_random_window_backtest

        return {
            "run_backtest": run_backtest,
            "run_random_window_backtest": run_random_window_backtest,
        }[name]
    raise AttributeError(name)
