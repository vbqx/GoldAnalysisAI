"""Serialize pipeline state into a compact narrative-only LLM context payload.

Analyst Team LLM stages use ``src.agents.llm.payload``. This module is only for
the final report narrative layer after debate/trader/risk/manager have run.
"""

from __future__ import annotations

from typing import Any

from src.analysis.technical_context import build_technical_context, timeframe_context
from src.analysis.narrative_sections import build_narrative_facts
from src.core.types import ManagerDecision, MarketContext, ResearchDebate


def build_llm_context(
    ctx: MarketContext,
    debate: ResearchDebate,
    decision: ManagerDecision,
    report: dict[str, Any],
) -> dict[str, Any]:
    """Structured facts for the LLM — no raw OHLCV arrays."""
    signals = report.get("signals", [])[:5]
    technical_context = build_technical_context(ctx)
    payload = {
        "symbol": report.get("meta", {}).get("symbol", "XAUUSD"),
        "price": ctx.price,
        "metrics": ctx.metrics,
        "external": ctx.external.to_dict(),
        "sentiment": report.get("sentiment", {}),
        "timeframes": [
            timeframe_context(tf, ctx.analyses[tf], price=ctx.price)
            for tf in ("1d", "4h", "1h", "15m", "5m")
            if tf in ctx.analyses
        ],
        "technical_context": technical_context,
        "debate": {
            "consensus_bias": debate.consensus_bias,
            "consensus_strength": debate.consensus_strength,
            "discussion_notes": debate.discussion_notes,
            "bullish_summary": debate.bullish.summary,
            "bearish_summary": debate.bearish.summary,
            "bullish_evidence": [i.summary for i in debate.bullish.items[:8]],
            "bearish_evidence": [i.summary for i in debate.bearish.items[:8]],
        },
        "manager_decision": decision.to_dict(),
        "signals": [
            {
                "name": s.get("name"),
                "direction": s.get("direction"),
                "entry": f"{s.get('entry_low')}-{s.get('entry_high')}",
                "stop_loss": s.get("stop_loss"),
                "take_profits": s.get("take_profits"),
                "note": s.get("note"),
            }
            for s in signals
        ],
        "path_summary": report.get("path_summary", [])[:3],
        "rule_conclusion": report.get("conclusion", {}),
        "invalidation": report.get("invalidation", [])[:5],
        "price_action": report.get("price_action") or technical_context.get("price_action") or {},
    }
    payload["narrative_facts"] = build_narrative_facts(report, technical_context)
    return payload
