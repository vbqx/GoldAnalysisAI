"""Shared Chinese/English labels for Lux structure display (analysis layer)."""

from __future__ import annotations

from src.analysis.ict_pa import LiquidityZone
from src.viz.display_labels import (
    TF_LABELS,
    TRADE_COLOR_LONG,
    TRADE_COLOR_SHORT,
    infer_trade_theme,
)

TREND_CN = {"bullish": "偏多", "bearish": "偏空", "ranging": "震荡"}
PREMIUM_DISCOUNT_CN = {
    "premium": "溢价区",
    "discount": "折价区",
    "equilibrium": "均衡区",
    "unknown": "区位不明",
}


def liquidity_label(zone: LiquidityZone) -> str:
    if zone.kind == "swing_high":
        return "摆动高点 / 上方流动性"
    if zone.kind == "swing_low":
        return "摆动低点 / 下方流动性"
    return zone.label


__all__ = [
    "TF_LABELS",
    "TRADE_COLOR_LONG",
    "TRADE_COLOR_SHORT",
    "TREND_CN",
    "PREMIUM_DISCOUNT_CN",
    "infer_trade_theme",
    "liquidity_label",
]
