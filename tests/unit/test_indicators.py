"""Indicator unit tests — IND-01~03, IND-10~13."""
from __future__ import annotations

import pandas as pd
import pytest

from src.data.fetcher import daily_metrics
from src.indicators.verify import indicator_snapshot, indicator_table_rows


def _sample_ohlcv(n: int = 100, price: float = 4200.0) -> pd.DataFrame:
    idx = pd.date_range("2026-01-01", periods=n, freq="5min")
    close = pd.Series(price, index=idx) + pd.Series(range(n), index=idx) * 0.01
    df = pd.DataFrame(
        {
            "Open": close - 0.5,
            "High": close + 1.0,
            "Low": close - 1.0,
            "Close": close,
            "Volume": 1000,
            "EMA20": close.rolling(20, min_periods=1).mean(),
            "EMA50": close.rolling(50, min_periods=1).mean(),
            "EMA610": close.rolling(min(610, n), min_periods=1).mean(),
            "VWAP": close * 0.99,
        },
        index=idx,
    )
    return df


def test_daily_metrics_change_consistency() -> None:
    """IND-02: daily_change / daily_change_pct 自洽."""
    df = _sample_ohlcv(5)
    df.iloc[-1, df.columns.get_loc("Close")] = 4210.0
    df.iloc[-2, df.columns.get_loc("Close")] = 4200.0
    m = daily_metrics(df)
    assert m["daily_change"] == pytest.approx(10.0)
    assert m["daily_change_pct"] == pytest.approx(10.0 / 4200.0 * 100)


def test_daily_high_low_bounds() -> None:
    """IND-03: daily_high >= current_price >= daily_low."""
    df = _sample_ohlcv(5)
    m = daily_metrics(df)
    assert m["daily_high"] >= m["current_price"] >= m["daily_low"]


def test_indicator_snapshot_has_ema_vwap() -> None:
    """IND-10: indicator_snapshot 输出 EMA/VWAP 字段."""
    snap = indicator_snapshot(_sample_ohlcv(200), "5m")
    assert snap["timeframe"] == "5m"
    for key in ("EMA20", "EMA50", "EMA610", "VWAP", "EMA20_diff", "VWAP_diff"):
        assert key in snap


def test_multi_tf_snapshot_same_price() -> None:
    """IND-11: 多周期 snapshot 现价一致（同源数据）."""
    df = _sample_ohlcv(200, price=4218.56)
    s5 = indicator_snapshot(df, "5m")
    s15 = indicator_snapshot(df, "15m")
    assert s5["price"] == s15["price"]


def test_ema610_insufficient_history_note() -> None:
    """IND-12: bars<610 时 EMA610 历史不足提示."""
    snap = indicator_snapshot(_sample_ohlcv(100), "5m")
    assert any("610" in n for n in snap["notes"])


def test_vwap_deviation_note() -> None:
    """IND-13: VWAP 偏离>5% 时 notes 警告."""
    df = _sample_ohlcv(50)
    df.iloc[-1, df.columns.get_loc("VWAP")] = df.iloc[-1]["Close"] * 0.90
    snap = indicator_snapshot(df, "5m")
    assert any("VWAP" in n and "5%" in n for n in snap["notes"])


def test_indicator_table_rows_columns() -> None:
    snaps = [indicator_snapshot(_sample_ohlcv(50), "5m")]
    rows = indicator_table_rows(snaps)
    assert rows[0]["周期"] == "5m"
    assert "EMA20" in rows[0] and "VWAP差" in rows[0]
