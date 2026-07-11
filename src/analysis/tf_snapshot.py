"""Per-timeframe Lux structure snapshot — single fact primitive for report/LLM/UI."""

from __future__ import annotations

from typing import Any

from src.analysis.ict_pa import StructureEvent, TimeframeAnalysis

SNAPSHOT_LIMIT = 5


def _newest_events(
    events: list[StructureEvent],
    *,
    kind: str,
    limit: int = SNAPSHOT_LIMIT,
) -> list[StructureEvent]:
    matched = [e for e in events if e.kind == kind]
    matched.sort(key=lambda e: e.time, reverse=True)
    return matched[:limit]


def _serialize_event(event: StructureEvent) -> dict[str, Any]:
    scope_cn = "内结构" if event.scope == "internal" else "摆动"
    dir_cn = "看涨" if event.direction == "bullish" else "看跌"
    return {
        "kind": event.kind,
        "direction": event.direction,
        "price": round(float(event.price), 2),
        "scope": event.scope,
        "label": f"{event.kind} {scope_cn}{dir_cn} @{event.price:.0f}",
    }


def _strong_weak_high_low(
    trend: str,
    swing_high: float | None,
    swing_low: float | None,
) -> dict[str, float | None]:
    if trend == "bullish":
        return {
            "strong_high": swing_high,
            "weak_high": None,
            "strong_low": None,
            "weak_low": swing_low,
        }
    if trend == "bearish":
        return {
            "strong_high": None,
            "weak_high": swing_high,
            "strong_low": swing_low,
            "weak_low": None,
        }
    return {
        "strong_high": None,
        "weak_high": swing_high,
        "strong_low": None,
        "weak_low": swing_low,
    }


def build_tf_snapshot(analysis: TimeframeAnalysis) -> dict[str, Any]:
    """Canonical per-TF facts from full-bar Lux detection (no chart visibility filter)."""
    bos_events = _newest_events(analysis.events, kind="BOS")
    choch_events = _newest_events(analysis.events, kind="CHoCH")
    sw = _strong_weak_high_low(analysis.trend, analysis.swing_high, analysis.swing_low)

    return {
        "timeframe": analysis.timeframe,
        "trend": analysis.trend,
        "bos": analysis.bos,
        "choch": analysis.choch,
        "premium_discount": analysis.premium_discount,
        "equilibrium": analysis.equilibrium,
        "volume_signal": analysis.volume_signal,
        "swing_high": analysis.swing_high,
        "swing_low": analysis.swing_low,
        "bos_list": [_serialize_event(e) for e in bos_events],
        "choch_list": [_serialize_event(e) for e in choch_events],
        "order_blocks": [
            {"low": ob.low, "high": ob.high, "direction": ob.direction}
            for ob in analysis.order_blocks[:SNAPSHOT_LIMIT]
        ],
        "fvgs": [
            {"low": fvg.low, "high": fvg.high, "direction": fvg.direction}
            for fvg in analysis.active_fvgs[:SNAPSHOT_LIMIT]
        ],
        **sw,
    }
