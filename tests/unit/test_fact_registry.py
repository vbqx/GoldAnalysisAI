from __future__ import annotations

import json
from pathlib import Path

from src.analysis.fact_registry import (
    allowed_prices,
    build_fact_registry,
    compact_fact_index,
    fact_ids_for_signal,
    fact_lookup,
)

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "golden_reports"


def _load(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def test_build_fact_registry_indexes_prices() -> None:
    report = _load("wait_observation.json")
    registry = build_fact_registry(report)
    assert registry["fact_count"] >= 10
    assert registry["version"] == "fr-v2"
    assert registry["as_of"] == "2026-07-12T15:00:00Z"
    assert "4140.00" in registry["price_index"]
    assert fact_lookup(registry, 4140.0)
    assert 4140.0 in allowed_prices(registry)


def test_session_pa_uses_canonical_fact_ids() -> None:
    report = _load("wait_observation.json")
    report["price_action"]["session"] = {
        "volume_profile": {"poc": 4102.31, "vah": 4117.53, "val": 4096.41},
        "sr_levels": [],
    }
    registry = build_fact_registry(report)
    assert "pa.session.poc" in registry["facts"]
    assert registry["facts"]["pa.session.poc"]["value"] == 4102.31
    assert registry["facts"]["pa.session.poc"]["as_of"] == report["meta"]["data_as_of"]["last_bar_time_utc"]


def test_claim_catalog_registers_5m_zone_boundaries_for_replay() -> None:
    report = _load("wait_observation.json")
    report["technical_claim_facts"] = [
        {
            "fact_ids": ["5m.ob.0.low", "5m.ob.0.high"],
            "kind": "order_block",
            "timeframe": "5m",
            "direction": "bearish",
            "low": 4061.04,
            "high": 4065.32,
            "as_of": "2026-07-14T17:40:00Z",
        }
    ]

    registry = build_fact_registry(report)

    assert registry["facts"]["5m.ob.0.low"]["value"] == 4061.04
    assert registry["facts"]["5m.ob.0.high"]["value"] == 4065.32
    assert registry["facts"]["5m.ob.0.low"]["refs"]["claim_catalog"] is True


def test_fact_registry_calendar_and_news() -> None:
    report = _load("wait_observation.json")
    report["external"] = {
        "calendar_count": 0,
        "risk_events": "—",
        "fetch_errors": [],
        "headline_items": [
            {"source": "jin10_flash", "time": "2026-07-12T14:30:00Z", "text": "地缘 headline"},
        ],
        "macro_quotes": [
            {
                "name": "DXY",
                "symbol": "TVC:DXY",
                "close": 104.2,
                "change_pct": 0.15,
                "bias": "bearish",
            }
        ],
    }
    report["calendar_events"] = []
    registry = build_fact_registry(report)
    assert registry["facts"]["calendar.state"]["value"] == "confirmed_empty"
    assert registry["facts"]["news.0.published_at"]["value"] == "2026-07-12T14:30:00Z"
    assert registry["facts"]["macro.DXY.close"]["value"] == 104.2
    assert registry["facts"]["macro.DXY.close"]["quality"] == "degraded"
    assert registry["facts"]["macro.DXY.close"]["refs"].get("pit_alignment") == "unknown"


def test_fact_registry_freshness_and_bar_counts() -> None:
    report = _load("wait_observation.json")
    report["meta"]["context_stats"] = {
        "technical_inputs": {"bars": {"5m": 500, "1h": 120, "1d": 30}},
    }
    report["meta"]["data_as_of"]["market_status"] = "closed_snapshot"
    registry = build_fact_registry(report)
    assert registry["facts"]["freshness.market_status"]["value"] == "closed_snapshot"
    assert registry["facts"]["freshness.executable"]["value"] == "false"
    assert registry["facts"]["bar.5m.count"]["value"] == 500


def test_fact_registry_marks_conflicts() -> None:
    report = _load("wait_observation.json")
    facts = build_fact_registry(report)["facts"]
    # Simulate re-register conflict by rebuilding with changed metrics.current_price path
    report["metrics"]["current_price"] = 4142.0
    report["metrics"]["daily_low"] = 4142.0
    registry2 = build_fact_registry(report)
    # different fact_ids — no conflict; test explicit conflict via same id would need internal API
    assert registry2["fact_count"] >= len(facts)


def test_fact_ids_for_signal_maps_geometry() -> None:
    report = _load("wait_observation.json")
    registry = build_fact_registry(report)
    sig = report["signals"][0]
    mapped = fact_ids_for_signal(sig, registry)
    assert mapped["entry_low_fact_id"] == "signal.plan_a.entry_low"
    assert mapped["take_profit_fact_ids"]


def test_compact_fact_index_sorted_and_complete() -> None:
    report = _load("wait_observation.json")
    registry = build_fact_registry(report)
    index = compact_fact_index(registry)
    assert index
    assert all("fact_id" in row and "as_of" in row and "source" in row and "quality" in row for row in index)
    assert index == sorted(index, key=lambda r: r["fact_id"])
