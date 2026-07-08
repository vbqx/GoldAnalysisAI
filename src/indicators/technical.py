"""Technical indicators: EMA, VWAP, momentum, volatility, Fibonacci."""

from __future__ import annotations

import pandas as pd

_NAN = float("nan")


def add_emas(df: pd.DataFrame, periods: tuple[int, ...] = (20, 50, 610)) -> pd.DataFrame:
    out = df.copy()
    for p in periods:
        out[f"EMA{p}"] = out["Close"].ewm(span=p, adjust=False).mean()
    return out


def add_vwap(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    typical = (out["High"] + out["Low"] + out["Close"]) / 3
    vol = out["Volume"].replace(0, _NAN).fillna(1)
    tp_vol = typical * vol
    # Reset VWAP each trading day (anchored VWAP)
    out["VWAP"] = tp_vol.groupby(out.index.date).cumsum() / vol.groupby(out.index.date).cumsum()
    return out


def add_atr(df: pd.DataFrame, period: int = 14) -> pd.DataFrame:
    out = df.copy()
    prev_close = out["Close"].shift(1)
    tr = pd.concat(
        [
            out["High"] - out["Low"],
            (out["High"] - prev_close).abs(),
            (out["Low"] - prev_close).abs(),
        ],
        axis=1,
    ).max(axis=1)
    out[f"ATR{period}"] = tr.rolling(period, min_periods=period).mean()
    return out


def add_rsi(df: pd.DataFrame, period: int = 14) -> pd.DataFrame:
    out = df.copy()
    delta = out["Close"].diff()
    gain = delta.clip(lower=0).rolling(period, min_periods=period).mean()
    loss = (-delta.clip(upper=0)).rolling(period, min_periods=period).mean()
    rs = gain / loss.replace(0, _NAN)
    rsi = 100 - (100 / (1 + rs))
    rsi = rsi.mask((loss == 0) & (gain > 0), 100)
    rsi = rsi.mask((loss == 0) & (gain == 0), 50)
    out[f"RSI{period}"] = rsi
    return out


def add_macd(
    df: pd.DataFrame,
    *,
    fast: int = 12,
    slow: int = 26,
    signal: int = 9,
) -> pd.DataFrame:
    out = df.copy()
    ema_fast = out["Close"].ewm(span=fast, adjust=False).mean()
    ema_slow = out["Close"].ewm(span=slow, adjust=False).mean()
    out["MACD"] = ema_fast - ema_slow
    out["MACD_SIGNAL"] = out["MACD"].ewm(span=signal, adjust=False).mean()
    out["MACD_HIST"] = out["MACD"] - out["MACD_SIGNAL"]
    return out


def add_adx(df: pd.DataFrame, period: int = 14) -> pd.DataFrame:
    out = df.copy()
    up_move = out["High"].diff()
    down_move = -out["Low"].diff()
    plus_dm = up_move.where((up_move > down_move) & (up_move > 0), 0.0)
    minus_dm = down_move.where((down_move > up_move) & (down_move > 0), 0.0)

    prev_close = out["Close"].shift(1)
    tr = pd.concat(
        [
            out["High"] - out["Low"],
            (out["High"] - prev_close).abs(),
            (out["Low"] - prev_close).abs(),
        ],
        axis=1,
    ).max(axis=1)
    tr_sum = tr.rolling(period, min_periods=period).sum()
    plus_di = 100 * plus_dm.rolling(period, min_periods=period).sum() / tr_sum.replace(0, _NAN)
    minus_di = 100 * minus_dm.rolling(period, min_periods=period).sum() / tr_sum.replace(0, _NAN)
    dx = ((plus_di - minus_di).abs() / (plus_di + minus_di).replace(0, _NAN)) * 100
    out[f"ADX{period}"] = dx.rolling(period, min_periods=period).mean()
    return out


def enrich(df: pd.DataFrame) -> pd.DataFrame:
    return add_adx(add_macd(add_rsi(add_atr(add_vwap(add_emas(df))))))


def indicator_values(row: pd.Series) -> dict[str, float | None]:
    values: dict[str, float | None] = {}
    for col in ("ATR14", "RSI14", "ADX14", "MACD", "MACD_SIGNAL", "MACD_HIST"):
        if col not in row or pd.isna(row[col]):
            values[col] = None
        else:
            values[col] = round(float(row[col]), 4)
    return values


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
