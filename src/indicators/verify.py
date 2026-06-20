"""Indicator sanity checks for manual verification against TradingView."""

from __future__ import annotations

import pandas as pd

from src.indicators.technical import ema_relation, indicator_values


def indicator_snapshot(df: pd.DataFrame, timeframe: str) -> dict:
    """Return last-bar indicator values and basic sanity notes."""
    if df.empty:
        return {"timeframe": timeframe, "error": "empty dataframe"}

    last = df.iloc[-1]
    price = float(last["Close"])
    row = {
        "timeframe": timeframe,
        "bars": len(df),
        "last_time": str(df.index[-1]),
        "price": round(price, 2),
        "open": round(float(last["Open"]), 2),
        "high": round(float(last["High"]), 2),
        "low": round(float(last["Low"]), 2),
    }

    for col in ("EMA20", "EMA50", "EMA610", "VWAP"):
        if col in df.columns and pd.notna(last[col]):
            val = float(last[col])
            row[col] = round(val, 2)
            row[f"{col}_diff"] = round(price - val, 2)

    row["ema_relation"] = ema_relation(price, last)
    row.update(indicator_values(last))

    notes: list[str] = []
    if "Volume" in df.columns:
        zero_vol = int((df["Volume"].fillna(0) == 0).sum())
        if zero_vol == len(df):
            notes.append("Volume 全为 0，VWAP 基于替代成交量计算，仅供参考")
        elif zero_vol >= len(df) * 0.5:
            notes.append(f"Volume 为 0 占比 {zero_vol}/{len(df)}，VWAP 可靠性下降")

    if len(df) < 610:
        notes.append(f"EMA610 仅基于 {len(df)} 根 K 线，历史不足 610 根时与 TV 长周期 EMA 可能有偏差")

    if "VWAP" in row:
        vwap = row["VWAP"]
        if abs(price - vwap) > price * 0.05:
            notes.append("VWAP 与现价偏离 >5%，请确认是否应为当日锚定 VWAP")

    ema20 = row.get("EMA20")
    ema50 = row.get("EMA50")
    if ema20 is not None and ema50 is not None:
        if ema20 > ema50 and price < ema50:
            notes.append("价格低于 EMA50，但 EMA20 在 EMA50 上方 — 可能处于回调段")
        elif ema20 < ema50 and price > ema50:
            notes.append("价格高于 EMA50，但 EMA20 在 EMA50 下方 — 可能处于反弹段")

    # EMA ordering sanity
    emas = [row.get("EMA20"), row.get("EMA50"), row.get("EMA610")]
    emas = [e for e in emas if e is not None]
    if len(emas) == 3 and not (emas[0] >= emas[1] or emas[1] >= emas[2] or emas[0] <= emas[1] or emas[1] <= emas[2]):
        notes.append("EMA 排列无明显趋势，可能处于震荡")

    row["notes"] = notes
    return row


def indicator_table_rows(snapshots: list[dict]) -> list[dict]:
    """Flatten snapshots for st.table display."""
    rows = []
    for s in snapshots:
        if "error" in s:
            rows.append({"周期": s["timeframe"], "状态": s["error"]})
            continue
        rows.append(
            {
                "周期": s["timeframe"],
                "K线数": s["bars"],
                "现价": s["price"],
                "EMA20": s.get("EMA20", "—"),
                "EMA50": s.get("EMA50", "—"),
                "EMA610": s.get("EMA610", "—"),
                "VWAP": s.get("VWAP", "—"),
                "RSI14": s.get("RSI14", "—"),
                "MACD": s.get("MACD", "—"),
                "MACD_SIG": s.get("MACD_SIGNAL", "—"),
                "ADX14": s.get("ADX14", "—"),
                "ATR14": s.get("ATR14", "—"),
                "EMA20差": s.get("EMA20_diff", "—"),
                "VWAP差": s.get("VWAP_diff", "—"),
            }
        )
    return rows
