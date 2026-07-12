"""LLM context uses fact_id references without duplicate raw prices."""

from __future__ import annotations

from src.analysis.fact_registry import build_fact_registry
from src.core.types import AgentEvidence, ManagerDecision, ResearchDebate
from src.llm.context import build_llm_context


def test_narrative_context_uses_fact_ids_not_raw_metrics() -> None:
    from tests.unit.test_analyst_input_density import _technical_ctx

    ctx = _technical_ctx()
    evidence = AgentEvidence(agent="test", direction="neutral", items=[], confidence=0.5, summary="ok")
    debate = ResearchDebate(
        bullish=evidence,
        bearish=evidence,
        consensus_bias="neutral",
        consensus_strength=0.5,
        discussion_notes=[],
    )
    decision = ManagerDecision(
        action="wait",
        primary_direction="wait",
        selected_signal_indices=[],
        confidence=0.5,
        summary="wait",
    )
    report = {
        "meta": {"symbol": "XAUUSD", "observation_mode": True},
        "metrics": {"current_price": 4200.0, "daily_low": 4180.0},
        "sentiment": {"bullish": 30, "bearish": 50, "ranging": 20},
        "price_action": {"5m": {"volume_profile": {"poc": 4200.0}}},
        "timeframes": {"4h": {"swing_high": 4300.0}},
        "signals": [
            {
                "signal_id": "plan_a",
                "name": "test",
                "direction": "short",
                "entry_low": 4210.0,
                "entry_high": 4220.0,
                "stop_loss": 4230.0,
                "take_profits": [4190.0],
                "signal_role": "primary",
            }
        ],
    }
    report["meta"]["fact_registry"] = build_fact_registry(report)
    payload = build_llm_context(ctx, debate, decision, report)
    assert "price" not in payload
    assert "metrics" not in payload
    assert payload["price_fact_id"] == "metrics.current_price"
    assert payload["signals"][0].get("entry_low_fact_id")
    assert "entry_low" not in payload["signals"][0]
    assert payload["fact_registry"]["facts"]
