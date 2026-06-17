"""Build JSON payloads for LLM agent stages (with analyst input budgets)."""

from __future__ import annotations

from typing import Any

from src.analysis.ict_pa import TimeframeAnalysis, sentiment_score
from src.analysis.technical_context import build_technical_context, fibonacci_context, timeframe_context
from src.config import (
    ANALYST_ICT_EVENTS_MAX,
    ANALYST_SOCIAL_MAX,
    ANALYST_TEAM_ITEMS_MAX,
    PAYLOAD_EVIDENCE_MAX,
)
from src.core.types import AgentEvidence, AnalystTeam, MarketContext
from src.indicators.technical import ema_relation


def _tf_block(tf: str, analysis: TimeframeAnalysis, *, price: float) -> dict[str, Any]:
    return timeframe_context(tf, analysis, price=price, event_limit=ANALYST_ICT_EVENTS_MAX)


def analyst_team_payload(team: AnalystTeam) -> dict[str, Any]:
    cap = ANALYST_TEAM_ITEMS_MAX
    return {
        role: {
            "bias": getattr(team, role).bias,
            "confidence": getattr(team, role).confidence,
            "summary": getattr(team, role).summary,
            "items": [
                {
                    "category": i.category,
                    "summary": i.summary,
                    "strength": i.strength,
                    "timeframe": i.timeframe,
                    "refs": i.refs,
                }
                for i in sorted(getattr(team, role).items, key=lambda x: -x.strength)[:cap]
            ],
        }
        for role in ("technical", "fundamentals", "news", "sentiment")
    }


def _fibonacci_block(ctx: MarketContext) -> dict[str, Any]:
    """Use the same primary swing selection as rule technical evidence."""
    return fibonacci_context(ctx)


def market_payload(ctx: MarketContext, team: AnalystTeam | None = None) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "symbol": "XAUUSD",
        "price": ctx.price,
        "metrics": ctx.metrics,
        "external": ctx.external.to_dict(),
        "derived": ctx.derived,
        "context_stats": ctx.context_stats,
        "source": ctx.source_label,
        "timeframes": [
            _tf_block(tf, ctx.analyses[tf], price=ctx.price)
            for tf in ("1d", "4h", "1h", "15m", "5m")
            if tf in ctx.analyses
        ],
    }
    if team:
        payload["analyst_team"] = analyst_team_payload(team)
    return payload


def technical_analyst_payload(ctx: MarketContext) -> dict[str, Any]:
    last_5m = ctx.enriched["5m"].iloc[-1] if "5m" in ctx.enriched else None
    ema_block = {}
    if last_5m is not None:
        ema_block = ema_relation(ctx.price, last_5m)
    payload = build_technical_context(ctx, event_limit=ANALYST_ICT_EVENTS_MAX)
    payload.update({
        "symbol": "XAUUSD",
        "price": ctx.price,
        "metrics": ctx.metrics,
        "market_position": ctx.derived.get("market_position"),
        "jin10_kline_summary": ctx.derived.get("jin10_kline_summary"),
        "spot_cross_check": ctx.derived.get("spot_cross_check"),
        "ema_vwap_relation": ema_block,
        "technical_input_stats": ctx.context_stats.get("technical_inputs", {}),
        "fibonacci": _fibonacci_block(ctx),
        "structure_sentiment": ctx.derived.get("structure_sentiment"),
    })
    return payload


def fundamentals_analyst_payload(ctx: MarketContext) -> dict[str, Any]:
    ext = ctx.external
    return {
        "symbol": "XAUUSD",
        "price": ctx.price,
        "metrics": ctx.metrics,
        "dxy_impact": ext.dxy_impact,
        "macro_quotes": [m.to_dict() for m in ext.macro_quotes],
        "calendar_high_impact": ctx.derived.get("calendar_high_impact_count", 0),
        "event_countdown": ctx.derived.get("event_countdown", {}),
        "risk_events": ext.risk_events,
    }


def news_analyst_payload(ctx: MarketContext) -> dict[str, Any]:
    ext = ctx.external
    ext_dict = ext.to_dict()
    flash = ext_dict.get("flash_headlines") or []
    articles = ext_dict.get("article_headlines") or []
    calendar = ext_dict.get("calendar") or []
    return {
        "symbol": "XAUUSD",
        "price": ctx.price,
        "risk_events": ext.risk_events,
        "channels": {
            "flash": {
                "count": len(flash),
                "hint": "快讯：即时冲击与短线波动，优先评估对黄金方向与波动率的即时影响",
                "items": flash,
            },
            "articles": {
                "count": len(articles),
                "hint": "资讯：深度背景与政策叙事，评估对中期方向与风险偏好的影响",
                "items": articles,
            },
            "calendar": {
                "count": len(calendar),
                "high_impact": ctx.derived.get("calendar_high_impact_count", 0),
                "hint": "日历：高 importance 事件应单独成条 evidence，标注时间与预期波动",
                "items": calendar,
                "upcoming": ctx.derived.get("upcoming_calendar", []),
            },
        },
        "news_topics": ctx.derived.get("news_topics", []),
        "flash_headlines": flash,
        "article_headlines": articles,
        "calendar": calendar,
        "news_headlines": ext_dict.get("news_headlines") or [],
        "headline_count": len(ext.headline_items),
        "sources": ext.sources,
    }


def sentiment_analyst_payload(ctx: MarketContext) -> dict[str, Any]:
    ext = ctx.external
    return {
        "symbol": "XAUUSD",
        "price": ctx.price,
        "structure_sentiment": sentiment_score(ctx.analyses),
        "timeframe_trends": {
            tf: ctx.analyses[tf].trend for tf in ("4h", "1h", "15m", "5m") if tf in ctx.analyses
        },
        "social_sentiment": ext.social_sentiment,
        "social_posts": ext.social_posts[:ANALYST_SOCIAL_MAX],
    }


def debate_payload(
    bullish: AgentEvidence,
    bearish: AgentEvidence,
    analyses,
    *,
    ctx: MarketContext | None = None,
    team: AnalystTeam | None = None,
) -> dict[str, Any]:
    from src.analysis.ict_pa import sentiment_score

    payload: dict[str, Any] = {
        "bullish": evidence_payload(bullish),
        "bearish": evidence_payload(bearish),
        "sentiment_vote": sentiment_score(analyses),
    }
    if ctx is not None:
        payload["derived"] = {
            "news_topics": ctx.derived.get("news_topics", []),
            "upcoming_calendar": ctx.derived.get("upcoming_calendar", []),
            "event_countdown": ctx.derived.get("event_countdown", {}),
            "calendar_high_impact_count": ctx.derived.get("calendar_high_impact_count", 0),
            "spot_cross_check": ctx.derived.get("spot_cross_check"),
        }
    if team is not None:
        payload["analyst_team_summaries"] = {
            role: {
                "bias": getattr(team, role).bias,
                "summary": getattr(team, role).summary,
                "confidence": getattr(team, role).confidence,
            }
            for role in ("technical", "fundamentals", "news", "sentiment")
        }
    return payload


def evidence_payload(evidence: AgentEvidence) -> dict[str, Any]:
    cap = PAYLOAD_EVIDENCE_MAX
    return {
        "agent": evidence.agent,
        "direction": evidence.direction,
        "confidence": evidence.confidence,
        "summary": evidence.summary,
        "items": [
            {
                "category": i.category,
                "summary": i.summary,
                "strength": i.strength,
                "timeframe": i.timeframe,
                "refs": i.refs,
            }
            for i in sorted(evidence.items, key=lambda x: -x.strength)[:cap]
        ],
    }
