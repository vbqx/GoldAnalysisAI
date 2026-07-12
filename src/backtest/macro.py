"""Historical macro replay helpers for backtests."""

from __future__ import annotations

import pandas as pd

from src.backtest.types import MacroReplayState


def fetch_historical_dxy(n_bars: int = 1500) -> pd.DataFrame:
    """Fetch DXY daily history once for a backtest run."""
    from tvDatafeed import Interval

    from src.config import TV_DXY_EXCHANGE, TV_DXY_SYMBOL
    from src.data.tradingview import _fetch_bars

    return _fetch_bars(
        Interval.in_daily,
        n_bars=n_bars,
        label="DXY historical",
        exchange=TV_DXY_EXCHANGE,
        symbol=TV_DXY_SYMBOL,
        report_progress=False,
    )


def normalize_macro_ohlcv(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    rename = {
        "open": "Open",
        "high": "High",
        "low": "Low",
        "close": "Close",
        "volume": "Volume",
        "datetime": "Datetime",
        "time": "Datetime",
        "timestamp": "Datetime",
    }
    out = out.rename(columns={k: v for k, v in rename.items() if k in out.columns})
    if "Datetime" in out.columns:
        out.index = pd.to_datetime(out.pop("Datetime"), utc=True)
    else:
        out.index = pd.to_datetime(out.index, utc=True)
    if "Close" not in out.columns:
        raise ValueError("Macro data missing Close column")
    return out.sort_index()


def macro_state_at(dxy_daily: pd.DataFrame | None, timestamp: pd.Timestamp) -> MacroReplayState:
    ts = pd.Timestamp(timestamp)
    if ts.tzinfo is None:
        ts = ts.tz_localize("UTC")
    else:
        ts = ts.tz_convert("UTC")

    if dxy_daily is None or dxy_daily.empty:
        return MacroReplayState(
            time=ts,
            dxy_time=None,
            dxy_close=None,
            dxy_change_1d=None,
            dxy_change_5d=None,
            dxy_change_20d=None,
            gold_bias="neutral",
            confidence=0.0,
            source="missing_dxy",
        )

    dxy = normalize_macro_ohlcv(dxy_daily)
    # Daily bars are indexed at day open; intraday replay must not use the current day's close.
    day_start = ts.floor("D")
    if ts > day_start:
        hist = dxy.loc[dxy.index < day_start]
    else:
        hist = dxy.loc[dxy.index < ts]
    if len(hist) < 2:
        return MacroReplayState(
            time=ts,
            dxy_time=hist.index[-1] if len(hist) else None,
            dxy_close=float(hist["Close"].iloc[-1]) if len(hist) else None,
            dxy_change_1d=None,
            dxy_change_5d=None,
            dxy_change_20d=None,
            gold_bias="neutral",
            confidence=0.0,
        )

    close = float(hist["Close"].iloc[-1])

    def pct_change(periods: int) -> float | None:
        if len(hist) <= periods:
            return None
        prev = float(hist["Close"].iloc[-1 - periods])
        return ((close - prev) / prev) * 100 if prev else None

    change_1d = pct_change(1)
    change_5d = pct_change(5)
    change_20d = pct_change(20)
    score = 0.0
    if change_1d is not None:
        if change_1d > 0.25:
            score -= 0.45
        elif change_1d < -0.25:
            score += 0.45
    if change_5d is not None:
        if change_5d > 0.50:
            score -= 0.35
        elif change_5d < -0.50:
            score += 0.35
    if change_20d is not None:
        if change_20d > 1.00:
            score -= 0.20
        elif change_20d < -1.00:
            score += 0.20

    if score > 0.20:
        bias = "bullish"
    elif score < -0.20:
        bias = "bearish"
    else:
        bias = "neutral"

    return MacroReplayState(
        time=ts,
        dxy_time=hist.index[-1],
        dxy_close=round(close, 4),
        dxy_change_1d=round(change_1d, 4) if change_1d is not None else None,
        dxy_change_5d=round(change_5d, 4) if change_5d is not None else None,
        dxy_change_20d=round(change_20d, 4) if change_20d is not None else None,
        gold_bias=bias,
        confidence=round(min(abs(score), 1.0), 4),
    )


def apply_macro_to_signals(signals: list, state: MacroReplayState, weight: float) -> list:
    if not signals or state.gold_bias == "neutral" or state.confidence <= 0 or weight <= 0:
        return signals
    adjustment = weight * 100 * state.confidence
    for signal in signals:
        direction = getattr(signal, "direction", "")
        aligned = (
            (direction == "BUY" and state.gold_bias == "bullish")
            or (direction == "SELL" and state.gold_bias == "bearish")
        )
        delta = adjustment if aligned else -adjustment
        base = float(getattr(signal, "score_total", 0.0) or 0.0)
        signal.score_total = round(max(0.0, min(100.0, base + delta)), 1)
        signal.score_grade = _grade(signal.score_total)
        signal.score_reasons.append(
            f"DXY macro {state.gold_bias} ({state.confidence:.2f}) {'+' if delta >= 0 else ''}{delta:.1f}"
        )
        setattr(signal, "macro_bias", state.gold_bias)
        setattr(signal, "macro_confidence", state.confidence)
        setattr(signal, "macro_score_delta", round(delta, 4))
        setattr(signal, "macro_dxy_time", str(state.dxy_time) if state.dxy_time is not None else "")
    return sorted(signals, key=lambda s: float(getattr(s, "score_total", 0.0) or 0.0), reverse=True)


def _grade(score: float) -> str:
    if score >= 80:
        return "A"
    if score >= 65:
        return "B"
    if score >= 50:
        return "C"
    return "D"
