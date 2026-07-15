"""Assemble DGT price-action facts for report schema and LLM."""

from __future__ import annotations

from typing import Any

import pandas as pd

from src.analysis.dgt_price_action import (
    DEFAULT_LOOKBACK,
    analyze_dgt_price_action,
    dgt_result_to_dict,
)

_PA_TFS = ("5m", "15m", "1h", "4h")
_PROFILE_LTF = "5m"
SESSION_TF = "session"
_SESSION_MAX_HOURS = 30
_DAILY_HLC_TOLERANCE = 0.51
# Require LTF to cover most of the Fixed-Range HTF window; else use native TF OHLC.
_LTF_COVER_FRAC = 0.85


def _ltf_covers_window(
    ltf_slice: pd.DataFrame,
    start: pd.Timestamp,
    end: pd.Timestamp,
    *,
    min_frac: float = _LTF_COVER_FRAC,
) -> bool:
    """True when lower-TF bars span ≥ min_frac of the HTF clock window."""
    if ltf_slice.empty or end <= start:
        return False
    window_sec = (pd.Timestamp(end) - pd.Timestamp(start)).total_seconds()
    if window_sec <= 0:
        return False
    covered_from = max(pd.Timestamp(start), pd.Timestamp(ltf_slice.index[0]))
    covered_to = min(pd.Timestamp(end), pd.Timestamp(ltf_slice.index[-1]))
    if covered_to <= covered_from:
        return False
    covered = (covered_to - covered_from).total_seconds()
    return covered >= window_sec * min_frac


def _align_timestamp(ts: pd.Timestamp, ref: pd.DatetimeIndex) -> pd.Timestamp:
    ts = pd.Timestamp(ts)
    if ref.tz is not None:
        if ts.tzinfo is None:
            return ts.tz_localize("UTC").tz_convert(ref.tz)
        return ts.tz_convert(ref.tz)
    if ts.tzinfo is not None:
        return ts.tz_convert("UTC").tz_localize(None)
    return ts


def _bars_for_latest_session_day(df_5m: pd.DataFrame, df_1d: pd.DataFrame) -> pd.DataFrame:
    """5m bars for the provider daily session anchored at the latest 1d bar open."""
    if df_5m.empty or df_1d.empty:
        return df_5m.iloc[0:0]
    idx_5m = df_5m.index
    idx_1d = df_1d.index
    if not isinstance(idx_5m, pd.DatetimeIndex) or not isinstance(idx_1d, pd.DatetimeIndex):
        return df_5m.iloc[0:0]

    session_start = _align_timestamp(idx_1d[-1], idx_5m)
    session_end = min(
        idx_5m[-1] + pd.Timedelta(minutes=5),
        session_start + pd.Timedelta(hours=_SESSION_MAX_HOURS),
    )
    return df_5m.loc[(idx_5m >= session_start) & (idx_5m <= session_end)]


def _session_matches_daily(df_session: pd.DataFrame, daily_row: pd.Series, *, tol: float) -> bool:
    if df_session.empty:
        return False
    agg_h = float(df_session["High"].max())
    agg_l = float(df_session["Low"].min())
    agg_c = float(df_session["Close"].iloc[-1])
    return (
        abs(agg_h - float(daily_row["High"])) <= tol
        and abs(agg_l - float(daily_row["Low"])) <= tol
        and abs(agg_c - float(daily_row["Close"])) <= tol
    )


def build_session_price_action_block(
    df_5m: pd.DataFrame | None,
    df_1d: pd.DataFrame | None,
) -> dict[str, Any] | None:
    """Intraday PA block: session-day volume profile + 量价 S/R from all 5m bars that day."""
    if df_5m is None or df_5m.empty or df_1d is None or df_1d.empty:
        return None
    session_bars = _bars_for_latest_session_day(df_5m, df_1d)
    if session_bars.empty:
        return None
    daily_row = df_1d.iloc[-1]
    if not _session_matches_daily(session_bars, daily_row, tol=_DAILY_HLC_TOLERANCE):
        return None
    lookback = len(session_bars)
    result = analyze_dgt_price_action(session_bars, SESSION_TF, lookback=lookback)
    if result.volume_profile is None or result.volume_profile.poc is None:
        return None
    return dgt_result_to_dict(
        result,
        lookback_requested=lookback,
        lookback_mode="session",
    )


def build_price_action_summaries(
    data: dict[str, pd.DataFrame],
    *,
    lookback: int = DEFAULT_LOOKBACK,
) -> dict[str, dict[str, Any]]:
    """Per-TF DGT metrics with Pine Fixed-Range lookback (default 360 bars).

    Window = last ``lookback`` bars of that timeframe (not chart Visible Range).
    Higher TFs fill volume from 5m in the same clock span when coverage ≥ 85%;
    otherwise the profile uses native timeframe bars (`profile_source`).
    """
    ltf = data.get(_PROFILE_LTF)
    summaries: dict[str, dict[str, Any]] = {}
    for tf in _PA_TFS:
        df = data.get(tf)
        if df is None or df.empty:
            continue
        window = df.tail(lookback)
        profile_bars = None
        profile_source = "native_tf"
        if ltf is not None and not ltf.empty and tf != _PROFILE_LTF and not window.empty:
            start, end = window.index[0], window.index[-1]
            candidates = ltf.loc[(ltf.index >= start) & (ltf.index <= end)]
            if not candidates.empty and _ltf_covers_window(candidates, start, end):
                profile_bars = candidates
                profile_source = "ltf_5m"
        result = analyze_dgt_price_action(
            df,
            tf,
            lookback=lookback,
            profile_bars=profile_bars,
        )
        row = dgt_result_to_dict(result, lookback_requested=lookback)
        row["profile_source"] = profile_source
        summaries[tf] = row
    session = build_session_price_action_block(ltf, data.get("1d"))
    if session:
        summaries[SESSION_TF] = session
    return summaries


def chart_sr_levels(report: dict[str, Any], timeframe: str = "5m") -> list[dict[str, Any]]:
    """Raw S/R list for chart overlays on the given timeframe."""
    pa = report.get("price_action") or {}
    block = pa.get(timeframe) or {}
    return list(block.get("sr_levels") or [])
