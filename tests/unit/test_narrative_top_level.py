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


def test_top_level_rejects_chase_wording_on_wait() -> None:
    facts = {
        "context_levels": [{"price": 4103.0}, {"price": 4072.0}],
        "authorized_execution_levels": [],
        "common": {
            "primary_signal": {"theme": "short"},
            "manager_decision": {"action": "wait", "primary_direction": "wait"},
            "sentiment": {"bearish": 60, "bullish": 30},
        },
    }
    reason = validate_llm_top_level(
        {"action_plan": "若价格跌破4103，可追空至4072附近"},
        facts=facts,
    )
    assert reason is not None


def test_top_level_allows_observation_action_plan_on_wait() -> None:
    facts = {
        "context_levels": [{"price": 4130.0}, {"price": 4200.0}],
        "authorized_execution_levels": [],
        "common": {
            "primary_signal": {"theme": "short"},
            "manager_decision": {"action": "wait", "primary_direction": "wait"},
            "sentiment": {"bearish": 60, "bullish": 30},
        },
    }
    reason = validate_llm_top_level(
        {
            "market_summary": "价格靠近 4130 支撑，等待结构确认",
            "trade_thesis": "偏空但需等待入场区确认后再评估",
            "action_plan": "观望：4200 上方阻力未破则维持观察",
        },
        facts=facts,
    )
    assert reason is None


def test_top_level_allows_round_integer_near_spot() -> None:
    """Archive 20260713T172427Z: LLM wrote 4000 while spot was 3998.5."""
    facts = {
        "context_levels": [{"price": 3998.5}, {"price": 4049.9}],
        "authorized_execution_levels": [
            {"price": 4044.5},
            {"price": 4046.5},
            {"price": 4048.5},
            {"price": 4054.5},
        ],
        "common": {
            "primary_signal": {"theme": "short", "direction": "SELL"},
            "manager_decision": {"action": "reduce", "primary_direction": "short"},
            "sentiment": {"bearish": 100, "bullish": 0},
        },
    }
    reason = validate_llm_top_level(
        {
            "market_summary": "金价失守4000关口；美元指数偏强（101.23）仍可写非金价数字",
            "trade_thesis": "主方向偏空，止损放在4054.5上方",
            "action_plan": "反抽至4046.4附近评估做空",
        },
        facts=facts,
    )
    assert reason is None


def test_top_level_partial_field_audit() -> None:
    from src.analysis.narrative_sections import validate_llm_top_level_fields

    facts = {
        "context_levels": [{"price": 4130.0}, {"price": 4200.0}],
        "authorized_execution_levels": [{"price": 4130.0}],
        "common": {
            "primary_signal": {"theme": "short", "direction": "SELL"},
            "manager_decision": {"action": "reduce", "primary_direction": "short"},
            "sentiment": {"bearish": 60, "bullish": 30},
        },
    }
    reasons = validate_llm_top_level_fields(
        {
            "market_summary": "上方 4200 为观察阻力",
            "action_plan": "等待 4200 做空",
        },
        facts=facts,
    )
    assert reasons["market_summary"] is None
    assert reasons["action_plan"] is not None
