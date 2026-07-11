"""Shared Chinese/English labels for Lux structure display."""

from __future__ import annotations

from src.analysis.ict_pa import LiquidityZone

TREND_CN = {"bullish": "偏多", "bearish": "偏空", "ranging": "震荡"}
PREMIUM_DISCOUNT_CN = {
    "premium": "溢价区",
    "discount": "折价区",
    "equilibrium": "均衡区",
    "unknown": "区位不明",
}

TF_LABELS = {"4h": "4H", "1h": "1H", "15m": "15M", "5m": "5M", "1d": "1D"}


def liquidity_label(zone: LiquidityZone) -> str:
    if zone.kind == "swing_high":
        return "摆动高点 / 上方流动性"
    if zone.kind == "swing_low":
        return "摆动低点 / 下方流动性"
    return zone.label
