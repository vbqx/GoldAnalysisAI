"""Compose the compact Advice V2 report artifact."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from src.advice.types import AdvicePacket
from src.analysis.data_freshness import build_data_as_of
from src.analysis.technical_context import support_resistance_context, timeframe_context
from src.core.types import MarketContext
from src.data.fetcher import format_utc8


def _external_context(ctx: MarketContext) -> dict[str, Any]:
    return {
        "dxy_impact": ctx.external.dxy_impact,
        "risk_events": ctx.external.risk_events,
        "calendar_events": [row.to_dict() for row in ctx.external.calendar_events[:8]],
        "headlines": [row.to_dict() for row in ctx.external.headline_items[:8]],
        "macro_quotes": [row.to_dict() for row in ctx.external.macro_quotes],
        "sources": list(ctx.external.sources),
        "fetch_errors": list(ctx.external.fetch_errors[:5]),
        "source_policy": "外部数据仅作背景与事件风险参考，不直接生成入场价位。",
    }


def build_advice_report(
    ctx: MarketContext,
    advice: AdvicePacket,
    *,
    run_id: str,
    run_config: dict[str, Any],
) -> dict[str, Any]:
    as_of = build_data_as_of(ctx.enriched, now=ctx.derived.get("evaluation_time"))
    timeframes = {
        tf: timeframe_context(tf, analysis, price=ctx.price)
        for tf in ("4h", "1h", "15m", "5m")
        if (analysis := ctx.analyses.get(tf)) is not None
    }
    return {
        "artifact_kind": "human_review_advice",
        "artifact_version": 2,
        "meta": {
            "title": "XAUUSD 人工审核交易建议",
            "updated_at": format_utc8(datetime.now(timezone.utc).isoformat()),
            "methodology": "结构事实 + 确定性审核 + 人工确认",
            "data_source": ctx.source_label,
            "run_archive_id": run_id,
            "run_config": run_config,
            "run_config_fingerprint": "",
            "data_as_of": as_of,
            "observation_mode": True,
            "context_stats": ctx.context_stats,
        },
        "metrics": dict(ctx.metrics),
        "advice": advice.to_dict(),
        "timeframes": timeframes,
        "levels": support_resistance_context(ctx, limit=12),
        "external": _external_context(ctx),
    }
