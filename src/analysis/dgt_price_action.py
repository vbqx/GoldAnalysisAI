"""DGT Price Action — volume/price S&R, spikes, volatility, volume profile.

Ported from indicator/Price Action concept.pine (dgtrd).
All metrics are computed for report/LLM; chart draws S/R horizontal lines only.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal

import numpy as np
import pandas as pd

# Pine defaults
VOLUME_MA_LEN = 89
VOLUME_SPIKE_MULT = 4.669
ATR_LEN = 11
ATR_MULT = 2.718
PROFILE_ROWS = 100
VALUE_AREA_PCT = 0.68
SUPPLY_DEMAND_THRESH = 0.15
DEFAULT_LOOKBACK = 360

SrKind = Literal["consecutive_sr", "volume_spike", "high_volatility"]
SrDirection = Literal["support", "resistance"]


@dataclass
class SrLevel:
    price: float
    kind: SrKind
    direction: SrDirection
    time: pd.Timestamp
    label: str


@dataclass
class VolumeProfileResult:
    poc: float | None
    vah: float | None
    val: float | None
    profile_high: float | None
    profile_low: float | None
    supply_demand_zones: list[dict[str, float]] = field(default_factory=list)
    volume_ok: bool = True


@dataclass
class DgtPriceActionResult:
    timeframe: str
    lookback_bars: int
    volume_ok: bool
    sr_levels: list[SrLevel] = field(default_factory=list)
    volume_profile: VolumeProfileResult | None = None
    volume_spike_count: int = 0
    high_volatility_count: int = 0


def _nz_volume(series: pd.Series) -> pd.Series:
    return series.fillna(0.0).astype(float)


def _volume_usable(vol: pd.Series, *, min_ratio: float = 0.05) -> bool:
    if vol.empty:
        return False
    return float((vol > 0).sum()) / len(vol) >= min_ratio


def _atr(high: pd.Series, low: pd.Series, close: pd.Series, length: int) -> pd.Series:
    prev = close.shift(1)
    tr = pd.concat(
        [(high - low).abs(), (high - prev).abs(), (low - prev).abs()],
        axis=1,
    ).max(axis=1)
    return tr.rolling(length, min_periods=1).mean()


def _consecutive_sr(
    window: pd.DataFrame,
    vol_ma: pd.Series,
    *,
    use_volume: bool,
) -> list[SrLevel]:
    levels: list[SrLevel] = []
    if len(window) < 3:
        return levels

    o = window["Open"].astype(float)
    h = window["High"].astype(float)
    l = window["Low"].astype(float)
    c = window["Close"].astype(float)
    v = _nz_volume(window["Volume"])

    bull = c > o
    bear = c < o
    rising_vol = v >= v.shift(1)
    rising_price = c > c.shift(1)
    falling_price = c < c.shift(1)

    for i in range(2, len(window)):
        idx = window.index[i]
        if use_volume:
            falling = (
                bool(bear.iloc[i] and bear.iloc[i - 1] and bear.iloc[i - 2])
                and float(v.iloc[i]) > float(vol_ma.iloc[i])
                and bool(rising_vol.iloc[i] and rising_vol.iloc[i - 1])
            )
            rising = (
                bool(bull.iloc[i] and bull.iloc[i - 1] and bull.iloc[i - 2])
                and float(v.iloc[i]) > float(vol_ma.iloc[i])
                and bool(rising_vol.iloc[i] and rising_vol.iloc[i - 1])
            )
        else:
            falling = (
                bool(bear.iloc[i] and bear.iloc[i - 1] and bear.iloc[i - 2])
                and bool(falling_price.iloc[i] and falling_price.iloc[i - 1] and falling_price.iloc[i - 2])
            )
            rising = (
                bool(bull.iloc[i] and bull.iloc[i - 1] and bull.iloc[i - 2])
                and bool(rising_price.iloc[i] and rising_price.iloc[i - 1] and rising_price.iloc[i - 2])
            )

        slice_l = l.iloc[i - 2 : i + 1]
        slice_h = h.iloc[i - 2 : i + 1]
        if falling:
            levels.append(
                SrLevel(
                    price=round(float(slice_l.min()), 2),
                    kind="consecutive_sr",
                    direction="support",
                    time=idx,
                    label="量价连续支撑",
                )
            )
        if rising:
            levels.append(
                SrLevel(
                    price=round(float(slice_h.max()), 2),
                    kind="consecutive_sr",
                    direction="resistance",
                    time=idx,
                    label="量价连续阻力",
                )
            )
    return levels


def _spike_and_volatility_levels(window: pd.DataFrame, vol_ma: pd.Series) -> tuple[list[SrLevel], int, int]:
    levels: list[SrLevel] = []
    spike_count = 0
    hv_count = 0

    o = window["Open"].astype(float)
    h = window["High"].astype(float)
    l = window["Low"].astype(float)
    c = window["Close"].astype(float)
    v = _nz_volume(window["Volume"])
    atr = _atr(h, l, c, ATR_LEN)
    weighted_atr = ATR_MULT * atr

    bull = c > o
    bear = c < o

    for i in range(len(window)):
        idx = window.index[i]
        if float(v.iloc[i]) > VOLUME_SPIKE_MULT * float(vol_ma.iloc[i]):
            spike_count += 1
            if bool(bull.iloc[i]):
                for price, label in ((float(h.iloc[i]), "放量阻力·高点"), (float(c.iloc[i]), "放量阻力·收盘")):
                    levels.append(
                        SrLevel(price=round(price, 2), kind="volume_spike", direction="resistance", time=idx, label=label)
                    )
            if bool(bear.iloc[i]):
                for price, label in ((float(l.iloc[i]), "放量支撑·低点"), (float(c.iloc[i]), "放量支撑·收盘")):
                    levels.append(
                        SrLevel(price=round(price, 2), kind="volume_spike", direction="support", time=idx, label=label)
                    )

        bar_range = float(h.iloc[i] - l.iloc[i])
        if bar_range > float(weighted_atr.iloc[i]):
            hv_count += 1
            if bool(bull.iloc[i]):
                levels.append(
                    SrLevel(
                        price=round(float(h.iloc[i]), 2),
                        kind="high_volatility",
                        direction="resistance",
                        time=idx,
                        label="高波动阻力",
                    )
                )
            if bool(bear.iloc[i]):
                levels.append(
                    SrLevel(
                        price=round(float(l.iloc[i]), 2),
                        kind="high_volatility",
                        direction="support",
                        time=idx,
                        label="高波动支撑",
                    )
                )

    return levels, spike_count, hv_count


def _volume_portion(
    bar_low: float,
    bar_high: float,
    row_low: float,
    row_high: float,
) -> float:
    bar_range = max(bar_high - bar_low, 1e-12)
    if bar_low >= row_low and bar_high > row_high:
        return max(row_high - bar_low, 0.0) / bar_range
    if bar_high <= row_high and bar_low < row_low:
        return max(bar_high - row_low, 0.0) / bar_range
    if bar_low >= row_low and bar_high <= row_high:
        return 1.0
    return max(row_high - row_low, 0.0) / bar_range


def build_volume_profile(
    bars: pd.DataFrame,
    *,
    num_rows: int = PROFILE_ROWS,
    value_area_pct: float = VALUE_AREA_PCT,
    sd_thresh: float = SUPPLY_DEMAND_THRESH,
) -> VolumeProfileResult:
    if bars.empty:
        return VolumeProfileResult(None, None, None, None, None, volume_ok=False)

    v = _nz_volume(bars["Volume"])
    volume_ok = _volume_usable(v)
    if not volume_ok or float(v.sum()) <= 0:
        return VolumeProfileResult(None, None, None, None, None, volume_ok=False)

    p_low = float(bars["Low"].min())
    p_high = float(bars["High"].max())
    if not np.isfinite(p_low) or not np.isfinite(p_high) or p_high <= p_low:
        return VolumeProfileResult(None, None, None, p_high if np.isfinite(p_high) else None, p_low if np.isfinite(p_low) else None, volume_ok=True)

    step = (p_high - p_low) / num_rows
    if not np.isfinite(step) or step <= 0:
        return VolumeProfileResult(None, None, None, p_high, p_low, volume_ok=True)
    totals = np.zeros(num_rows, dtype=float)
    buys = np.zeros(num_rows, dtype=float)

    for idx, row in bars.iterrows():
        bar_low = float(row["Low"])
        bar_high = float(row["High"])
        if not np.isfinite(bar_low) or not np.isfinite(bar_high) or bar_high < bar_low:
            continue
        bar_vol = float(v.loc[idx])
        if bar_vol <= 0 or not np.isfinite(bar_vol):
            continue
        bullish = float(row["Close"]) > float(row["Open"])
        start_row = max(int((bar_low - p_low) / step), 0)
        end_row = min(int((bar_high - p_low) / step), num_rows - 1)
        for ri in range(start_row, end_row + 1):
            row_floor = p_low + ri * step
            row_ceil = row_floor + step
            portion = _volume_portion(bar_low, bar_high, row_floor, row_ceil)
            totals[ri] += bar_vol * portion
            if bullish:
                buys[ri] += bar_vol * portion

    max_vol = float(totals.max()) if totals.size else 0.0
    if max_vol <= 0:
        return VolumeProfileResult(None, None, None, p_high, p_low, volume_ok=True)

    poc_idx = int(totals.argmax())
    poc = round(p_low + (poc_idx + 0.5) * step, 2)

    target = float(totals.sum()) * value_area_pct
    va = float(totals[poc_idx])
    lo_idx = poc_idx
    hi_idx = poc_idx
    while va < target and (lo_idx > 0 or hi_idx < num_rows - 1):
        up_vol = float(totals[hi_idx + 1]) if hi_idx < num_rows - 1 else 0.0
        dn_vol = float(totals[lo_idx - 1]) if lo_idx > 0 else 0.0
        if up_vol >= dn_vol and hi_idx < num_rows - 1:
            hi_idx += 1
            va += up_vol
        elif lo_idx > 0:
            lo_idx -= 1
            va += dn_vol
        else:
            hi_idx += 1
            va += up_vol

    vah = round(p_low + (hi_idx + 1.0) * step, 2)
    val = round(p_low + lo_idx * step, 2)

    sd_zones: list[dict[str, float]] = []
    for ri in range(num_rows):
        if totals[ri] / max_vol < sd_thresh:
            sd_zones.append(
                {
                    "low": round(p_low + ri * step, 2),
                    "high": round(p_low + (ri + 1) * step, 2),
                    "volume_ratio": round(float(totals[ri] / max_vol), 4),
                }
            )

    return VolumeProfileResult(
        poc=poc,
        vah=vah,
        val=val,
        profile_high=round(p_high, 2),
        profile_low=round(p_low, 2),
        supply_demand_zones=sd_zones[:20],
        volume_ok=True,
    )


def _dedupe_sr_levels(levels: list[SrLevel], *, tolerance: float = 0.35) -> list[SrLevel]:
    """Keep newest level when prices cluster (Pine deletes duplicate consecutive lines)."""
    if not levels:
        return []
    ordered = sorted(levels, key=lambda x: x.time)
    kept: list[SrLevel] = []
    for lvl in ordered:
        replaced = False
        for i, existing in enumerate(kept):
            if (
                existing.direction == lvl.direction
                and existing.kind == lvl.kind
                and abs(existing.price - lvl.price) <= tolerance
            ):
                kept[i] = lvl
                replaced = True
                break
        if not replaced:
            kept.append(lvl)
    return kept


def analyze_dgt_price_action(
    df: pd.DataFrame,
    timeframe: str,
    *,
    lookback: int = DEFAULT_LOOKBACK,
    profile_bars: pd.DataFrame | None = None,
) -> DgtPriceActionResult:
    """Run full DGT metrics on one timeframe window."""
    if df.empty:
        return DgtPriceActionResult(timeframe=timeframe, lookback_bars=0, volume_ok=False)

    window = df.tail(lookback).copy()
    vol = _nz_volume(window["Volume"])
    volume_ok = _volume_usable(vol)
    vol_ma = vol.rolling(VOLUME_MA_LEN, min_periods=1).mean()

    sr: list[SrLevel] = []
    sr.extend(_consecutive_sr(window, vol_ma, use_volume=volume_ok))
    spike_levels, spike_count, hv_count = _spike_and_volatility_levels(window, vol_ma)
    sr.extend(spike_levels)
    sr = _dedupe_sr_levels(sr)

    profile_source = profile_bars.tail(lookback) if profile_bars is not None else window
    profile = build_volume_profile(profile_source)

    return DgtPriceActionResult(
        timeframe=timeframe,
        lookback_bars=len(window),
        volume_ok=volume_ok,
        sr_levels=sr,
        volume_profile=profile,
        volume_spike_count=spike_count,
        high_volatility_count=hv_count,
    )


def dgt_result_to_dict(result: DgtPriceActionResult) -> dict[str, Any]:
    vp = result.volume_profile
    return {
        "timeframe": result.timeframe,
        "lookback_bars": result.lookback_bars,
        "volume_ok": result.volume_ok,
        "volume_spike_count": result.volume_spike_count,
        "high_volatility_count": result.high_volatility_count,
        "sr_levels": [
            {
                "price": lvl.price,
                "kind": lvl.kind,
                "direction": lvl.direction,
                "time": lvl.time.isoformat(),
                "label": lvl.label,
            }
            for lvl in result.sr_levels
        ],
        "volume_profile": None
        if vp is None
        else {
            "poc": vp.poc,
            "vah": vp.vah,
            "val": vp.val,
            "profile_high": vp.profile_high,
            "profile_low": vp.profile_low,
            "supply_demand_zones": vp.supply_demand_zones,
            "volume_ok": vp.volume_ok,
        },
    }
