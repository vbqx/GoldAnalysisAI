"""Build derived analyst context and density metrics.

Called once after ``assemble_market_context()`` via ``finalize_market_context()``:

- Layer 2 derived signals (EMA position, news topics, event countdown, spot/kline cross-check)
- ``context_stats`` for observability in report meta and Analyst Team stage I/O
"""

from __future__ import annotations

import json
from datetime import datetime
from typing import Any

import pandas as pd

from src.data.news_topics import cluster_headline_topics
from src.analysis.ict_pa import sentiment_score
from src.config import (
    JIN10_KLINE_ENABLED,
    JIN10_QUOTE_ENABLED,
)
from src.core.types import CalendarEvent, MarketContext
from src.data.calendar_utils import filter_upcoming_calendar_events, parse_event_time
from src.data.external_format import sync_external_legacy_fields
from src.indicators.technical import ema_relation

_TECHNICAL_READY_COLUMNS = (
    # Stats include legacy EMA/VWAP plus momentum/volatility columns; quality
    # scoring in technical_context only evaluates TECHNICAL_INDICATORS.
    "EMA20",
    "EMA50",
    "EMA610",
    "VWAP",
    "ATR14",
    "RSI14",
    "ADX14",
    "MACD",
    "MACD_SIGNAL",
    "MACD_HIST",
)


def build_market_position(enriched: dict[str, pd.DataFrame], price: float) -> dict[str, Any]:
    """EMA / VWAP distances and recent range for technical analyst."""
    block: dict[str, Any] = {"price": price}
    if "5m" in enriched:
        last = enriched["5m"].iloc[-1]
        relations = ema_relation(price, last)
        block["ema_vwap"] = {
            col: {"value": round(float(last[col]), 2), "relation": rel}
            for col, rel in relations.items()
            if col in last and pd.notna(last[col]) and rel != "N/A"
        }
    if "1d" in enriched and len(enriched["1d"]) >= 5:
        df = enriched["1d"].tail(5)
        block["range_5d"] = {
            "high": round(float(df["High"].max()), 2),
            "low": round(float(df["Low"].min()), 2),
        }
        block["range_position"] = round(
            (price - float(df["Low"].min())) / max(float(df["High"].max()) - float(df["Low"].min()), 1e-9),
            3,
        )
    return block


def build_spot_cross_check(tv_price: float, quote: dict[str, Any] | None) -> dict[str, Any]:
    if not quote:
        return {}
    try:
        jin10_close = float(quote.get("close") or 0)
    except (TypeError, ValueError):
        return {}
    if jin10_close <= 0 or tv_price <= 0:
        return {}
    diff_pct = abs(jin10_close - tv_price) / tv_price * 100
    return {
        "code": quote.get("code", "XAUUSD"),
        "jin10_close": jin10_close,
        "tv_price": round(tv_price, 2),
        "diff_pct": round(diff_pct, 3),
        "aligned": diff_pct < 0.15,
        "jin10_change_pct": quote.get("ups_percent"),
        "quote_time": quote.get("time"),
    }


def build_event_countdown(events: list[CalendarEvent]) -> dict[str, Any]:
    """Hours until the next high-impact calendar event."""
    now = datetime.now()
    best: CalendarEvent | None = None
    best_hours: float | None = None
    for event in filter_upcoming_calendar_events(events):
        if event.importance < 3.0:
            continue
        when = parse_event_time(event.time)
        if when is None:
            continue
        hours = (when - now).total_seconds() / 3600
        if hours < -1:
            continue
        if best_hours is None or hours < best_hours:
            best_hours = hours
            best = event
    if best is None or best_hours is None:
        return {}
    return {
        "event": best.event,
        "time": best.time,
        "region": best.region,
        "importance": best.importance,
        "hours_until": round(best_hours, 1),
    }


def build_jin10_kline_summary(bars: list[dict[str, Any]], tv_price: float) -> dict[str, Any]:
    if not bars:
        return {}
    last = bars[-1]
    try:
        close = float(last.get("close") or 0)
    except (TypeError, ValueError):
        return {}
    if close <= 0:
        return {}
    first = bars[0]
    try:
        open_px = float(first.get("open") or first.get("close") or close)
    except (TypeError, ValueError):
        open_px = close
    change_pct = (close - open_px) / open_px * 100 if open_px else 0.0
    diff_pct = abs(close - tv_price) / tv_price * 100 if tv_price > 0 else 0.0
    return {
        "bars": len(bars),
        "last_close": round(close, 2),
        "session_change_pct": round(change_pct, 3),
        "tv_price": round(tv_price, 2),
        "diff_pct": round(diff_pct, 3),
        "aligned_with_tv": diff_pct < 0.15,
        "last_time": last.get("time"),
    }


def build_derived_context(ctx: MarketContext) -> dict[str, Any]:
    vote = sentiment_score(ctx.analyses)
    ext = ctx.external
    upcoming = filter_upcoming_calendar_events(ext.calendar_events)
    high_impact = sum(1 for e in upcoming if e.importance >= 3.0)
    derived: dict[str, Any] = {
        "market_position": build_market_position(ctx.enriched, ctx.price),
        "structure_sentiment": vote,
        "calendar_high_impact_count": high_impact,
        "upcoming_calendar": [e.to_dict() for e in upcoming[:6]],
        "news_topics": cluster_headline_topics(ext.headline_items),
        "event_countdown": build_event_countdown(upcoming),
        "headline_count": len(ext.headline_items),
        "flash_count": sum(1 for h in ext.headline_items if h.source == "jin10_flash"),
        "article_count": sum(1 for h in ext.headline_items if h.source == "jin10_news"),
        "macro_bias_votes": {
            q.bias: sum(1 for m in ext.macro_quotes if m.bias == q.bias) for q in ext.macro_quotes
        },
    }
    if JIN10_QUOTE_ENABLED:
        from src.data.sources.jin10_feed import fetch_jin10_quote

        quote, _ = fetch_jin10_quote()
        cross = build_spot_cross_check(ctx.price, quote)
        if cross:
            derived["spot_cross_check"] = cross
    if JIN10_KLINE_ENABLED:
        from src.data.sources.jin10_feed import fetch_jin10_kline

        bars, _ = fetch_jin10_kline()
        kline_summary = build_jin10_kline_summary(bars, ctx.price)
        if kline_summary:
            derived["jin10_kline_summary"] = kline_summary
    return derived


def compute_context_stats(ctx: MarketContext) -> dict[str, Any]:
    ext = ctx.external
    ict_events = sum(len(a.events) for a in ctx.analyses.values())
    stats = {
        "headline_items": len(ext.headline_items),
        "calendar_events": len(ext.calendar_events),
        "macro_quotes": len(ext.macro_quotes),
        "social_posts": len(ext.social_posts),
        "ict_events_total": ict_events,
        "technical_inputs": _technical_input_stats(ctx),
        "analyst_inputs": _analyst_input_stats(ctx),
        "sources": list(ext.sources),
    }
    try:
        payload_sample = json.dumps(ctx.external.to_dict(), ensure_ascii=False)
        stats["external_payload_bytes"] = len(payload_sample.encode("utf-8"))
    except Exception:
        stats["external_payload_bytes"] = 0
    return stats


def _technical_input_stats(ctx: MarketContext) -> dict[str, Any]:
    """Observability snapshot for K-line-derived technical inputs."""
    from src.analysis.technical_context import support_resistance_context, technical_quality

    bars = {tf: len(df) for tf, df in ctx.enriched.items()}
    sr = support_resistance_context(ctx)
    indicator_ready: dict[str, list[str]] = {}
    for tf, df in ctx.enriched.items():
        if df.empty:
            indicator_ready[tf] = []
            continue
        last = df.iloc[-1]
        indicator_ready[tf] = [col for col in _TECHNICAL_READY_COLUMNS if col in last and pd.notna(last[col])]

    by_timeframe: dict[str, Any] = {}
    for tf, analysis in ctx.analyses.items():
        by_timeframe[tf] = {
            "bars": bars.get(tf, 0),
            "ict_events": len(analysis.events),
            "order_blocks": len(analysis.order_blocks),
            "active_fvgs": len(analysis.active_fvgs),
            "liquidity_zones": len(analysis.liquidity),
            "premium_discount": analysis.premium_discount,
            "volume_signal_available": analysis.volume_signal != "N/A",
            "indicator_ready": indicator_ready.get(tf, []),
            "volume_nonzero_ratio": _volume_nonzero_ratio(ctx.enriched.get(tf)),
        }

    return {
        "bars": bars,
        "timeframes": sorted(set(ctx.enriched) | set(ctx.analyses)),
        "by_timeframe": by_timeframe,
        "premium_discount_known": sum(
            1 for a in ctx.analyses.values() if a.premium_discount != "unknown"
        ),
        "volume_signal_available": sum(
            1 for a in ctx.analyses.values() if a.volume_signal != "N/A"
        ),
        "liquidity_zones": sum(len(a.liquidity) for a in ctx.analyses.values()),
        "active_fvgs": sum(len(a.active_fvgs) for a in ctx.analyses.values()),
        "order_blocks": sum(len(a.order_blocks) for a in ctx.analyses.values()),
        "indicator_ready": indicator_ready,
        "volume_nonzero_ratio": {
            tf: _volume_nonzero_ratio(df) for tf, df in ctx.enriched.items()
        },
        "support_resistance": {
            "resistance": len(sr.get("resistance") or []),
            "support": len(sr.get("support") or []),
            "neutral": len(sr.get("neutral") or []),
        },
        "quality": technical_quality(ctx),
    }


def _volume_nonzero_ratio(df: pd.DataFrame | None) -> float:
    if df is None or df.empty or "Volume" not in df:
        return 0.0
    vol = df["Volume"].astype(float)
    return round(float((vol > 0).sum() / len(vol)), 3)


def _analyst_input_stats(ctx: MarketContext) -> dict[str, Any]:
    """Role-level input density for the non-technical analysts.

    These stats are audit metadata, not direct trading signals. The rule analysts
    convert the same underlying inputs into EvidenceItem rows when useful.
    """
    ext = ctx.external
    flash = sum(1 for h in ext.headline_items if h.source == "jin10_flash")
    articles = sum(1 for h in ext.headline_items if h.source == "jin10_news")
    high_impact = sum(1 for e in ext.calendar_events if e.importance >= 3.0)

    social_kind_counts: dict[str, int] = {}
    social_delta = 0.0
    for post in ext.social_posts:
        kind = str(post.get("kind") or "social")
        social_kind_counts[kind] = social_kind_counts.get(kind, 0) + 1
        try:
            social_delta += float(post.get("bias_delta") or 0)
        except (TypeError, ValueError):
            continue

    quote_names = [q.name for q in ext.macro_quotes]
    return {
        "fundamentals": {
            "macro_quotes": len(ext.macro_quotes),
            "quote_names": quote_names,
            "has_dxy": "DXY" in quote_names,
            "has_us10y": "US10Y" in quote_names,
            "high_impact_calendar": high_impact,
            "fetch_errors": [e for e in ext.fetch_errors if "dxy" in e.lower() or "us10y" in e.lower()][:3],
        },
        "news": {
            "headline_items": len(ext.headline_items),
            "flash": flash,
            "articles": articles,
            "calendar_events": len(ext.calendar_events),
            "high_impact_calendar": high_impact,
            "topics": ctx.derived.get("news_topics", []),
            "live_sources": [
                s for s in ext.sources if s in ("jin10_flash", "jin10_news", "jin10_calendar")
            ],
            "fetch_errors": [e for e in ext.fetch_errors if "jin10" in e.lower()][:3],
        },
        "sentiment": {
            "structure_sentiment": ctx.derived.get("structure_sentiment", {}),
            "social_posts": len(ext.social_posts),
            "social_kind_counts": social_kind_counts,
            "social_bias_delta": round(social_delta, 3),
            "has_social_summary": bool(ext.social_sentiment and ext.social_sentiment != "—"),
            "live_sources": [s for s in ext.sources if s == "tradingview_social"],
        },
    }


def finalize_market_context(ctx: MarketContext) -> MarketContext:
    """Attach derived signals and density stats after assembly."""
    upcoming = filter_upcoming_calendar_events(ctx.external.calendar_events)
    ctx.external.calendar_events = upcoming
    sync_external_legacy_fields(ctx.external)
    ctx.derived = build_derived_context(ctx)
    ctx.context_stats = compute_context_stats(ctx)
    return ctx
