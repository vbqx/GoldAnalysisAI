"""Execution simulator with conservative OHLC assumptions."""

from __future__ import annotations

import pandas as pd

from src.analysis.report_engine import TradingSignal
from src.backtest.types import BacktestConfig, TradeResult


def _signal_value(signal: TradingSignal | dict, key: str, default=None):
    if isinstance(signal, dict):
        return signal.get(key, default)
    return getattr(signal, key, default)


def _entry_price(signal: TradingSignal | dict, direction: str, slippage: float) -> float:
    low = float(_signal_value(signal, "entry_low"))
    high = float(_signal_value(signal, "entry_high"))
    if direction == "BUY":
        return high + slippage
    return low - slippage


def _risk_points(entry: float, stop: float, direction: str) -> float:
    if direction == "BUY":
        return entry - stop
    return stop - entry


def _entered(row: pd.Series, signal: TradingSignal | dict) -> bool:
    low = float(_signal_value(signal, "entry_low"))
    high = float(_signal_value(signal, "entry_high"))
    return float(row["Low"]) <= high and float(row["High"]) >= low


def _hit_stop(row: pd.Series, stop: float, direction: str) -> bool:
    if direction == "BUY":
        return float(row["Low"]) <= stop
    return float(row["High"]) >= stop


def _hit_tp(row: pd.Series, tp: float, direction: str) -> bool:
    if direction == "BUY":
        return float(row["High"]) >= tp
    return float(row["Low"]) <= tp


def _pnl_points(entry: float, exit_price: float, direction: str, fee_points: float) -> float:
    gross = exit_price - entry if direction == "BUY" else entry - exit_price
    return gross - fee_points


def _signal_metadata(signal: TradingSignal | dict) -> dict:
    return {
        "macro_bias": _signal_value(signal, "macro_bias"),
        "macro_confidence": _signal_value(signal, "macro_confidence"),
        "macro_score_delta": _signal_value(signal, "macro_score_delta"),
        "macro_dxy_time": _signal_value(signal, "macro_dxy_time"),
    }


def simulate_signal(
    signal: TradingSignal | dict,
    future_5m: pd.DataFrame,
    signal_time: pd.Timestamp,
    config: BacktestConfig,
) -> TradeResult:
    """Simulate one signal using future 5m bars only.

    Conservative mode assumes a same-bar stop is hit before profit targets when
    both are reachable inside one OHLC candle.
    """
    direction = str(_signal_value(signal, "direction", "")).upper()
    stop = float(_signal_value(signal, "stop_loss"))
    tps = [float(x) for x in (_signal_value(signal, "take_profits", []) or [])]
    setup_type = str(_signal_value(signal, "setup_type", ""))
    name = str(_signal_value(signal, "name", ""))
    score = float(_signal_value(signal, "score_total", 0.0) or 0.0)
    entry = _entry_price(signal, direction, config.slippage_points)

    if future_5m.empty:
        return TradeResult(
            signal_time=signal_time,
            entry_time=None,
            exit_time=None,
            direction=direction,
            setup_type=setup_type,
            signal_name=name,
            entry_price=entry,
            stop_loss=stop,
            take_profits=tps,
            exit_price=None,
            exit_reason="no_future",
            r_multiple=0.0,
            pnl_points=0.0,
            holding_bars=0,
            signal_score=score,
            metadata=_signal_metadata(signal),
        )

    risk = _risk_points(entry, stop, direction)
    if risk <= 0:
        return TradeResult(
            signal_time=signal_time,
            entry_time=None,
            exit_time=None,
            direction=direction,
            setup_type=setup_type,
            signal_name=name,
            entry_price=entry,
            stop_loss=stop,
            take_profits=tps,
            exit_price=None,
            exit_reason="not_triggered",
            r_multiple=0.0,
            pnl_points=0.0,
            holding_bars=0,
            signal_score=score,
            metadata={**_signal_metadata(signal), "invalid_risk": risk},
        )

    bars = future_5m.iloc[: config.max_holding_bars]
    entry_time: pd.Timestamp | None = None
    entry_offset = 0
    for offset, (ts, row) in enumerate(bars.iterrows()):
        if _entered(row, signal):
            entry_time = ts
            entry_offset = offset
            break

    if entry_time is None:
        return TradeResult(
            signal_time=signal_time,
            entry_time=None,
            exit_time=None,
            direction=direction,
            setup_type=setup_type,
            signal_name=name,
            entry_price=entry,
            stop_loss=stop,
            take_profits=tps,
            exit_price=None,
            exit_reason="not_triggered",
            r_multiple=0.0,
            pnl_points=0.0,
            holding_bars=len(bars),
            signal_score=score,
            metadata=_signal_metadata(signal),
        )

    active = bars.iloc[entry_offset:]
    for holding, (ts, row) in enumerate(active.iterrows(), start=1):
        stop_hit = _hit_stop(row, stop, direction)
        hit_index = next((i for i, tp in enumerate(tps, start=1) if _hit_tp(row, tp, direction)), None)
        if stop_hit and (hit_index is None or config.conservative_same_bar):
            pnl = _pnl_points(entry, stop, direction, config.fee_points)
            return TradeResult(
                signal_time=signal_time,
                entry_time=entry_time,
                exit_time=ts,
                direction=direction,
                setup_type=setup_type,
                signal_name=name,
                entry_price=entry,
                stop_loss=stop,
                take_profits=tps,
                exit_price=stop,
                exit_reason="stop",
                r_multiple=round(pnl / risk, 4),
                pnl_points=round(pnl, 4),
                holding_bars=holding,
                signal_score=score,
                metadata=_signal_metadata(signal),
            )
        if hit_index is not None:
            exit_price = tps[hit_index - 1]
            pnl = _pnl_points(entry, exit_price, direction, config.fee_points)
            return TradeResult(
                signal_time=signal_time,
                entry_time=entry_time,
                exit_time=ts,
                direction=direction,
                setup_type=setup_type,
                signal_name=name,
                entry_price=entry,
                stop_loss=stop,
                take_profits=tps,
                exit_price=exit_price,
                exit_reason=f"tp{hit_index}",  # type: ignore[arg-type]
                r_multiple=round(pnl / risk, 4),
                pnl_points=round(pnl, 4),
                holding_bars=holding,
                signal_score=score,
                metadata=_signal_metadata(signal),
            )

    last = active.iloc[-1]
    exit_price = float(last["Close"])
    pnl = _pnl_points(entry, exit_price, direction, config.fee_points)
    return TradeResult(
        signal_time=signal_time,
        entry_time=entry_time,
        exit_time=active.index[-1],
        direction=direction,
        setup_type=setup_type,
        signal_name=name,
        entry_price=entry,
        stop_loss=stop,
        take_profits=tps,
        exit_price=exit_price,
        exit_reason="timeout",
        r_multiple=round(pnl / risk, 4),
        pnl_points=round(pnl, 4),
        holding_bars=len(active),
        signal_score=score,
        metadata=_signal_metadata(signal),
    )
