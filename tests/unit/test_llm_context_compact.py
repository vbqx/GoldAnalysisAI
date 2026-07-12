"""Narrative LLM context deduplication."""

from __future__ import annotations

from src.core.types import AgentEvidence, ManagerDecision, ResearchDebate
from src.llm.context import build_llm_context, estimate_payload_size


def test_narrative_context_omits_duplicate_blobs() -> None:
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
        "meta": {"symbol": "XAUUSD"},
        "price_action": {"5m": {"volume_profile": {"poc": 4200.0}}},
        "timeframes": {"4h": {"swing_high": 4300.0}},
    }
    payload = build_llm_context(ctx, debate, decision, report)
    assert "timeframes" not in payload
    assert "price_action" not in payload
    assert "price_action" not in payload["narrative_facts"]
    meta = estimate_payload_size(payload)
    assert meta["input_tokens_est"] < 50000
