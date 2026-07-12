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

# Trading advice: short = red, long = green (Western convention).
TRADE_COLOR_SHORT = "#dc2626"
TRADE_COLOR_LONG = "#16a34a"


def infer_trade_theme(
    *,
    theme: str = "",
    direction: str = "",
    direction_cn: str = "",
) -> str:
    """Return ``short`` or ``long`` for plan cards and decision styling."""
    t = str(theme or "").strip().lower()
    if t in ("short", "long"):
        return t
    raw = f"{direction} {direction_cn}".lower()
    if raw.strip() in ("sell", "short", "bearish", "se") or any(x in raw for x in ("空", "卖")):
        return "short"
    if raw.strip() in ("buy", "long", "bullish") or any(x in raw for x in ("多", "买")):
        return "long"
    return "long"

def liquidity_label(zone: LiquidityZone) -> str:
    if zone.kind == "swing_high":
        return "摆动高点 / 上方流动性"
    if zone.kind == "swing_low":
        return "摆动低点 / 下方流动性"
    return zone.label
