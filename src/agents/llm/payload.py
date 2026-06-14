"""Build compact JSON payloads for LLM agent stages."""

from __future__ import annotations

from typing import Any

from src.analysis.ict_pa import TimeframeAnalysis
from src.core.types import AgentEvidence, AnalystTeam, MarketContext


def _tf_block(tf: str, analysis: TimeframeAnalysis) -> dict[str, Any]:
    return {
        "timeframe": tf,
        "trend": analysis.trend,
        "bos": analysis.bos,
        "choch": analysis.choch,
        "premium_discount": analysis.premium_discount,
        "volume_signal": analysis.volume_signal,
        "swing_high": analysis.swing_high,
        "swing_low": analysis.swing_low,
        "events": [
            {"kind": e.kind, "direction": e.direction, "price": e.price}
            for e in analysis.events[-4:]
        ],
        "order_blocks": [
            {"direction": ob.direction, "low": ob.low, "high": ob.high}
            for ob in analysis.order_blocks[-3:]
        ],
        "active_fvgs": [
            {"direction": f.direction, "low": f.low, "high": f.high}
            for f in analysis.active_fvgs[:3]
        ],
        "liquidity": [
            {"price": lz.price, "label": lz.label}
            for lz in analysis.liquidity[:4]
        ],
    }


def analyst_team_payload(team: AnalystTeam) -> dict[str, Any]:
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
                }
                for i in getattr(team, role).items[:8]
            ],
        }
        for role in ("technical", "fundamentals", "news", "sentiment")
    }


def market_payload(ctx: MarketContext, team: AnalystTeam | None = None) -> dict[str, Any]:
    payload = {
        "symbol": "XAUUSD",
        "price": ctx.price,
        "metrics": ctx.metrics,
        "external": ctx.external.to_dict(),
        "source": ctx.source_label,
        "timeframes": [
            _tf_block(tf, ctx.analyses[tf])
            for tf in ("1d", "4h", "1h", "15m", "5m")
            if tf in ctx.analyses
        ],
    }
    if team:
        payload["analyst_team"] = analyst_team_payload(team)
    return payload


def evidence_payload(evidence: AgentEvidence) -> dict[str, Any]:
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
            }
            for i in evidence.items[:12]
        ],
    }
