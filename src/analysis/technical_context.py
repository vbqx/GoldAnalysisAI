"""Shared technical facts for rule analysts, LLM payloads, and narrative.

This module is a context builder, not a signal engine: it normalizes OHLCV,
ICT/PA/SMC facts, indicators, quality metadata, and support/resistance levels
so downstream stages can create their own EvidenceItem rows or narratives.
"""

from __future__ import annotations

from typing import Any

import pandas as pd

from src.analysis.ict_pa import TimeframeAnalysis, sentiment_score
from src.core.types import MarketContext
from src.indicators.technical import ema_relation, fibonacci_levels, indicator_values

TF_ORDER = ("1d", "4h", "1h", "15m", "5m")
TF_WEIGHT = {"1d": 0.20, "4h": 0.30, "1h": 0.25, "15m": 0.15, "5m": 0.10}
TECHNICAL_INDICATORS = ("ATR14", "RSI14", "ADX14", "MACD", "MACD_SIGNAL", "MACD_HIST")
MIN_BARS = {"1d": 50, "4h": 50, "1h": 80, "15m": 100, "5m": 120}


def distance_pct(price: float, level: float) -> float:
    if price <= 0:
        return 0.0
    return (price - level) / price * 100


def primary_analysis(ctx: MarketContext) -> TimeframeAnalysis | None:
    return ctx.analyses.get("4h") or ctx.analyses.get("1h") or ctx.analyses.get("1d")


def fibonacci_context(ctx: MarketContext) -> dict[str, Any]:
    """Use the same primary swing selection across rule and LLM paths."""
    primary = primary_analysis(ctx)
    if not primary:
        return {}
    swing_high = primary.swing_high or ctx.metrics.get("daily_high")
    swing_low = primary.swing_low or ctx.metrics.get("daily_low")
    if not swing_high or not swing_low or swing_high <= swing_low:
        return {}
    levels = fibonacci_levels(float(swing_high), float(swing_low))
    return {
        "timeframe": primary.timeframe,
        "swing_high": swing_high,
        "swing_low": swing_low,
        "levels": levels,
        "nearest": sorted(
            [
                {**row, "dist_pct": round(distance_pct(ctx.price, float(row["price"])), 3)}
                for row in levels
            ],
            key=lambda row: abs(float(row["dist_pct"])),
        )[:3],
    }


def support_resistance_context(ctx: MarketContext, *, limit: int = 12) -> dict[str, Any]:
    """Compose auditable S/R levels from price action, ICT zones, and report metrics."""
    levels: list[dict[str, Any]] = []

    def add_level(
        *,
        price: float | None,
        kind: str | None,
        label: str,
        source: str,
        timeframe: str | None = None,
        strength: float = 0.4,
    ) -> None:
        if price is None or price <= 0:
            return
        resolved_kind = kind or _level_kind(ctx.price, price)
        levels.append(
            {
                "kind": resolved_kind,
                "price": round(float(price), 2),
                "label": label,
                "source": source,
                "timeframe": timeframe,
                "strength": round(strength, 3),
                "dist_pct": round(distance_pct(ctx.price, float(price)), 3),
            }
        )

    def add_zone(
        *,
        low: float,
        high: float,
        preferred_kind: str,
        label: str,
        source: str,
        timeframe: str | None,
        strength: float,
    ) -> None:
        mid = (float(low) + float(high)) / 2
        kind = _zone_kind(ctx.price, float(low), float(high), preferred_kind)
        levels.append(
            {
                "kind": kind,
                "price_low": round(float(low), 2),
                "price_high": round(float(high), 2),
                "price": round(mid, 2),
                "label": label,
                "source": source,
                "timeframe": timeframe,
                "strength": round(strength, 3),
                "dist_pct": round(distance_pct(ctx.price, mid), 3),
            }
        )

    metrics = ctx.metrics
    add_level(price=metrics.get("daily_high"), kind="resistance", label="日内高点压力", source="daily_high", strength=0.65)
    add_level(price=metrics.get("daily_low"), kind="support", label="日内低点支撑", source="daily_low", strength=0.65)
    add_level(price=metrics.get("prev_close"), kind=None, label="前收/日开分界", source="prev_close", strength=0.45)

    primary = primary_analysis(ctx)
    if primary:
        add_level(price=primary.swing_high, kind="resistance", label=f"{primary.timeframe} swing high 压力", source="swing_high", timeframe=primary.timeframe, strength=0.72)
        add_level(price=primary.swing_low, kind="support", label=f"{primary.timeframe} swing low 支撑", source="swing_low", timeframe=primary.timeframe, strength=0.72)
        add_level(price=primary.equilibrium, kind="neutral", label=f"{primary.timeframe} equilibrium 多空分界", source="equilibrium", timeframe=primary.timeframe, strength=0.55)

    fib = fibonacci_context(ctx)
    for row in (fib.get("nearest") or [])[:4]:
        add_level(
            price=float(row["price"]),
            kind=None,
            label=f"Fib {row['ratio']:.3f} {row['significance']}",
            source="fibonacci",
            timeframe=fib.get("timeframe"),
            strength=float(row.get("probability", 0.45)),
        )

    for tf, weight in TF_WEIGHT.items():
        analysis = ctx.analyses.get(tf)
        if not analysis:
            continue
        for zone in analysis.liquidity[:3]:
            kind = "support" if "low" in zone.kind or "buy" in zone.label.lower() else "resistance"
            zone_strength = max(float(getattr(zone, "strength", 0.5)), 0.35)
            add_level(
                price=zone.price,
                kind=kind,
                label=zone.label,
                source=f"liquidity:{zone.kind}",
                timeframe=tf,
                strength=weight * 0.85 * zone_strength,
            )
        for ob in analysis.order_blocks[-2:]:
            add_zone(
                low=ob.low,
                high=ob.high,
                preferred_kind="resistance" if ob.direction == "bearish" else "support",
                label=f"{tf} OB {ob.direction}",
                source="order_block",
                timeframe=tf,
                strength=weight * 0.8,
            )
        for fvg in analysis.active_fvgs[:2]:
            add_zone(
                low=fvg.low,
                high=fvg.high,
                preferred_kind="resistance" if fvg.direction == "bearish" else "support",
                label=f"{tf} FVG {fvg.direction}",
                source="fvg",
                timeframe=tf,
                strength=weight * 0.75,
            )

    deduped = _dedupe_levels(levels)
    ranked = sorted(deduped, key=lambda row: (abs(float(row["dist_pct"])), -float(row["strength"])))
    resistance = [row for row in ranked if row["kind"] == "resistance"][:limit]
    support = [row for row in ranked if row["kind"] == "support"][:limit]
    neutral = [row for row in ranked if row["kind"] == "neutral"][: max(3, limit // 3)]
    return {
        "levels": ranked[: limit * 2],
        "resistance": resistance,
        "support": support,
        "neutral": neutral,
        "nearest_resistance": resistance[0] if resistance else None,
        "nearest_support": support[0] if support else None,
    }


def indicator_snapshot(ctx: MarketContext) -> dict[str, Any]:
    by_timeframe: dict[str, Any] = {}
    for tf in TF_ORDER:
        df = ctx.enriched.get(tf)
        if df is None or df.empty:
            continue
        last = df.iloc[-1]
        volume_ratio = _nonzero_volume_ratio(df)
        by_timeframe[tf] = {
            "bars": len(df),
            "ema_vwap_relation": ema_relation(ctx.price, last),
            "indicators": indicator_values(last),
            "ready": _ready_indicators(last),
            "volume_nonzero_ratio": round(volume_ratio, 3),
        }
    return by_timeframe


def timeframe_context(
    tf: str,
    analysis: TimeframeAnalysis,
    *,
    price: float,
    event_limit: int = 8,
    ob_limit: int = 5,
    fvg_limit: int = 5,
    liquidity_limit: int = 6,
) -> dict[str, Any]:
    return {
        "timeframe": tf,
        "trend": analysis.trend,
        "bos": analysis.bos,
        "choch": analysis.choch,
        "premium_discount": analysis.premium_discount,
        "equilibrium": analysis.equilibrium,
        "volume_signal": analysis.volume_signal,
        "swing_high": analysis.swing_high,
        "swing_low": analysis.swing_low,
        "events": _rank_ict_events(analysis, limit=event_limit),
        "order_blocks": [
            {"direction": ob.direction, "low": ob.low, "high": ob.high}
            for ob in analysis.order_blocks[-ob_limit:]
        ],
        "active_fvgs": [
            {"direction": f.direction, "low": f.low, "high": f.high}
            for f in analysis.active_fvgs[:fvg_limit]
        ],
        "liquidity": [
            {
                "price": lz.price,
                "kind": lz.kind,
                "label": lz.label,
                "strength": lz.strength,
                "swept": lz.swept,
            }
            for lz in analysis.liquidity[:liquidity_limit]
        ],
        "distance_to_swing_high_pct": round(distance_pct(price, analysis.swing_high), 3)
        if analysis.swing_high
        else None,
        "distance_to_swing_low_pct": round(distance_pct(price, analysis.swing_low), 3)
        if analysis.swing_low
        else None,
    }


def technical_quality(ctx: MarketContext, indicators: dict[str, Any] | None = None) -> dict[str, Any]:
    indicators = indicators or indicator_snapshot(ctx)
    warnings: list[str] = []
    scores: list[float] = []

    for tf in TF_ORDER:
        bars = len(ctx.enriched.get(tf, []))
        required = MIN_BARS[tf]
        score = min(bars / required, 1.0)
        scores.append(score)
        if bars < required:
            warnings.append(f"{tf} K线不足 {bars}/{required}")

        ready = set((indicators.get(tf) or {}).get("ready") or [])
        ready_score = len(ready.intersection(TECHNICAL_INDICATORS)) / len(TECHNICAL_INDICATORS)
        scores.append(ready_score)
        if ready_score < 0.6:
            warnings.append(f"{tf} 指标未充分 warm-up")

        volume_ratio = float((indicators.get(tf) or {}).get("volume_nonzero_ratio") or 0)
        scores.append(volume_ratio)
        if volume_ratio < 0.5:
            warnings.append(f"{tf} volume 有效性不足")

    ict_total = sum(len(a.events) for a in ctx.analyses.values())
    liquidity_total = sum(len(a.liquidity) for a in ctx.analyses.values())
    premium_known = sum(1 for a in ctx.analyses.values() if a.premium_discount != "unknown")
    structure_score = min((ict_total + liquidity_total + premium_known) / 10, 1.0)
    scores.append(structure_score)
    if structure_score < 0.4:
        warnings.append("ICT结构事件/流动性输入偏少")

    sr = support_resistance_context(ctx)
    sr_count = len(sr.get("support") or []) + len(sr.get("resistance") or [])
    scores.append(min(sr_count / 4, 1.0))
    if sr_count < 2:
        warnings.append("支撑/阻力输入不足")

    score = round(sum(scores) / len(scores), 3) if scores else 0.0
    return {
        "score": score,
        "warnings": warnings[:8],
        "ict_events_total": ict_total,
        "liquidity_zones": liquidity_total,
        "premium_discount_known": premium_known,
        "support_resistance_levels": sr_count,
    }


def build_technical_context(ctx: MarketContext, *, event_limit: int = 8) -> dict[str, Any]:
    indicators = indicator_snapshot(ctx)
    return {
        "symbol": "XAUUSD",
        "price": ctx.price,
        "metrics": ctx.metrics,
        "market_position": ctx.derived.get("market_position"),
        "spot_cross_check": ctx.derived.get("spot_cross_check"),
        "jin10_kline_summary": ctx.derived.get("jin10_kline_summary"),
        "structure_sentiment": ctx.derived.get("structure_sentiment") or sentiment_score(ctx.analyses),
        "technical_input_stats": ctx.context_stats.get("technical_inputs", {}),
        "quality": technical_quality(ctx, indicators),
        "indicators": indicators,
        "fibonacci": fibonacci_context(ctx),
        "support_resistance": support_resistance_context(ctx),
        "timeframes": [
            timeframe_context(tf, ctx.analyses[tf], price=ctx.price, event_limit=event_limit)
            for tf in TF_ORDER
            if tf in ctx.analyses
        ],
    }


def _ready_indicators(row: pd.Series) -> list[str]:
    return [col for col in TECHNICAL_INDICATORS if col in row and pd.notna(row[col])]


def _nonzero_volume_ratio(df: pd.DataFrame) -> float:
    if "Volume" not in df or df.empty:
        return 0.0
    vol = df["Volume"].astype(float)
    return float((vol > 0).sum() / len(vol))


def _rank_ict_events(analysis: TimeframeAnalysis, *, limit: int) -> list[dict[str, Any]]:
    priority = {"choch": 0, "bos": 1}
    sorted_events = sorted(
        analysis.events,
        key=lambda e: (priority.get((e.kind or "").lower(), 9), -e.price),
    )
    return [
        {
            "kind": e.kind,
            "direction": e.direction,
            "price": e.price,
            "time": str(e.time),
        }
        for e in sorted_events[:limit]
    ]


def _level_kind(price: float, level: float) -> str:
    if level > price * 1.0005:
        return "resistance"
    if level < price * 0.9995:
        return "support"
    return "neutral"


def _zone_kind(price: float, low: float, high: float, preferred: str) -> str:
    if high < price:
        return "support"
    if low > price:
        return "resistance"
    if low <= price <= high:
        return "neutral"
    return preferred


def _dedupe_levels(levels: list[dict[str, Any]]) -> list[dict[str, Any]]:
    best: dict[tuple[str, int], dict[str, Any]] = {}
    for level in levels:
        key = (str(level["kind"]), round(float(level["price"]) * 2))
        current = best.get(key)
        if current is None or float(level["strength"]) > float(current["strength"]):
            best[key] = level
    return list(best.values())
