"""Serialize pipeline state into a compact narrative-only LLM context payload.

Analyst Team LLM stages use ``src.agents.llm.payload``. This module is only for
the final report narrative layer after debate/trader/risk/manager have run.

Numeric facts must be cited via ``fact_registry`` fact_id — raw OHLC duplicates
are intentionally omitted (Report Trust #29).
"""

from __future__ import annotations

import json
from typing import Any

from src.analysis.fact_registry import compact_fact_index, fact_ids_for_signal
from src.analysis.narrative_facts import (
    NARRATIVE_ICT_PER_TF,
    build_narrative_facts_for_llm,
)
from src.analysis.technical_context import build_technical_context
from src.config import ANALYST_CALENDAR_MAX
from src.core.types import ManagerDecision, MarketContext, ResearchDebate

NARRATIVE_ICT_TOTAL = NARRATIVE_ICT_PER_TF * 3


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


def _slim_narrative_technical_context(ctx: MarketContext) -> dict[str, Any]:
    """Quality + S/R labels only — indicator raw numbers live in fact_registry."""
    full = build_technical_context(ctx, event_limit=NARRATIVE_ICT_PER_TF)
    sr = full.get("support_resistance") or {}
    for side in ("support", "resistance", "neutral"):
        if side in sr and isinstance(sr[side], list):
            sr[side] = [
                {k: row[k] for k in ("label", "timeframe", "kind") if k in row}
                for row in sr[side][:5]
            ]
    return {
        "quality": full.get("quality"),
        "support_resistance": sr,
    }


def _levels_as_fact_refs(levels: list[dict[str, Any]], registry: dict[str, Any]) -> list[dict[str, Any]]:
    from src.analysis.fact_registry import fact_lookup

    out: list[dict[str, Any]] = []
    for row in levels:
        price = row.get("price")
        refs: dict[str, Any] = {"role": row.get("role"), "label": row.get("label")}
        if price is not None:
            matches = fact_lookup(registry, float(price))
            if matches:
                refs["fact_ids"] = matches
            else:
                refs["unregistered_price"] = price
        out.append(refs)
    return out


def _slim_narrative_facts(facts: dict[str, Any], registry: dict[str, Any]) -> dict[str, Any]:
    slim = dict(facts)
    if "context_levels" in slim:
        slim["context_levels"] = _levels_as_fact_refs(slim.get("context_levels") or [], registry)
    if "authorized_execution_levels" in slim:
        slim["authorized_execution_levels"] = _levels_as_fact_refs(
            slim.get("authorized_execution_levels") or [], registry
        )
    return slim


def estimate_payload_size(payload: dict[str, Any]) -> dict[str, int]:
    raw = json.dumps(payload, ensure_ascii=False, default=str)
    chars = len(raw)
    return {"input_chars": chars, "input_tokens_est": round(chars / 1.8)}


def build_llm_context(
    ctx: MarketContext,
    debate: ResearchDebate,
    decision: ManagerDecision,
    report: dict[str, Any],
) -> dict[str, Any]:
    """Structured facts for the LLM — cite fact_id; no duplicate raw price tables."""
    authorized = [
        s
        for s in report.get("signals", [])
        if s.get("signal_role") in ("primary", "alternate")
    ]
    signals = authorized[:3]
    registry = (report.get("meta") or {}).get("fact_registry") or {}
    technical_context = _slim_narrative_technical_context(ctx)
    payload: dict[str, Any] = {
        "symbol": report.get("meta", {}).get("symbol", "XAUUSD"),
        "price_fact_id": "metrics.current_price",
        "metric_fact_ids": {
            "current_price": "metrics.current_price",
            "daily_low": "metrics.daily_low",
            "daily_high": "metrics.daily_high",
            "prev_close": "metrics.prev_close",
        },
        "sentiment_fact_ids": {
            "bullish": "sentiment.bullish",
            "bearish": "sentiment.bearish",
            "ranging": "sentiment.ranging",
        },
        "external": _slim_external(ctx.external.to_dict(), ctx.derived),
        "technical_context": technical_context,
        "debate": {
            "consensus_bias": debate.consensus_bias,
            "consensus_strength": debate.consensus_strength,
            "discussion_notes": debate.discussion_notes[:5],
            "bullish_summary": debate.bullish.summary,
            "bearish_summary": debate.bearish.summary,
            "bullish_evidence": [
                {"evidence_id": i.evidence_id, "summary": i.summary, "refs": i.refs}
                for i in debate.bullish.items[:6]
            ],
            "bearish_evidence": [
                {"evidence_id": i.evidence_id, "summary": i.summary, "refs": i.refs}
                for i in debate.bearish.items[:6]
            ],
        },
        "manager_decision": decision.to_dict(),
        "authorized_only": True,
        "signals": [
            fact_ids_for_signal(s, registry)
            | {
                "name": s.get("name"),
                "direction": s.get("direction"),
                "signal_role": s.get("signal_role"),
                "note": s.get("note"),
            }
            for s in signals
        ],
        "path_summary": report.get("path_summary", [])[:3],
        "rule_conclusion": report.get("conclusion", {}),
        "invalidation": report.get("invalidation", [])[:5],
        "observation_mode": report.get("meta", {}).get("observation_mode"),
        "data_as_of": report.get("meta", {}).get("data_as_of"),
    }
    narrative_facts = build_narrative_facts_for_llm(
        report,
        ctx=ctx,
        technical_context=technical_context,
        event_limit=NARRATIVE_ICT_PER_TF,
        compact_for_llm=True,
    )
    payload["narrative_facts"] = _slim_narrative_facts(narrative_facts, registry)
    if registry:
        payload["fact_registry"] = {
            "version": registry.get("version"),
            "as_of": registry.get("as_of"),
            "source": registry.get("source"),
            "facts": compact_fact_index(registry),
            "usage": "所有价位/指标必须引用 fact_id；禁止自造数字",
        }
    payload["context_meta"] = estimate_payload_size(payload)
    return payload
