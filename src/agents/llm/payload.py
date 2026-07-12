"""Build JSON payloads for LLM agent stages (with analyst input budgets)."""

from __future__ import annotations

from typing import Any

from src.analysis.ict_pa import TimeframeAnalysis, sentiment_score
from src.analysis.narrative_combine import build_pa_llm_summary
from src.analysis.technical_context import build_technical_context, fibonacci_context, timeframe_context
from src.config import (
    ANALYST_CALENDAR_MAX,
    ANALYST_ICT_EVENTS_MAX,
    ANALYST_SOCIAL_MAX,
    ANALYST_TEAM_ITEMS_MAX,
    DEBATE_ANALYST_ITEMS_MAX,
    LLM_PAYLOAD_FUNNEL,
    PAYLOAD_EVIDENCE_MAX,
    TRADER_DEBATE_NOTES_MAX,
)
from src.core.types import AgentEvidence, AnalystTeam, MarketContext, ResearchDebate, RiskReview, TransactionProposal
from src.indicators.technical import ema_relation


def _tf_block(tf: str, analysis: TimeframeAnalysis, *, price: float) -> dict[str, Any]:
    return timeframe_context(tf, analysis, price=price, event_limit=ANALYST_ICT_EVENTS_MAX)


def _structure_vote(analyses) -> dict[str, float]:
    return sentiment_score(analyses)


def _timeframe_trends(ctx: MarketContext) -> dict[str, str]:
    return {
        tf: ctx.analyses[tf].trend for tf in ("1d", "4h", "1h", "15m", "5m") if tf in ctx.analyses
    }


def _event_risk_block(ctx: MarketContext) -> dict[str, Any]:
    upcoming = ctx.derived.get("upcoming_calendar") or []
    return {
        "calendar_high_impact_count": ctx.derived.get("calendar_high_impact_count", 0),
        "event_countdown": ctx.derived.get("event_countdown", {}),
        "upcoming_calendar": upcoming[: min(4, ANALYST_CALENDAR_MAX)],
    }


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


def analyst_team_summaries_payload(team: AnalystTeam, *, top_items: int = 0) -> dict[str, Any]:
    """Bias/summary/confidence per role; optional top-N evidence items per role."""
    out: dict[str, Any] = {}
    for role in ("technical", "fundamentals", "news", "sentiment"):
        report = getattr(team, role)
        block: dict[str, Any] = {
            "bias": report.bias,
            "confidence": report.confidence,
            "summary": report.summary,
        }
        if top_items > 0 and report.items:
            block["items"] = [
                {
                    "category": i.category,
                    "summary": i.summary,
                    "strength": i.strength,
                    "timeframe": i.timeframe,
                    "refs": i.refs,
                }
                for i in sorted(report.items, key=lambda x: -x.strength)[:top_items]
            ]
        out[role] = block
    return out


def analyst_team_input_payload(ctx: MarketContext) -> dict[str, Any]:
    """Per-specialist inputs actually sent to Analyst Team LLM stages (for stage_io audit)."""
    return {
        "technical": technical_analyst_payload(ctx),
        "fundamentals": fundamentals_analyst_payload(ctx),
        "news": news_analyst_payload(ctx),
        "sentiment": sentiment_analyst_payload(ctx),
        "context_stats": ctx.context_stats,
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


def research_payload(ctx: MarketContext, team: AnalystTeam, direction: str) -> dict[str, Any]:
    """Research stage: analyst conclusions primary; minimal structure/event validation."""
    if not LLM_PAYLOAD_FUNNEL:
        payload = market_payload(ctx, team)
        payload["direction"] = direction
        return payload
    return {
        "symbol": "XAUUSD",
        "price": ctx.price,
        "direction": direction,
        "analyst_team": analyst_team_payload(team),
        "structure_vote": _structure_vote(ctx.analyses),
        "timeframe_trends": _timeframe_trends(ctx),
        "event_risk": _event_risk_block(ctx),
    }


def technical_analyst_payload(ctx: MarketContext) -> dict[str, Any]:
    last_5m = ctx.enriched["5m"].iloc[-1] if "5m" in ctx.enriched else None
    ema_block = {}
    if last_5m is not None:
        ema_block = ema_relation(ctx.price, last_5m)
    base = build_technical_context(ctx, event_limit=ANALYST_ICT_EVENTS_MAX)
    pa = base.get("price_action") or {}
    return {
        "symbol": "XAUUSD",
        "price": ctx.price,
        "price_action": pa,
        "price_action_summary": build_pa_llm_summary(pa, price=ctx.price),
        "support_resistance": base.get("support_resistance"),
        "lux_timeframe_panels": base.get("lux_timeframe_panels"),
        "timeframes": base.get("timeframes"),
        "structure_sentiment": ctx.derived.get("structure_sentiment") or base.get("structure_sentiment"),
        "metrics": ctx.metrics,
        "market_position": ctx.derived.get("market_position"),
        "jin10_kline_summary": ctx.derived.get("jin10_kline_summary"),
        "spot_cross_check": ctx.derived.get("spot_cross_check"),
        "ema_vwap_relation": ema_block,
        "fibonacci": _fibonacci_block(ctx),
        "indicators": base.get("indicators"),
        "quality": base.get("quality"),
        "technical_input_stats": ctx.context_stats.get("technical_inputs", {}),
    }


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
        "upcoming_calendar": ctx.derived.get("upcoming_calendar", []),
        "risk_events": ext.risk_events if ext.risk_events and ext.risk_events != "—" else "—",
    }


def news_analyst_payload(ctx: MarketContext) -> dict[str, Any]:
    ext = ctx.external
    ext_dict = ext.to_dict()
    flash = ext_dict.get("flash_headlines") or []
    articles = ext_dict.get("article_headlines") or []
    calendar = ext_dict.get("calendar") or []
    upcoming = ctx.derived.get("upcoming_calendar", [])
    risk_summary = ext.risk_events if ext.risk_events and ext.risk_events != "—" else "—"
    return {
        "symbol": "XAUUSD",
        "price": ctx.price,
        "risk_events": risk_summary,
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
                "count": len(upcoming),
                "high_impact": ctx.derived.get("calendar_high_impact_count", 0),
                "hint": "日历：高 importance 事件应单独成条 evidence，标注时间与预期波动",
                "items": upcoming,
                "upcoming": upcoming,
            },
        },
        "news_topics": ctx.derived.get("news_topics", []),
        "flash_headlines": flash,
        "article_headlines": articles,
        "calendar": upcoming,
        "upcoming_calendar": upcoming,
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
    payload: dict[str, Any] = {
        "bullish": evidence_payload(bullish),
        "bearish": evidence_payload(bearish),
        "sentiment_vote": sentiment_score(analyses),
    }
    if ctx is not None:
        if LLM_PAYLOAD_FUNNEL:
            payload["event_risk"] = _event_risk_block(ctx)
        else:
            payload["derived"] = {
                "news_topics": ctx.derived.get("news_topics", []),
                "upcoming_calendar": ctx.derived.get("upcoming_calendar", []),
                "event_countdown": ctx.derived.get("event_countdown", {}),
                "calendar_high_impact_count": ctx.derived.get("calendar_high_impact_count", 0),
                "spot_cross_check": ctx.derived.get("spot_cross_check"),
            }
    if team is not None:
        if LLM_PAYLOAD_FUNNEL:
            payload["analyst_team"] = analyst_team_summaries_payload(team, top_items=DEBATE_ANALYST_ITEMS_MAX)
        else:
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


def _signal_payload(signal: Any) -> dict[str, Any]:
    return {
        "name": getattr(signal, "name", ""),
        "direction": getattr(signal, "direction", ""),
        "entry_low": getattr(signal, "entry_low", None),
        "entry_high": getattr(signal, "entry_high", None),
        "stop_loss": getattr(signal, "stop_loss", None),
        "take_profits": getattr(signal, "take_profits", []),
        "theme": getattr(signal, "theme", ""),
        "setup_type": getattr(signal, "setup_type", ""),
        "status": getattr(signal, "status", ""),
        "score_grade": getattr(signal, "score_grade", ""),
        "score_total": getattr(signal, "score_total", 0),
        "note": getattr(signal, "note", ""),
    }


def signal_list_payload(signals: list[Any]) -> list[dict[str, Any]]:
    return [
        {"index": idx, **_signal_payload(signal)}
        for idx, signal in enumerate(signals)
    ]


def _legacy_trader_payload(
    ctx: MarketContext,
    debate: ResearchDebate,
    signals: list[Any],
) -> dict[str, Any]:
    return {
        "market": market_payload(ctx),
        "debate": {
            "consensus_bias": debate.consensus_bias,
            "consensus_strength": debate.consensus_strength,
            "discussion_notes": debate.discussion_notes[-6:],
        },
        "candidate_signals": signal_list_payload(signals),
        "decision_constraints": {
            "primary_direction": "Choose long, short, or wait.",
            "signal_indices": "Use only indexes from candidate_signals and exclude invalid signals.",
            "rationale": "Explain why selected signals fit the debate and current structure.",
        },
    }


def trader_decision_payload(
    ctx: MarketContext,
    debate: ResearchDebate,
    team: AnalystTeam,
    signals: list[Any],
) -> dict[str, Any]:
    """Trader stage: debate consensus + analyst summaries + candidate signals (no raw market dump)."""
    notes_cap = TRADER_DEBATE_NOTES_MAX
    return {
        "price": ctx.price,
        "debate": {
            "consensus_bias": debate.consensus_bias,
            "consensus_strength": debate.consensus_strength,
            "discussion_notes": debate.discussion_notes[-notes_cap:],
        },
        "analyst_team_summaries": analyst_team_summaries_payload(team, top_items=DEBATE_ANALYST_ITEMS_MAX),
        "structure_vote": _structure_vote(ctx.analyses),
        "candidate_signals": signal_list_payload(signals),
        "decision_constraints": {
            "primary_direction": "Choose long, short, or wait based on debate consensus.",
            "signal_indices": "Use only indexes from candidate_signals and exclude invalid signals.",
            "rationale": "Explain why selected signals fit the debate; do not invent new price levels.",
        },
    }


def trader_payload(
    ctx: MarketContext,
    debate: ResearchDebate,
    signals: list[Any],
    team: AnalystTeam | None = None,
) -> dict[str, Any]:
    if LLM_PAYLOAD_FUNNEL and team is not None:
        return trader_decision_payload(ctx, debate, team, signals)
    return _legacy_trader_payload(ctx, debate, signals)


def risk_payload(
    proposal: TransactionProposal,
    signal_count: int,
) -> dict[str, Any]:
    return {
        "proposal": proposal.to_dict(),
        "signal_count": signal_count,
        "profiles": ["aggressive", "neutral", "conservative"],
        "review_constraints": {
            "approved": "Reject neutral or weak proposals when risk is unclear.",
            "allowed_signal_indices": "Use only proposal.signal_indices values below signal_count.",
            "position_scale": "0.0 to 1.0; conservative should normally be smaller than neutral.",
        },
    }


def manager_payload(
    proposal: TransactionProposal,
    reviews: list[RiskReview],
) -> dict[str, Any]:
    return {
        "proposal": proposal.to_dict(),
        "risk_reviews": [r.to_dict() for r in reviews],
        "decision_constraints": {
            "action": "execute, reduce, or wait.",
            "selected_signal_indices": "Use only indexes approved by at least one risk profile.",
            "confidence": "0.0 to 1.0; lower confidence when only aggressive risk approves.",
        },
    }


def level_proposer_payload(
    ctx: MarketContext,
    team: AnalystTeam,
    debate: ResearchDebate,
    rule_signals: list[Any],
) -> dict[str, Any]:
    if LLM_PAYLOAD_FUNNEL:
        structure = build_technical_context(ctx, event_limit=ANALYST_ICT_EVENTS_MAX)
        return {
            "symbol": "XAUUSD",
            "price": ctx.price,
            "analyst_team": analyst_team_payload(team),
            "debate": {
                "consensus_bias": debate.consensus_bias,
                "consensus_strength": debate.consensus_strength,
                "discussion_notes": debate.discussion_notes[-5:],
            },
            "structure_context": {
                "price_action": structure.get("price_action"),
                "support_resistance": structure.get("support_resistance"),
                "lux_timeframe_panels": structure.get("lux_timeframe_panels"),
                "timeframes": structure.get("timeframes"),
            },
            "rule_candidate_signals": [_signal_payload(s) for s in rule_signals[:5]],
            "level_constraints": {
                "scope": "Use only levels supported by structure_context, analyst_team and candidate signals.",
                "geometry": "SELL requires stop_loss above entry and TP below entry. BUY requires stop_loss below entry and TP above entry.",
                "execution": "Return candidate zones, not market orders. Include invalidation and trigger expectation in reason.",
                "risk": "Prefer TP1 risk/reward >= 1.0; avoid entries already far behind current price.",
            },
        }
    payload = market_payload(ctx, team)
    payload["debate"] = {
        "consensus_bias": debate.consensus_bias,
        "consensus_strength": debate.consensus_strength,
        "discussion_notes": debate.discussion_notes[-5:],
    }
    payload["rule_candidate_signals"] = [_signal_payload(s) for s in rule_signals[:5]]
    payload["level_constraints"] = {
        "scope": "Use only levels supported by supplied price, Lux SMC structures, FVG/OB zones, swing H/L, Strong/Weak H/L, liquidity, Fib and candidate signals.",
        "geometry": "SELL requires stop_loss above entry and TP below entry. BUY requires stop_loss below entry and TP above entry.",
        "execution": "Return candidate zones, not market orders. Include invalidation and trigger expectation in reason.",
        "risk": "Prefer TP1 risk/reward >= 1.0; avoid entries already far behind current price.",
    }
    return payload
