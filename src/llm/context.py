"""Serialize pipeline state into a compact narrative-only LLM context payload.

Analyst Team LLM stages use ``src.agents.llm.payload``. This module is only for
the final report narrative layer after debate/trader/risk/manager have run.
"""

from __future__ import annotations

from typing import Any

from src.analysis.narrative_facts import (
    NARRATIVE_ICT_PER_TF,
    build_narrative_facts_for_llm,
)
from src.analysis.technical_context import build_technical_context, timeframe_context
from src.config import ANALYST_CALENDAR_MAX, ANALYST_ICT_EVENTS_MAX
from src.core.types import ManagerDecision, MarketContext, ResearchDebate

NARRATIVE_ICT_TOTAL = ANALYST_ICT_EVENTS_MAX * 3
NARRATIVE_TIMEFRAMES = ("4h", "1h", "15m")


def _slim_external(external: dict[str, Any], derived: dict[str, Any] | None = None) -> dict[str, Any]:
    derived = derived or {}
    upcoming = derived.get("upcoming_calendar") or []
    risk_summary = external.get("risk_events") if external.get("risk_events") not in (None, "—", "") else "—"
    if not upcoming:
        risk_summary = "—"
    return {
        "dxy_impact": external.get("dxy_impact"),
        "risk_events": risk_summary,
        "upcoming_calendar": upcoming[:ANALYST_CALENDAR_MAX],
        "event_countdown": derived.get("event_countdown") or {},
        "news_topics": (derived.get("news_topics") or [])[:6],
        "social_sentiment": external.get("social_sentiment"),
        "fetch_errors": (external.get("fetch_errors") or [])[:2],
    }


def _cap_ict_events(timeframes: list[dict[str, Any]]) -> list[dict[str, Any]]:
    remaining = NARRATIVE_ICT_TOTAL
    capped: list[dict[str, Any]] = []
    for row in timeframes:
        events = list(row.get("events") or [])
        take = min(len(events), NARRATIVE_ICT_PER_TF, remaining)
        slim = {**row, "events": events[:take]}
        for key in ("order_blocks", "active_fvgs", "liquidity"):
            if key in slim and isinstance(slim[key], list):
                slim[key] = slim[key][:3]
        capped.append(slim)
        remaining -= take
        if remaining <= 0:
            break
    return capped


def _compress_technical_context(ctx: MarketContext) -> dict[str, Any]:
    technical_context = build_technical_context(ctx, event_limit=NARRATIVE_ICT_PER_TF)
    technical_context["timeframes"] = _cap_ict_events(technical_context.get("timeframes") or [])
    sr = technical_context.get("support_resistance") or {}
    for side in ("support", "resistance", "neutral"):
        if side in sr and isinstance(sr[side], list):
            sr[side] = sr[side][:5]
    technical_context["support_resistance"] = sr
    return technical_context


def build_llm_context(
    ctx: MarketContext,
    debate: ResearchDebate,
    decision: ManagerDecision,
    report: dict[str, Any],
) -> dict[str, Any]:
    """Structured facts for the LLM — no raw OHLCV arrays."""
    authorized = [
        s
        for s in report.get("signals", [])
        if s.get("signal_role") in ("primary", "alternate")
    ]
    signals = authorized[:3]
    technical_context = _compress_technical_context(ctx)
    payload = {
        "symbol": report.get("meta", {}).get("symbol", "XAUUSD"),
        "price": ctx.price,
        "metrics": ctx.metrics,
        "external": _slim_external(ctx.external.to_dict(), ctx.derived),
        "sentiment": report.get("sentiment", {}),
        "timeframes": [
            timeframe_context(tf, ctx.analyses[tf], price=ctx.price, event_limit=NARRATIVE_ICT_PER_TF)
            for tf in NARRATIVE_TIMEFRAMES
            if tf in ctx.analyses
        ],
        "technical_context": technical_context,
        "debate": {
            "consensus_bias": debate.consensus_bias,
            "consensus_strength": debate.consensus_strength,
            "discussion_notes": debate.discussion_notes[:5],
            "bullish_summary": debate.bullish.summary,
            "bearish_summary": debate.bearish.summary,
            "bullish_evidence": [i.summary for i in debate.bullish.items[:6]],
            "bearish_evidence": [i.summary for i in debate.bearish.items[:6]],
        },
        "manager_decision": decision.to_dict(),
        "authorized_only": True,
        "signals": [
            {
                "signal_id": s.get("signal_id"),
                "name": s.get("name"),
                "direction": s.get("direction"),
                "entry": f"{s.get('entry_low')}-{s.get('entry_high')}",
                "stop_loss": s.get("stop_loss"),
                "take_profits": s.get("take_profits"),
                "note": s.get("note"),
                "signal_role": s.get("signal_role"),
            }
            for s in signals
        ],
        "path_summary": report.get("path_summary", [])[:3],
        "rule_conclusion": report.get("conclusion", {}),
        "invalidation": report.get("invalidation", [])[:5],
        "price_action": report.get("price_action") or technical_context.get("price_action") or {},
        "observation_mode": report.get("meta", {}).get("observation_mode"),
        "data_as_of": report.get("meta", {}).get("data_as_of"),
    }
    payload["narrative_facts"] = build_narrative_facts_for_llm(
        report,
        ctx=ctx,
        technical_context=technical_context,
        event_limit=NARRATIVE_ICT_PER_TF,
    )
    return payload
