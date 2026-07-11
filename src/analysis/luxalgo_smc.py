"""LuxAlgo Smart Money Concepts — Python port of detection rules.

Reference: LuxAlgo SMC Pine (CC BY-NC-SA 4.0). Defaults match indicator inputs:
- Swing structure size 50, internal 5, equal H/L length 3
- FVG auto threshold, OB ATR(200) filter, High/Low mitigation
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

import numpy as np
import pandas as pd

from src.analysis.ict_pa import (
    FairValueGap,
    LiquidityZone,
    OrderBlock,
    StructureEvent,
    SwingPoint,
    Trend,
)

BULLISH = 1
BEARISH = 0

SWING_STRUCTURE_SIZE = 50
INTERNAL_STRUCTURE_SIZE = 5
INTERNAL_FILTER_CONFLUENCE = False  # Lux Pine default: Confluence Filter = off
EQUAL_HL_SIZE = 3
EQUAL_HL_THRESHOLD = 0.1
ATR_OB_PERIOD = 200
MAX_STORED_OBS = 100
MAX_OBS_OUTPUT = 5
MAX_FVG_OUTPUT = 50


@dataclass
class _Pivot:
    current_level: float | None = None
    last_level: float | None = None
    crossed: bool = False
    bar_index: int = 0
    bar_time: pd.Timestamp | None = None


@dataclass
class _Trailing:
    top: float | None = None
    bottom: float | None = None
    bar_time: pd.Timestamp | None = None


@dataclass
class LuxAlgoResult:
    swings: list[SwingPoint] = field(default_factory=list)
    trend: Trend = "ranging"
    events: list[StructureEvent] = field(default_factory=list)
    order_blocks: list[OrderBlock] = field(default_factory=list)
    internal_order_blocks: list[OrderBlock] = field(default_factory=list)
    fvgs: list[FairValueGap] = field(default_factory=list)
    active_fvgs: list[FairValueGap] = field(default_factory=list)
    liquidity: list[LiquidityZone] = field(default_factory=list)
    swing_high: float | None = None
    swing_low: float | None = None
    trailing_top: float | None = None
    trailing_bottom: float | None = None


def _true_range(high: np.ndarray, low: np.ndarray, close: np.ndarray) -> np.ndarray:
    n = len(close)
    tr = np.empty(n)
    tr[0] = high[0] - low[0]
    for i in range(1, n):
        tr[i] = max(high[i] - low[i], abs(high[i] - close[i - 1]), abs(low[i] - close[i - 1]))
    return tr


def _atr_series(high: np.ndarray, low: np.ndarray, close: np.ndarray, period: int) -> np.ndarray:
    tr = _true_range(high, low, close)
    out = np.full(len(close), np.nan)
    if len(close) < period:
        return out
    for i in range(period - 1, len(close)):
        out[i] = float(np.mean(tr[i - period + 1 : i + 1]))
    return out


def _leg_at_bar(highs: np.ndarray, lows: np.ndarray, i: int, size: int, prev_leg: int) -> int:
    if i < size:
        return prev_leg
    ref = i - size
    window_high = float(np.max(highs[i - size + 1 : i + 1]))
    window_low = float(np.min(lows[i - size + 1 : i + 1]))
    if highs[ref] > window_high:
        return BEARISH
    if lows[ref] < window_low:
        return BULLISH
    return prev_leg


def _parsed_bar(high: float, low: float, vol: float) -> tuple[float, float]:
    if vol > 0 and (high - low) >= 2 * vol:
        return low, high
    return high, low


def _fvg_threshold(cum_abs_delta: float, bar_index: int) -> float:
    if bar_index <= 0:
        return 0.0
    return (cum_abs_delta / bar_index) * 2.0


def _store_order_block(
    parsed_highs: list[float],
    parsed_lows: list[float],
    times: list[pd.Timestamp],
    pivot_index: int,
    current_index: int,
    bias: Literal["bullish", "bearish"],
) -> OrderBlock | None:
    if pivot_index < 0 or current_index <= pivot_index:
        return None
    if bias == "bearish":
        segment = parsed_highs[pivot_index:current_index]
        if not segment:
            return None
        rel = int(np.argmax(segment))
        idx = pivot_index + rel
    else:
        segment = parsed_lows[pivot_index:current_index]
        if not segment:
            return None
        rel = int(np.argmin(segment))
        idx = pivot_index + rel
    return OrderBlock(
        high=float(parsed_highs[idx]),
        low=float(parsed_lows[idx]),
        direction=bias,
        time=times[idx],
    )


def _mitigate_obs(
    obs: list[OrderBlock],
    high: float,
    low: float,
) -> list[OrderBlock]:
    kept: list[OrderBlock] = []
    for ob in obs:
        if ob.direction == "bearish" and high > ob.high:
            continue
        if ob.direction == "bullish" and low < ob.low:
            continue
        kept.append(ob)
    return kept


def _mitigate_fvgs(
    fvgs: list[FairValueGap],
    high: float,
    low: float,
) -> list[FairValueGap]:
    kept: list[FairValueGap] = []
    for fvg in fvgs:
        if fvg.direction == "bullish" and low < fvg.low:
            continue
        if fvg.direction == "bearish" and high > fvg.high:
            continue
        kept.append(fvg)
    return kept


def _crossover(close_prev: float, close_curr: float, level: float) -> bool:
    return close_curr > level and close_prev <= level


def _crossunder(close_prev: float, close_curr: float, level: float) -> bool:
    return close_curr < level and close_prev >= level


def _internal_confluence_bars(
    open_: float, high: float, low: float, close: float,
) -> tuple[bool, bool]:
    """Lux internalFilterConfluence: wick dominance on the signal bar."""
    body_top = max(close, open_)
    body_bot = min(close, open_)
    upper_wick = high - body_top
    lower_wick = body_bot - low
    bullish_bar = lower_wick > upper_wick
    bearish_bar = upper_wick > lower_wick
    return bullish_bar, bearish_bar


def _append_structure_event(
    events: list[StructureEvent],
    *,
    tag: Literal["BOS", "CHoCH"],
    direction: Literal["bullish", "bearish"],
    level: float,
    bar_time: pd.Timestamp,
    pivot_time: pd.Timestamp | None,
    scope: Literal["internal", "swing"],
) -> None:
    events.append(
        StructureEvent(
            tag,
            direction,
            level,
            bar_time,
            pivot_time=pivot_time,
            scope=scope,
        )
    )


def _update_structure_pivots(
    *,
    size: int,
    leg_prev: int,
    leg_curr: int,
    highs: np.ndarray,
    lows: np.ndarray,
    index: pd.DatetimeIndex,
    i: int,
    pivot_high: _Pivot,
    pivot_low: _Pivot,
    trailing: _Trailing | None,
    swings: list[SwingPoint],
    equal_mode: bool,
    atr_measure: float,
    equal_prev_low: _Pivot,
    equal_prev_high: _Pivot,
    liquidity: list[LiquidityZone],
) -> None:
    if leg_prev == leg_curr or i < size:
        return
    ref = i - size
    ts = index[ref]

    if leg_curr == BULLISH and leg_prev == BEARISH:
        level = float(lows[ref])
        if equal_mode and equal_prev_low.current_level is not None:
            if abs(equal_prev_low.current_level - level) < EQUAL_HL_THRESHOLD * atr_measure:
                pass  # EQH/EQL not exported — use swing H/L downstream
        equal_prev_low.last_level = equal_prev_low.current_level
        equal_prev_low.current_level = level
        equal_prev_low.bar_index = ref
        equal_prev_low.bar_time = ts
        equal_prev_low.crossed = False

        if not equal_mode:
            pivot_low.last_level = pivot_low.current_level
            pivot_low.current_level = level
            pivot_low.bar_index = ref
            pivot_low.bar_time = ts
            pivot_low.crossed = False
            swings.append(SwingPoint(ref, level, "low", ts))
            if trailing is not None:
                trailing.bottom = level
                trailing.bar_time = ts

    elif leg_curr == BEARISH and leg_prev == BULLISH:
        level = float(highs[ref])
        if equal_mode and equal_prev_high.current_level is not None:
            if abs(equal_prev_high.current_level - level) < EQUAL_HL_THRESHOLD * atr_measure:
                pass  # EQH/EQL not exported — use swing H/L downstream
        equal_prev_high.last_level = equal_prev_high.current_level
        equal_prev_high.current_level = level
        equal_prev_high.bar_index = ref
        equal_prev_high.bar_time = ts
        equal_prev_high.crossed = False

        if not equal_mode:
            pivot_high.last_level = pivot_high.current_level
            pivot_high.current_level = level
            pivot_high.bar_index = ref
            pivot_high.bar_time = ts
            pivot_high.crossed = False
            swings.append(SwingPoint(ref, level, "high", ts))
            if trailing is not None:
                trailing.top = level
                trailing.bar_time = ts


def _push_ob(blocks: list[OrderBlock], ob: OrderBlock | None) -> None:
    if ob is None:
        return
    if len(blocks) >= MAX_STORED_OBS:
        blocks.pop()
    blocks.insert(0, ob)


def analyze_luxalgo(df: pd.DataFrame) -> LuxAlgoResult:
    """Run LuxAlgo SMC detection over OHLC bars."""
    if len(df) < 3:
        return LuxAlgoResult()

    index = df.index
    opens = df["Open"].astype(float).values
    highs = df["High"].astype(float).values
    lows = df["Low"].astype(float).values
    closes = df["Close"].astype(float).values
    n = len(df)

    atr200 = _atr_series(highs, lows, closes, ATR_OB_PERIOD)
    parsed_highs: list[float] = []
    parsed_lows: list[float] = []
    times: list[pd.Timestamp] = []

    swing_high = _Pivot()
    swing_low = _Pivot()
    internal_high = _Pivot()
    internal_low = _Pivot()
    equal_high = _Pivot()
    equal_low = _Pivot()
    trailing = _Trailing()
    swing_trend = 0
    internal_trend = 0

    swing_leg = 0
    internal_leg = 0
    equal_leg = 0

    swings: list[SwingPoint] = []
    events: list[StructureEvent] = []
    liquidity: list[LiquidityZone] = []
    swing_obs: list[OrderBlock] = []
    internal_obs: list[OrderBlock] = []
    fvgs: list[FairValueGap] = []

    cum_abs_delta = 0.0

    for i in range(n):
        vol = float(atr200[i]) if not np.isnan(atr200[i]) else 0.0
        ph, pl = _parsed_bar(float(highs[i]), float(lows[i]), vol)
        parsed_highs.append(ph)
        parsed_lows.append(pl)
        times.append(index[i])

        if i >= 1:
            bar_delta = (closes[i - 1] - opens[i - 1]) / (opens[i - 1] * 100) if opens[i - 1] else 0.0
            cum_abs_delta += abs(bar_delta)

        swing_leg_prev = swing_leg
        internal_leg_prev = internal_leg
        equal_leg_prev = equal_leg

        swing_leg = _leg_at_bar(highs, lows, i, SWING_STRUCTURE_SIZE, swing_leg)
        internal_leg = _leg_at_bar(highs, lows, i, INTERNAL_STRUCTURE_SIZE, internal_leg)
        equal_leg = _leg_at_bar(highs, lows, i, EQUAL_HL_SIZE, equal_leg)

        if vol > 0:
            atr_m = vol
        else:
            slice_atr = atr200[max(0, i - 20) : i + 1]
            valid_atr = slice_atr[~np.isnan(slice_atr)]
            atr_m = float(np.mean(valid_atr)) if len(valid_atr) else 1.0

        _update_structure_pivots(
            size=SWING_STRUCTURE_SIZE,
            leg_prev=swing_leg_prev,
            leg_curr=swing_leg,
            highs=highs,
            lows=lows,
            index=index,
            i=i,
            pivot_high=swing_high,
            pivot_low=swing_low,
            trailing=trailing,
            swings=swings,
            equal_mode=False,
            atr_measure=atr_m,
            equal_prev_low=equal_low,
            equal_prev_high=equal_high,
            liquidity=liquidity,
        )
        _update_structure_pivots(
            size=INTERNAL_STRUCTURE_SIZE,
            leg_prev=internal_leg_prev,
            leg_curr=internal_leg,
            highs=highs,
            lows=lows,
            index=index,
            i=i,
            pivot_high=internal_high,
            pivot_low=internal_low,
            trailing=None,
            swings=swings,
            equal_mode=False,
            atr_measure=atr_m,
            equal_prev_low=equal_low,
            equal_prev_high=equal_high,
            liquidity=liquidity,
        )
        _update_structure_pivots(
            size=EQUAL_HL_SIZE,
            leg_prev=equal_leg_prev,
            leg_curr=equal_leg,
            highs=highs,
            lows=lows,
            index=index,
            i=i,
            pivot_high=equal_high,
            pivot_low=equal_low,
            trailing=None,
            swings=swings,
            equal_mode=True,
            atr_measure=atr_m,
            equal_prev_low=equal_low,
            equal_prev_high=equal_high,
            liquidity=liquidity,
        )

        if i >= 2:
            threshold = _fvg_threshold(cum_abs_delta, i)
            last_close = closes[i - 1]
            last_open = opens[i - 1]
            last2_high = highs[i - 2]
            last2_low = lows[i - 2]
            bar_delta_pct = (last_close - last_open) / (last_open * 100) if last_open else 0.0

            if (
                lows[i] > last2_high
                and last_close > last2_high
                and bar_delta_pct > threshold
            ):
                fvgs.insert(
                    0,
                    FairValueGap(
                        high=float(lows[i]),
                        low=float(last2_high),
                        direction="bullish",
                        time=index[i],
                    ),
                )
            if (
                highs[i] < last2_low
                and last_close < last2_low
                and -bar_delta_pct > threshold
            ):
                fvgs.insert(
                    0,
                    FairValueGap(
                        high=float(last2_low),
                        low=float(highs[i]),
                        direction="bearish",
                        time=index[i],
                    ),
                )

        close_prev = closes[i - 1] if i >= 1 else closes[i]
        close_curr = closes[i]

        if swing_high.current_level is not None and not swing_high.crossed:
            if _crossover(close_prev, close_curr, swing_high.current_level):
                tag: Literal["BOS", "CHoCH"] = "CHoCH" if swing_trend == BEARISH else "BOS"
                _append_structure_event(
                    events,
                    tag=tag,
                    direction="bullish",
                    level=swing_high.current_level,
                    bar_time=index[i],
                    pivot_time=swing_high.bar_time,
                    scope="swing",
                )
                swing_high.crossed = True
                swing_trend = BULLISH
                _push_ob(
                    swing_obs,
                    _store_order_block(
                        parsed_highs, parsed_lows, times,
                        swing_high.bar_index, i, "bullish",
                    ),
                )
        if swing_low.current_level is not None and not swing_low.crossed:
            if _crossunder(close_prev, close_curr, swing_low.current_level):
                tag = "CHoCH" if swing_trend == BULLISH else "BOS"
                _append_structure_event(
                    events,
                    tag=tag,
                    direction="bearish",
                    level=swing_low.current_level,
                    bar_time=index[i],
                    pivot_time=swing_low.bar_time,
                    scope="swing",
                )
                swing_low.crossed = True
                swing_trend = BEARISH
                _push_ob(
                    swing_obs,
                    _store_order_block(
                        parsed_highs, parsed_lows, times,
                        swing_low.bar_index, i, "bearish",
                    ),
                )

        bullish_bar, bearish_bar = True, True
        if INTERNAL_FILTER_CONFLUENCE:
            bullish_bar, bearish_bar = _internal_confluence_bars(
                float(opens[i]), float(highs[i]), float(lows[i]), float(closes[i]),
            )

        if internal_high.current_level is not None and not internal_high.crossed:
            internal_extra = (
                swing_high.current_level is None
                or internal_high.current_level != swing_high.current_level
            )
            if INTERNAL_FILTER_CONFLUENCE:
                internal_extra = internal_extra and bullish_bar
            if internal_extra and _crossover(close_prev, close_curr, internal_high.current_level):
                tag_i: Literal["BOS", "CHoCH"] = "CHoCH" if internal_trend == BEARISH else "BOS"
                _append_structure_event(
                    events,
                    tag=tag_i,
                    direction="bullish",
                    level=internal_high.current_level,
                    bar_time=index[i],
                    pivot_time=internal_high.bar_time,
                    scope="internal",
                )
                internal_high.crossed = True
                internal_trend = BULLISH
                _push_ob(
                    internal_obs,
                    _store_order_block(
                        parsed_highs, parsed_lows, times,
                        internal_high.bar_index, i, "bullish",
                    ),
                )
        if internal_low.current_level is not None and not internal_low.crossed:
            internal_extra = (
                swing_low.current_level is None
                or internal_low.current_level != swing_low.current_level
            )
            if INTERNAL_FILTER_CONFLUENCE:
                internal_extra = internal_extra and bearish_bar
            if internal_extra and _crossunder(close_prev, close_curr, internal_low.current_level):
                tag_i = "CHoCH" if internal_trend == BULLISH else "BOS"
                _append_structure_event(
                    events,
                    tag=tag_i,
                    direction="bearish",
                    level=internal_low.current_level,
                    bar_time=index[i],
                    pivot_time=internal_low.bar_time,
                    scope="internal",
                )
                internal_low.crossed = True
                internal_trend = BEARISH
                _push_ob(
                    internal_obs,
                    _store_order_block(
                        parsed_highs, parsed_lows, times,
                        internal_low.bar_index, i, "bearish",
                    ),
                )

        swing_obs = _mitigate_obs(swing_obs, float(highs[i]), float(lows[i]))
        internal_obs = _mitigate_obs(internal_obs, float(highs[i]), float(lows[i]))
        fvgs = _mitigate_fvgs(fvgs, float(highs[i]), float(lows[i]))

    if swing_trend == BULLISH:
        trend: Trend = "bullish"
    elif swing_trend == BEARISH:
        trend = "bearish"
    else:
        trend = "ranging"

    active_fvgs = list(fvgs)
    # Lux default: internal OBs for chart/LLM; fall back to swing when none remain.
    primary_obs = internal_obs[:MAX_OBS_OUTPUT] or swing_obs[:MAX_OBS_OUTPUT]

    return LuxAlgoResult(
        swings=sorted(swings, key=lambda s: s.index),
        trend=trend,
        events=events,
        order_blocks=primary_obs,
        internal_order_blocks=internal_obs[:MAX_OBS_OUTPUT],
        fvgs=fvgs[:MAX_FVG_OUTPUT],
        active_fvgs=active_fvgs[:MAX_FVG_OUTPUT],
        liquidity=liquidity,
        swing_high=swing_high.current_level,
        swing_low=swing_low.current_level,
        trailing_top=trailing.top,
        trailing_bottom=trailing.bottom,
    )
