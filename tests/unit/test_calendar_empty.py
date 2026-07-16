"""Issue #38 — empty calendar must not become verified placeholder risk."""

from __future__ import annotations

from src.analysis.fact_registry import build_fact_registry, calendar_state
from src.analysis.narrative_sections import (
    _unapproved_calendar_claims,
    validate_llm_top_level_fields,
)
from src.analysis.report_engine import build_calendar_events, calendar_rows_from_external
from src.core.types import CalendarEvent


def test_build_calendar_events_no_placeholders() -> None:
    assert build_calendar_events() == []


def test_empty_calendar_confirmed_empty_in_registry() -> None:
    report = {
        "calendar_events": build_calendar_events(),
        "external": {"risk_events": "—", "calendar_count": 0, "fetch_errors": []},
        "meta": {"data_as_of": {"last_bar_time_utc": "2026-07-16 04:15 UTC"}},
        "metrics": {"current_price": 4000.0},
        "signals": [],
        "timeframes": {},
    }
    assert report["calendar_events"] == []
    assert calendar_state(report) == "confirmed_empty"
    registry = build_fact_registry(report)
    assert registry["facts"]["calendar.state"]["value"] == "confirmed_empty"
    assert registry["facts"]["calendar.state"]["quality"] == "verified"
    assert not any(k.startswith("calendar.event.") for k in registry["facts"])


def test_placeholder_rows_ignored_when_calendar_count_zero() -> None:
    report = {
        "calendar_events": [
            {"time": "22:45", "flag": "🇺🇸", "event": "美联储官员讲话 (关注)"},
        ],
        "external": {"risk_events": "—", "calendar_count": 0, "fetch_errors": []},
        "meta": {},
        "metrics": {"current_price": 4000.0},
        "signals": [],
        "timeframes": {},
    }
    assert calendar_state(report) == "confirmed_empty"


def test_calendar_rows_from_structured_events() -> None:
    rows = calendar_rows_from_external(
        calendar_events=[
            CalendarEvent(time="2026-07-16 14:30", region="US", event="CPI YoY", importance=3.0),
        ],
        risk_events="—",
    )
    assert len(rows) == 1
    assert "CPI" in rows[0]["event"]
    assert rows[0]["flag"] == "🇺🇸"


def test_narrative_rejects_unregistered_calendar_claim() -> None:
    hit = _unapproved_calendar_claims(
        "美联储官员讲话（22:45）引发波动",
        calendar_state="confirmed_empty",
        allowed_times=set(),
    )
    assert hit and "22:45" in hit

    reasons = validate_llm_top_level_fields(
        {
            "market_summary": "美联储官员讲话（22:45）引发波动，短线观望。",
            "trade_thesis": "结构偏空。",
            "action_plan": "等待触发。",
        },
        facts={
            "common": {
                "calendar_state": "confirmed_empty",
                "allowed_calendar_times": [],
                "execution_authorized": False,
                "manager_decision": {"action": "wait"},
                "primary_signal": {},
            },
            "context_levels": [{"price": 4000.0}],
            "authorized_execution_levels": [],
        },
    )
    assert reasons["market_summary"] and "calendar" in reasons["market_summary"]
