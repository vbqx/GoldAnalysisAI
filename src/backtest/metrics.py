"""Performance statistics for backtest runs."""

from __future__ import annotations

from collections import defaultdict
from typing import Iterable

from src.backtest.types import TradeResult


def _max_drawdown(values: list[float]) -> float:
    equity = 0.0
    peak = 0.0
    max_dd = 0.0
    for value in values:
        equity += value
        peak = max(peak, equity)
        max_dd = min(max_dd, equity - peak)
    return round(max_dd, 4)


def summarize_trades(trades: list[TradeResult]) -> dict:
    triggered = [t for t in trades if t.triggered]
    closed = [t for t in triggered if t.exit_reason not in ("no_future", "not_triggered")]
    wins = [t for t in closed if t.r_multiple > 0]
    losses = [t for t in closed if t.r_multiple < 0]
    tp1 = [t for t in closed if t.exit_reason.startswith("tp")]
    gross_profit = sum(t.r_multiple for t in wins)
    gross_loss = abs(sum(t.r_multiple for t in losses))
    total_r = sum(t.r_multiple for t in closed)
    avg_win = gross_profit / len(wins) if wins else 0.0
    avg_loss = gross_loss / len(losses) if losses else 0.0
    win_rate = len(wins) / len(closed) if closed else 0.0
    loss_rate = len(losses) / len(closed) if closed else 0.0
    return {
        "signals": len(trades),
        "triggered": len(triggered),
        "closed": len(closed),
        "trigger_rate": round(len(triggered) / len(trades), 4) if trades else 0.0,
        "tp1_success_rate": round(len(tp1) / len(triggered), 4) if triggered else 0.0,
        "win_rate": round(win_rate, 4),
        "total_r": round(total_r, 4),
        "avg_r": round(total_r / len(closed), 4) if closed else 0.0,
        "profit_factor": round(gross_profit / gross_loss, 4) if gross_loss else (round(gross_profit, 4) if gross_profit else 0.0),
        "expectancy_r": round(win_rate * avg_win - loss_rate * avg_loss, 4) if closed else 0.0,
        "max_drawdown_r": _max_drawdown([t.r_multiple for t in closed]),
        "avg_holding_bars": round(sum(t.holding_bars for t in closed) / len(closed), 2) if closed else 0.0,
    }


def group_trades(trades: Iterable[TradeResult], key: str) -> list[dict]:
    buckets: dict[str, list[TradeResult]] = defaultdict(list)
    for trade in trades:
        buckets[str(getattr(trade, key) or "unknown")].append(trade)
    rows = []
    for label, items in sorted(buckets.items()):
        stats = summarize_trades(items)
        rows.append({"bucket": label, **stats})
    return rows
