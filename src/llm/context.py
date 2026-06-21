"""Serialize pipeline state into a compact narrative-only LLM context payload.

Analyst Team LLM stages use ``src.agents.llm.payload``. This module is only for
the final report narrative layer after debate/trader/risk/manager have run.
"""

from __future__ import annotations

from typing import Any

from src.analysis.technical_context import build_technical_context
from src.analysis.ict_pa import TimeframeAnalysis
from src.core.types import ManagerDecision, MarketContext, ResearchDebate


def _tf_summary(tf: str, analysis: TimeframeAnalysis) -> dict[str, Any]:
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
        "active_fvg_count": len(analysis.active_fvgs),
        "order_block_count": len(analysis.order_blocks),
        "active_fvgs": [
            {"direction": fvg.direction, "low": fvg.low, "high": fvg.high}
            for fvg in analysis.active_fvgs[:3]
        ],
        "order_blocks": [
            {"direction": ob.direction, "low": ob.low, "high": ob.high}
            for ob in analysis.order_blocks[-3:]
        ],
        "liquidity": [
            {
                "price": lz.price,
                "kind": lz.kind,
                "label": lz.label,
                "strength": lz.strength,
                "swept": lz.swept,
            }
            for lz in analysis.liquidity[:4]
        ],
    }


def build_llm_context(
    ctx: MarketContext,
    debate: ResearchDebate,
    decision: ManagerDecision,
    report: dict[str, Any],
) -> dict[str, Any]:
    """Structured facts for the LLM — no raw OHLCV arrays."""
    signals = report.get("signals", [])[:5]
    technical_context = build_technical_context(ctx)
    return {
        "symbol": report.get("meta", {}).get("symbol", "XAUUSD"),
        "price": ctx.price,
        "metrics": ctx.metrics,
        "external": ctx.external.to_dict(),
        "sentiment": report.get("sentiment", {}),
        "timeframes": [
            _tf_summary(tf, ctx.analyses[tf])
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
    }
