"""Shared Chinese/English labels for Lux structure display (analysis layer)."""

from __future__ import annotations

from src.analysis.ict_pa import LiquidityZone
TF_LABELS = {"4h": "4H", "1h": "1H", "15m": "15M", "5m": "5M", "1d": "1D"}
TRADE_COLOR_SHORT = "#dc2626"
TRADE_COLOR_LONG = "#16a34a"


def infer_trade_theme(*, theme: str = "", direction: str = "", direction_cn: str = "") -> str:
    value = f"{theme} {direction} {direction_cn}".lower()
    return "short" if any(token in value for token in ("short", "sell", "bear", "空", "卖")) else "long"

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
