"""Narrative authorization boundary and calendar filter tests."""

from __future__ import annotations

from datetime import datetime, timedelta

from src.agents.llm.payload import fundamentals_analyst_payload
from src.analysis.narrative_sections import validate_llm_top_level
from src.core.types import CalendarEvent, ExternalFactors, MarketContext
from src.data.calendar_utils import filter_upcoming_calendar_events
from src.data.external_format import sync_external_legacy_fields


def _facts_with_split_levels() -> dict:
    return {
        "context_levels": [{"price": 4130.0}, {"price": 4200.0}],
        "authorized_execution_levels": [
            {"price": 4130.0, "signal_id": "sig-a"},
            {"price": 4132.0, "signal_id": "sig-a"},
        ],
        "common": {
            "primary_signal": {"theme": "short", "direction": "SELL"},
            "manager_decision": {"action": "reduce", "primary_direction": "short"},
            "sentiment": {"bearish": 60, "bullish": 30},
        },
    }


def test_action_plan_rejects_reference_level_not_in_authorized_execution() -> None:
    reason = validate_llm_top_level(
        {"action_plan": "等待 4200 入场做空"},
        facts=_facts_with_split_levels(),
    )
    assert reason is not None
    assert "4200" in reason or "unapproved" in reason


def test_market_summary_allows_reference_level_outside_execution() -> None:
    reason = validate_llm_top_level(
        {
            "market_summary": "上方 4200 为观察阻力",
            "action_plan": "在 4130-4132 区间按授权计划做空",
        },
        facts=_facts_with_split_levels(),
    )
    assert reason is None


def test_expired_calendar_removed_from_fundamentals_payload() -> None:
    old_time = (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d %H:%M")
    ext = ExternalFactors(
        calendar_events=[
            CalendarEvent(time=old_time, region="US", event="CPI", importance=5.0),
        ],
        risk_events="legacy stale CPI text",
    )
    sync_external_legacy_fields(ext)
    ctx = MarketContext(
        price=2650.0,
        metrics={"current_price": 2650.0},
        enriched={},
        analyses={},
        external=ext,
        derived={},
        context_stats={},
        source_label="test",
    )
    ctx.external.calendar_events = filter_upcoming_calendar_events(ext.calendar_events)
    sync_external_legacy_fields(ctx.external)
    ctx.derived = {
        "calendar_high_impact_count": 0,
        "upcoming_calendar": [],
        "event_countdown": {},
    }
    payload = fundamentals_analyst_payload(ctx)
    assert payload["upcoming_calendar"] == []
    assert "CPI" not in str(payload.get("risk_events", ""))


def test_context_builder_imports_without_cycle() -> None:
    import importlib

    importlib.import_module("src.data.context_builder")
