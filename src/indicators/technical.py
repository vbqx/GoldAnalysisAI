"""Technical indicators: EMA, VWAP, Fibonacci."""

from __future__ import annotations

import pandas as pd


def add_emas(df: pd.DataFrame, periods: tuple[int, ...] = (20, 50, 610)) -> pd.DataFrame:
    out = df.copy()
    for p in periods:
        out[f"EMA{p}"] = out["Close"].ewm(span=p, adjust=False).mean()
    return out


def add_vwap(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    typical = (out["High"] + out["Low"] + out["Close"]) / 3
    vol = out["Volume"].replace(0, pd.NA).fillna(1)
    tp_vol = typical * vol
    # Reset VWAP each trading day (anchored VWAP)
    out["VWAP"] = tp_vol.groupby(out.index.date).cumsum() / vol.groupby(out.index.date).cumsum()
    return out


def enrich(df: pd.DataFrame) -> pd.DataFrame:
    return add_vwap(add_emas(df))


def ema_relation(price: float, row: pd.Series) -> dict[str, str]:
    relations = {}
    for col in ("EMA20", "EMA50", "EMA610", "VWAP"):
        if col not in row or pd.isna(row[col]):
            relations[col] = "N/A"
            continue
        val = float(row[col])
        if price > val * 1.001:
            relations[col] = "上方"
        elif price < val * 0.999:
            relations[col] = "下方"
        else:
            relations[col] = "附近"
    return relations


def fibonacci_levels(swing_high: float, swing_low: float) -> list[dict]:
    """Retracement from high to low (bearish move)."""
    diff = swing_high - swing_low
    ratios = [
        (0.382, "浅回调阻力", 0.65),
        (0.500, "均衡位", 0.55),
        (0.618, "黄金分割阻力", 0.70),
        (0.786, "深度回调", 0.45),
    ]
    levels = []
    for ratio, significance, prob in ratios:
        level = swing_low + diff * ratio
        levels.append(
            {
                "ratio": ratio,
                "price": round(level, 2),
                "significance": significance,
                "probability": prob,
            }
        )
    return levels
