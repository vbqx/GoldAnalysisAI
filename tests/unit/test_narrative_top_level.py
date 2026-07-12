"""Top-level LLM narrative validation."""

from __future__ import annotations

from src.analysis.narrative_sections import validate_llm_top_level


def test_top_level_rejects_unapproved_price_in_action_plan() -> None:
    facts = {
        "context_levels": [{"price": 4130.0}, {"price": 4200.0}],
        "authorized_execution_levels": [{"price": 4130.0}],
        "common": {
            "primary_signal": {"theme": "short", "direction": "SELL"},
            "manager_decision": {"action": "reduce", "primary_direction": "short"},
            "sentiment": {"bearish": 60, "bullish": 30},
        },
    }
    reason = validate_llm_top_level(
        {"action_plan": "等待 4200 做空"},
        facts=facts,
    )
    assert reason is not None
    assert "unapproved" in reason


def test_top_level_rejects_executable_wording_on_wait() -> None:
    facts = {
        "context_levels": [{"price": 4130.0}],
        "authorized_execution_levels": [],
        "common": {
            "primary_signal": {"theme": "short"},
            "manager_decision": {"action": "wait", "primary_direction": "wait"},
            "sentiment": {"bearish": 60, "bullish": 30},
        },
    }
    reason = validate_llm_top_level({"action_plan": "立即入场做空"}, facts=facts)
    assert reason is not None
