"""Price-distance helpers for execution vs context structure levels."""

from __future__ import annotations

# Main-chart draw thresholds (also documented in docs/operations/walkthrough.md)
SWING_ATR_MULT = 1.0   # 4h/1h swing zones on 5m main chart
MACRO_ATR_MULT = 1.0   # 15m OB/FVG overlaid on 5m main
EXEC_ATR_MULT = 2.0    # 5m structure on 5m main (execution window)
PCT_FALLBACK = 0.005   # minimum relative distance (0.5%)


def proximity_threshold(
    price: float,
    atr: float | None,
    *,
    atr_mult: float = 1.0,
    pct: float = PCT_FALLBACK,
) -> float:
    return max((atr or 0.0) * atr_mult, price * pct)


def zone_near_price(
    price: float,
    low: float,
    high: float,
    atr: float | None,
    *,
    atr_mult: float = 1.0,
    pct: float = PCT_FALLBACK,
) -> bool:
    """True when price is inside the zone or within the ATR/pct band."""
    lo, hi = min(low, high), max(low, high)
    if lo <= price <= hi:
        return True
    dist = min(abs(price - lo), abs(price - hi))
    return dist <= proximity_threshold(price, atr, atr_mult=atr_mult, pct=pct)


def level_near_price(
    level: float,
    price: float,
    atr: float | None,
    *,
    atr_mult: float = 1.0,
    pct: float = PCT_FALLBACK,
) -> bool:
    return abs(price - level) <= proximity_threshold(price, atr, atr_mult=atr_mult, pct=pct)
