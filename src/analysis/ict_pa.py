"""ICT / Price Action structure detection (simplified MVP rules)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

import numpy as np
import pandas as pd

Trend = Literal["bullish", "bearish", "ranging"]


@dataclass
class SwingPoint:
    index: int
    price: float
    kind: Literal["high", "low"]
    time: pd.Timestamp


@dataclass
class OrderBlock:
    high: float
    low: float
    direction: Literal["bullish", "bearish"]
    time: pd.Timestamp
    label: str = "OB"


@dataclass
class FairValueGap:
    high: float
    low: float
    direction: Literal["bullish", "bearish"]
    time: pd.Timestamp
    label: str = "FVG"


@dataclass
class LiquidityZone:
    price: float
    kind: str
    label: str
    strength: float = 0.5
    swept: bool = False


@dataclass
class StructureEvent:
    kind: Literal["BOS", "CHoCH"]
    direction: Literal["bullish", "bearish"]
    price: float
    time: pd.Timestamp


@dataclass
class TimeframeAnalysis:
    timeframe: str
    trend: Trend
    bos: str
    choch: str
    order_blocks: list[OrderBlock] = field(default_factory=list)
    fvgs: list[FairValueGap] = field(default_factory=list)
    active_fvgs: list[FairValueGap] = field(default_factory=list)
    liquidity: list[LiquidityZone] = field(default_factory=list)
    swing_high: float | None = None
    swing_low: float | None = None
    events: list[StructureEvent] = field(default_factory=list)
    premium_discount: str = "unknown"
    equilibrium: float | None = None
    volume_signal: str = "N/A"
    atr: float | None = None
    last_close: float | None = None
    recent_high: float | None = None
    recent_low: float | None = None


def _find_swings(df: pd.DataFrame, left: int = 3, right: int = 3) -> list[SwingPoint]:
    swings: list[SwingPoint] = []
    highs = df["High"].values
    lows = df["Low"].values
    n = len(df)

    for i in range(left, n - right):
        if highs[i] == max(highs[i - left : i + right + 1]):
            swings.append(SwingPoint(i, float(highs[i]), "high", df.index[i]))
        if lows[i] == min(lows[i - left : i + right + 1]):
            swings.append(SwingPoint(i, float(lows[i]), "low", df.index[i]))
    return sorted(swings, key=lambda s: s.index)


def _infer_trend(swings: list[SwingPoint]) -> Trend:
    highs = [s for s in swings if s.kind == "high"][-3:]
    lows = [s for s in swings if s.kind == "low"][-3:]
    if len(highs) < 2 or len(lows) < 2:
        return "ranging"

    hh = highs[-1].price > highs[-2].price
    hl = lows[-1].price > lows[-2].price
    lh = highs[-1].price < highs[-2].price
    ll = lows[-1].price < lows[-2].price

    if hh and hl:
        return "bullish"
    if lh and ll:
        return "bearish"
    return "ranging"


def _detect_structure_events(df: pd.DataFrame, swings: list[SwingPoint], trend: Trend) -> list[StructureEvent]:
    events: list[StructureEvent] = []
    if len(swings) < 4:
        return events

    recent = swings[-6:]
    close = float(df["Close"].iloc[-1])

    last_highs = [s for s in recent if s.kind == "high"]
    last_lows = [s for s in recent if s.kind == "low"]

    if len(last_highs) >= 2:
        prev_h = last_highs[-2].price
        if close > prev_h:
            kind: Literal["BOS", "CHoCH"] = "CHoCH" if trend == "bearish" else "BOS"
            events.append(StructureEvent(kind, "bullish", prev_h, df.index[-1]))

    if len(last_lows) >= 2:
        prev_l = last_lows[-2].price
        if close < prev_l:
            kind = "CHoCH" if trend == "bullish" else "BOS"
            events.append(StructureEvent(kind, "bearish", prev_l, df.index[-1]))

    return events


def _detect_fvgs(df: pd.DataFrame, lookback: int = 80) -> list[FairValueGap]:
    fvgs: list[FairValueGap] = []
    start = max(2, len(df) - lookback)
    for i in range(start, len(df)):
        c1 = df.iloc[i - 2]
        c3 = df.iloc[i]
        # Bearish FVG: gap between candle 1 low and candle 3 high (price moved down leaving gap)
        if c1["Low"] > c3["High"]:
            fvgs.append(
                FairValueGap(
                    high=float(c1["Low"]),
                    low=float(c3["High"]),
                    direction="bearish",
                    time=df.index[i],
                )
            )
        # Bullish FVG
        if c1["High"] < c3["Low"]:
            fvgs.append(
                FairValueGap(
                    high=float(c3["Low"]),
                    low=float(c1["High"]),
                    direction="bullish",
                    time=df.index[i],
                )
            )
    return fvgs[-5:]


def _detect_order_blocks(df: pd.DataFrame, swings: list[SwingPoint], lookback: int = 60) -> list[OrderBlock]:
    """OB = last opposing candle before impulsive move (MVP heuristic)."""
    obs: list[OrderBlock] = []
    if len(df) < 5:
        return obs

    subset = df.iloc[-lookback:]
    for i in range(2, len(subset) - 1):
        prev = subset.iloc[i - 1]
        curr = subset.iloc[i]
        nxt = subset.iloc[i + 1]

        body_prev = abs(prev["Close"] - prev["Open"])
        body_curr = abs(curr["Close"] - curr["Open"])
        body_nxt = abs(nxt["Close"] - nxt["Open"])

        # Bearish OB: strong down move after bullish candle
        if (
            prev["Close"] > prev["Open"]
            and curr["Close"] < curr["Open"]
            and body_nxt > body_curr * 1.2
            and nxt["Close"] < prev["Low"]
        ):
            obs.append(
                OrderBlock(
                    high=float(prev["High"]),
                    low=float(prev["Low"]),
                    direction="bearish",
                    time=subset.index[i - 1],
                )
            )

        # Bullish OB
        if (
            prev["Close"] < prev["Open"]
            and curr["Close"] > curr["Open"]
            and body_nxt > body_curr * 1.2
            and nxt["Close"] > prev["High"]
        ):
            obs.append(
                OrderBlock(
                    high=float(prev["High"]),
                    low=float(prev["Low"]),
                    direction="bullish",
                    time=subset.index[i - 1],
                )
            )

    return obs[-4:]


def _liquidity_from_swings(
    swings: list[SwingPoint],
    *,
    price: float | None = None,
    atr: float | None = None,
    recent_high: float | None = None,
    recent_low: float | None = None,
) -> list[LiquidityZone]:
    zones: list[LiquidityZone] = []
    highs = [s for s in swings if s.kind == "high"]
    lows = [s for s in swings if s.kind == "low"]
    reference_price = price or (swings[-1].price if swings else 0)
    atr_value = atr if atr and atr > 0 else None
    equal_tol = max((atr_value or 0) * 0.15, reference_price * 0.0005 if reference_price else 0.5)
    stop_offset = max((atr_value or 0) * 0.25, 2.0)

    if len(highs) >= 2:
        distance = abs(highs[-1].price - highs[-2].price)
        if distance <= equal_tol:
            strength = max(0.35, min(1.0, 1 - distance / max(equal_tol, 0.01)))
            swept_line = max(highs[-1].price, highs[-2].price) + equal_tol * 0.5
            swept = recent_high is not None and recent_high > swept_line
            zones.append(
                LiquidityZone(
                    highs[-1].price,
                    "equal_highs",
                    "Equal Highs / Sell-side Liquidity",
                    round(strength, 2),
                    swept,
                )
            )

    if len(lows) >= 2:
        distance = abs(lows[-1].price - lows[-2].price)
        if distance <= equal_tol:
            strength = max(0.35, min(1.0, 1 - distance / max(equal_tol, 0.01)))
            swept_line = min(lows[-1].price, lows[-2].price) - equal_tol * 0.5
            swept = recent_low is not None and recent_low < swept_line
            zones.append(
                LiquidityZone(
                    lows[-1].price,
                    "equal_lows",
                    "Equal Lows / Buy-side Liquidity",
                    round(strength, 2),
                    swept,
                )
            )

    if highs:
        sweep_price = highs[-1].price + stop_offset
        swept = recent_high is not None and recent_high >= sweep_price
        zones.append(LiquidityZone(round(sweep_price, 2), "stop_hunt_high", "Stop Hunt Above Highs", 0.55, swept))
    if lows:
        sweep_price = lows[-1].price - stop_offset
        swept = recent_low is not None and recent_low <= sweep_price
        zones.append(LiquidityZone(round(sweep_price, 2), "stop_hunt_low", "Stop Hunt Below Lows", 0.55, swept))

    return zones


def _is_fvg_filled(df: pd.DataFrame, fvg: FairValueGap) -> bool:
    """True if price later traded through the gap zone."""
    try:
        loc = df.index.get_indexer([fvg.time], method="nearest")[0]
    except Exception:
        return False
    if loc < 0 or loc >= len(df) - 1:
        return False
    later = df.iloc[loc + 1 :]
    if later.empty:
        return False
    if fvg.direction == "bearish":
        return bool((later["High"] >= fvg.low).any())
    return bool((later["Low"] <= fvg.high).any())


def _active_fvgs(df: pd.DataFrame, fvgs: list[FairValueGap]) -> list[FairValueGap]:
    return [f for f in fvgs if not _is_fvg_filled(df, f)]


def _premium_discount(
    swing_high: float | None, swing_low: float | None, price: float
) -> tuple[str, float | None]:
    if swing_high is None or swing_low is None or swing_high <= swing_low:
        return "unknown", None
    eq = (swing_high + swing_low) / 2
    if price > eq * 1.001:
        return "premium", eq
    if price < eq * 0.999:
        return "discount", eq
    return "equilibrium", eq


def _recent_swing_range(swings: list[SwingPoint], *, per_side: int = 2) -> tuple[float | None, float | None]:
    """Use recent structure bounds instead of stale full-window extremes."""
    if not swings:
        return None, None
    highs = [s.price for s in swings if s.kind == "high"][-per_side:]
    lows = [s.price for s in swings if s.kind == "low"][-per_side:]
    if not highs:
        highs = [s.price for s in swings if s.kind == "high"]
    if not lows:
        lows = [s.price for s in swings if s.kind == "low"]
    return (max(highs) if highs else None, min(lows) if lows else None)


def _volume_signal(df: pd.DataFrame) -> str:
    if "Volume" not in df.columns or len(df) < 21:
        return "N/A"
    vol = df["Volume"].astype(float)
    avg = float(vol.iloc[-21:-1].mean())
    last = float(vol.iloc[-1])
    if avg <= 0:
        return "N/A"
    ratio = last / avg
    if ratio > 1.5:
        return f"放量 {ratio:.1f}x — 聪明钱可能活跃"
    if ratio < 0.5:
        return f"缩量 {ratio:.1f}x"
    return f"正常 {ratio:.1f}x"


def _last_numeric(df: pd.DataFrame, column: str) -> float | None:
    if column not in df.columns or df.empty:
        return None
    value = df[column].iloc[-1]
    if pd.isna(value):
        return None
    return float(value)


def analyze_timeframe(df: pd.DataFrame, timeframe: str) -> TimeframeAnalysis:
    swings = _find_swings(df)
    trend = _infer_trend(swings)
    events = _detect_structure_events(df, swings, trend)
    fvgs = _detect_fvgs(df)
    obs = _detect_order_blocks(df, swings)

    bos_status = "无"
    choch_status = "无"
    for e in events:
        label = f"{e.direction} @ {e.price:.2f}"
        if e.kind == "BOS":
            bos_status = label
        else:
            choch_status = label

    swing_high, swing_low = _recent_swing_range(swings)
    price = float(df["Close"].iloc[-1])
    recent = df.iloc[-5:] if len(df) >= 5 else df
    atr = _last_numeric(df, "ATR14")
    recent_high = float(recent["High"].max()) if not recent.empty else None
    recent_low = float(recent["Low"].min()) if not recent.empty else None
    pd_zone, eq = _premium_discount(swing_high, swing_low, price)

    return TimeframeAnalysis(
        timeframe=timeframe,
        trend=trend,
        bos=bos_status,
        choch=choch_status,
        order_blocks=obs,
        fvgs=fvgs,
        active_fvgs=_active_fvgs(df, fvgs),
        liquidity=_liquidity_from_swings(
            swings,
            price=price,
            atr=atr,
            recent_high=recent_high,
            recent_low=recent_low,
        ),
        swing_high=swing_high,
        swing_low=swing_low,
        events=events,
        premium_discount=pd_zone,
        equilibrium=eq,
        volume_signal=_volume_signal(df),
        atr=atr,
        last_close=price,
        recent_high=recent_high,
        recent_low=recent_low,
    )


def sentiment_score(analyses: dict[str, TimeframeAnalysis]) -> dict[str, float]:
    """Weighted bear/bull/range probabilities."""
    weights = {"1d": 0.20, "4h": 0.30, "1h": 0.25, "15m": 0.15, "5m": 0.10}
    bull = bear = neutral = 0.0

    for tf, weight in weights.items():
        if tf not in analyses:
            continue
        t = analyses[tf].trend
        if t == "bullish":
            bull += weight
        elif t == "bearish":
            bear += weight
        else:
            neutral += weight

    total = bull + bear + neutral or 1.0
    return {
        "bullish": round(bull / total * 100, 1),
        "bearish": round(bear / total * 100, 1),
        "ranging": round(neutral / total * 100, 1),
    }
