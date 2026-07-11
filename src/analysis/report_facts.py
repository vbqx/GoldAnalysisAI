"""Report-level facts assembled from Lux analyses (no human copy)."""

from __future__ import annotations

from typing import Any

import pandas as pd

from src.analysis.display_labels import liquidity_label
from src.analysis.ict_pa import TimeframeAnalysis
from src.analysis.proximity import SWING_ATR_MULT, level_near_price
from src.analysis.tf_snapshot import build_tf_snapshot
from src.indicators.technical import ema_relation

_REPORT_TFS = ("4h", "1h", "15m")
_LIQUIDITY_TFS = ("4h", "1h", "15m", "5m")


def build_tf_summaries(
    data: dict[str, pd.DataFrame],
    analyses: dict[str, TimeframeAnalysis],
    *,
    price: float,
) -> dict[str, dict[str, Any]]:
    """Per-TF Lux snapshots for report schema + narrative_sections."""
    summaries: dict[str, dict[str, Any]] = {}
    for tf in _REPORT_TFS:
        if tf not in analyses or tf not in data:
            continue
        panel = build_tf_snapshot(analyses[tf])
        last = data[tf].iloc[-1]
        panel["ema_relation"] = ema_relation(price, last)
        summaries[tf] = panel
    return summaries


def _strong_weak_context_entries(
    analysis: TimeframeAnalysis,
    *,
    price: float,
    swing_atr: float | None,
) -> list[dict[str, Any]]:
    panel = build_tf_snapshot(analysis)
    entries: list[dict[str, Any]] = []
    for key, label in (
        ("strong_high", "Lux Strong High"),
        ("weak_high", "Lux Weak High"),
        ("strong_low", "Lux Strong Low"),
        ("weak_low", "Lux Weak Low"),
    ):
        level = panel.get(key)
        if level is None:
            continue
        if level_near_price(float(level), price, swing_atr, atr_mult=SWING_ATR_MULT):
            continue
        entries.append(
            {
                "timeframe": analysis.timeframe,
                "price": round(float(level), 2),
                "label": label,
                "kind": key,
                "role": "context",
            }
        )
    return entries


def build_liquidity_entries(
    analyses: dict[str, TimeframeAnalysis],
    *,
    price: float,
    swing_tf: str,
    swing_atr: float | None,
) -> list[dict[str, Any]]:
    """Swing H/L per TF; distant Strong/Weak H/L as context."""
    entries: list[dict[str, Any]] = []
    seen: set[tuple[str, str, float]] = set()

    for tf in _LIQUIDITY_TFS:
        analysis = analyses.get(tf)
        if not analysis:
            continue
        for zone in analysis.liquidity:
            if zone.kind not in ("swing_high", "swing_low"):
                continue
            key = (tf, zone.kind, round(float(zone.price), 2))
            if key in seen:
                continue
            seen.add(key)
            entries.append(
                {
                    "timeframe": tf,
                    "price": round(float(zone.price), 2),
                    "label": liquidity_label(zone),
                    "kind": zone.kind,
                    "role": "execution",
                    "strength": zone.strength,
                }
            )

    primary = analyses.get(swing_tf)
    if primary:
        entries.extend(_strong_weak_context_entries(primary, price=price, swing_atr=swing_atr))

    entries.sort(
        key=lambda row: (
            0 if row["role"] == "execution" else 1,
            abs(float(row["price"]) - price),
        ),
    )
    return entries[:10]
