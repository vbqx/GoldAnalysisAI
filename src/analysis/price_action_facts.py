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


def build_price_action_summaries(
    data: dict[str, pd.DataFrame],
    *,
    lookback: int = DEFAULT_LOOKBACK,
) -> dict[str, dict[str, Any]]:
    """Per-TF DGT metrics; higher TFs use 5m bars in-window for volume profile."""
    ltf = data.get(_PROFILE_LTF)
    summaries: dict[str, dict[str, Any]] = {}
    for tf in _PA_TFS:
        df = data.get(tf)
        if df is None or df.empty:
            continue
        window = df.tail(lookback)
        profile_bars = None
        if ltf is not None and not ltf.empty and tf != _PROFILE_LTF and not window.empty:
            start, end = window.index[0], window.index[-1]
            profile_bars = ltf.loc[(ltf.index >= start) & (ltf.index <= end)]
        result = analyze_dgt_price_action(
            df,
            tf,
            lookback=lookback,
            profile_bars=profile_bars if profile_bars is not None and not profile_bars.empty else None,
        )
        summaries[tf] = dgt_result_to_dict(result)
    return summaries


def chart_sr_levels(report: dict[str, Any], timeframe: str = "5m") -> list[dict[str, Any]]:
    """Raw S/R list for chart overlays on the given timeframe."""
    pa = report.get("price_action") or {}
    block = pa.get(timeframe) or {}
    return list(block.get("sr_levels") or [])
