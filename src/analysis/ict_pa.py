"""ICT / Price Action shared types — LuxAlgo SMC detection via luxalgo_smc."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

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
    pivot_time: pd.Timestamp | None = None
    scope: Literal["internal", "swing"] = "swing"


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


def _swing_liquidity(
    swing_high: float | None,
    swing_low: float | None,
) -> list[LiquidityZone]:
    """Key liquidity from Lux swing pivots (replaces EQH/EQL for LLM/UI)."""
    zones: list[LiquidityZone] = []
    if swing_high is not None:
        zones.append(
            LiquidityZone(
                float(swing_high),
                "swing_high",
                "摆动高点 / 上方流动性",
                0.72,
            )
        )
    if swing_low is not None:
        zones.append(
            LiquidityZone(
                float(swing_low),
                "swing_low",
                "摆动低点 / 下方流动性",
                0.72,
            )
        )
    return zones


def _latest_structure_labels(
    events: list[StructureEvent],
    *,
    scope: Literal["internal", "swing"] | None = None,
) -> tuple[str, str]:
    filtered = [e for e in events if scope is None or e.scope == scope]
    bos = choch = "无"
    for event in reversed(filtered):
        label = f"{event.direction} @ {event.price:.2f}"
        if event.kind == "BOS" and bos == "无":
            bos = label
        elif event.kind == "CHoCH" and choch == "无":
            choch = label
    return bos, choch


def analyze_timeframe(df: pd.DataFrame, timeframe: str) -> TimeframeAnalysis:
    """Analyze one timeframe using LuxAlgo SMC detection rules."""
    from src.analysis.luxalgo_smc import analyze_luxalgo

    lux = analyze_luxalgo(df)

    # Lux chart defaults: internal structure labels (dashed) are primary on 1H/15M/4H.
    bos_status, choch_status = _latest_structure_labels(lux.events, scope="internal")
    if bos_status == "无" and choch_status == "无":
        bos_status, choch_status = _latest_structure_labels(lux.events, scope="swing")

    price = float(df["Close"].iloc[-1])
    recent = df.iloc[-5:] if len(df) >= 5 else df
    atr = _last_numeric(df, "ATR14")
    recent_high = float(recent["High"].max()) if not recent.empty else None
    recent_low = float(recent["Low"].min()) if not recent.empty else None

    swing_high = lux.swing_high
    swing_low = lux.swing_low
    pd_zone, eq = _premium_discount(swing_high, swing_low, price)

    liquidity = _swing_liquidity(swing_high, swing_low)

    return TimeframeAnalysis(
        timeframe=timeframe,
        trend=lux.trend,
        bos=bos_status,
        choch=choch_status,
        order_blocks=lux.order_blocks,
        fvgs=lux.fvgs,
        active_fvgs=lux.active_fvgs,
        liquidity=liquidity,
        swing_high=swing_high,
        swing_low=swing_low,
        events=lux.events,
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
