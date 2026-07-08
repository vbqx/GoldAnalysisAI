"""Typed data structures for institutional-style backtesting."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import StrEnum
from typing import Any, Literal

import pandas as pd


class BacktestMode(StrEnum):
    CONTINUOUS = "continuous"
    RANDOM_WINDOWS = "random_windows"
    WALK_FORWARD = "walk_forward"
    REGIME_SPLIT = "regime_split"


ExitReason = Literal["tp1", "tp2", "tp3", "stop", "timeout", "not_triggered", "no_future"]


@dataclass(frozen=True)
class BacktestConfig:
    symbol: str = "XAUUSD"
    mode: BacktestMode = BacktestMode.CONTINUOUS
    warmup_bars: int = 500
    step_bars: int = 12
    max_holding_bars: int = 96
    fee_points: float = 0.0
    slippage_points: float = 0.0
    conservative_same_bar: bool = True
    min_score: float = 0.0
    use_macro: bool = False
    dxy_bars: int = 1500
    macro_weight: float = 0.15
    random_windows: int = 100
    random_window_bars: int = 20 * 24 * 12
    random_seed: int = 42


@dataclass(frozen=True)
class MacroReplayState:
    time: pd.Timestamp
    dxy_time: pd.Timestamp | None
    dxy_close: float | None
    dxy_change_1d: float | None
    dxy_change_5d: float | None
    dxy_change_20d: float | None
    gold_bias: Literal["bullish", "bearish", "neutral"]
    confidence: float
    source: str = "historical_dxy"

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["time"] = str(self.time)
        if d["dxy_time"] is not None:
            d["dxy_time"] = str(d["dxy_time"])
        return d


@dataclass(frozen=True)
class TradeResult:
    signal_time: pd.Timestamp
    entry_time: pd.Timestamp | None
    exit_time: pd.Timestamp | None
    direction: str
    setup_type: str
    signal_name: str
    entry_price: float
    stop_loss: float
    take_profits: list[float]
    exit_price: float | None
    exit_reason: ExitReason
    r_multiple: float
    pnl_points: float
    holding_bars: int
    signal_score: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def triggered(self) -> bool:
        return self.entry_time is not None and self.exit_reason != "not_triggered"

    @property
    def won(self) -> bool:
        return self.r_multiple > 0

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        for key in ("signal_time", "entry_time", "exit_time"):
            if d[key] is not None:
                d[key] = str(d[key])
        return d


@dataclass(frozen=True)
class BacktestResult:
    config: BacktestConfig
    trades: list[TradeResult]
    summary: dict[str, Any]
    by_setup: list[dict[str, Any]]
    by_direction: list[dict[str, Any]]
    diagnostics: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "config": asdict(self.config),
            "summary": self.summary,
            "by_setup": self.by_setup,
            "by_direction": self.by_direction,
            "diagnostics": self.diagnostics,
            "trades": [t.to_dict() for t in self.trades],
        }
