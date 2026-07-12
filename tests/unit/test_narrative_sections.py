from __future__ import annotations

from copy import deepcopy

from src.analysis.narrative_sections import (
    SECTION_KEYS,
    build_narrative_facts,
    build_rule_narrative_sections,
    validate_and_merge_llm_sections,
)
from src.llm.analyst import _error_result, apply_llm_to_report


def _report() -> dict:
    tf = {
        "trend": "bearish",
        "premium_discount": "premium",
        "bos": "bearish @ 4148",
        "choch": "none",
        "swing_high": 4175.0,
        "swing_low": 4122.0,
        "order_blocks": [{"direction": "bearish", "low": 4148.0, "high": 4160.0}],
        "fvgs": [{"direction": "bullish", "low": 4122.0, "high": 4135.0}],
    }
    return {
        "metrics": {"current_price": 4140.0, "daily_low": 4135.0, "daily_high": 4160.0},
        "sentiment": {"bullish": 32.0, "bearish": 55.0, "ranging": 13.0},
        "conclusion": {"action": "等待反抽确认", "direction_summary": "反抽失败后偏空"},
        "timeframes": {"4h": deepcopy(tf), "1h": deepcopy(tf), "15m": deepcopy(tf)},
        "liquidity": [
            {"price": 4148.0, "kind": "swing_high", "label": "上方流动性", "timeframe": "15m"},
            {"price": 4135.0, "kind": "swing_low", "label": "下方流动性", "timeframe": "15m"},
        ],
        "signals": [{
            "direction": "short", "theme": "short", "entry_low": 4148.0, "entry_high": 4160.0,
            "stop_loss": 4175.0, "take_profits": [4135.0, 4122.0], "status": "candidate",
        }],
        "price_action": {
            "5m": {
                "volume_ok": True,
                "volume_spike_count": 2,
                "high_volatility_count": 3,
                "volume_profile": {"poc": 4140.0, "vah": 4155.0, "val": 4125.0},
                "sr_levels": [
                    {"price": 4150.0, "direction": "resistance", "label": "量价连续阻力", "kind": "consecutive_sr"},
                    {"price": 4130.0, "direction": "support", "label": "量价连续支撑", "kind": "consecutive_sr"},
                ],
            },
            "4h": {"volume_ok": True, "volume_profile": {"poc": 4142.0, "vah": 4160.0, "val": 4120.0}, "sr_levels": []},
            "1h": {"volume_ok": True, "volume_profile": {"poc": 4141.0, "vah": 4158.0, "val": 4122.0}, "sr_levels": []},
            "15m": {"volume_ok": True, "volume_profile": {"poc": 4140.0, "vah": 4155.0, "val": 4128.0}, "sr_levels": []},
        },
    }


def _candidate(confidence: float = 0.8) -> dict:
    return {
        key: {
            "summary": "当前结构偏空。",
            "context": ["反弹仍受压。"],
            "levels": ["关注4148-4160压力。"],
            "conditions": ["若4148反抽失败，则观察回落。"],
            "invalidation": "有效站上4175后失效。",
            "source": "llm",
            "confidence": confidence,
        }
        for key in SECTION_KEYS
    }


def test_rule_sections_have_shared_contract_and_screenshot_density() -> None:
    sections = build_rule_narrative_sections(_report())
    assert tuple(sections) == SECTION_KEYS
    assert all(section["source"] == "rule" for section in sections.values())
    for section in sections.values():
        visible = 1 + len(section["context"]) + len(section["levels"]) + len(section["conditions"]) + 1
        assert 3 <= visible <= 6
    assert "量价" in sections["liquidity"]["context"][0]
    assert "POC" in sections["4h"]["context"][0] or "量价" in sections["4h"]["context"][0]
    assert "SMC" not in sections["15m"]["context"][0]
    assert "现价不追单" in sections["15m"]["conditions"][0]


def test_rule_sections_degrade_to_wait_when_structure_is_ranging() -> None:
    report = _report()
    for info in report["timeframes"].values():
        info["trend"] = "ranging"
        info["order_blocks"] = []
        info["fvgs"] = []
    sections = build_rule_narrative_sections(report)
    assert "待确认" in sections["market_overview"]["summary"] or "震荡" in sections["market_overview"]["summary"]
    assert "保持等待" in sections["4h"]["conditions"][0]


def test_llm_sections_are_accepted_per_block_in_llm_mode() -> None:
    report = _report()
    rules = build_rule_narrative_sections(report)
    facts = build_narrative_facts(report, {"quality": {"score": 1.0}})
    merged, audit = validate_and_merge_llm_sections(
        _candidate(), rule_sections=rules, facts=facts, mode="llm", threshold=0.65,
    )
    assert all(section["source"] == "llm" for section in merged.values())
    assert all(row["accepted"] for row in audit.values())


def test_hybrid_falls_back_only_low_confidence_block() -> None:
    report = _report()
    rules = build_rule_narrative_sections(report)
    facts = build_narrative_facts(report, {"quality": {"score": 1.0}})
    candidate = _candidate()
    candidate["1h"]["confidence"] = 0.5
    merged, audit = validate_and_merge_llm_sections(
        candidate, rule_sections=rules, facts=facts, mode="hybrid", threshold=0.65,
    )
    assert merged["1h"]["source"] == "fallback"
    assert merged["4h"]["source"] == "llm"
    assert "confidence" in audit["1h"]["fallback_reason"]


def test_unapproved_price_and_direction_conflict_fall_back() -> None:
    report = _report()
    rules = build_rule_narrative_sections(report)
    facts = build_narrative_facts(report, {"quality": {"score": 1.0}})
    candidate = _candidate()
    candidate["liquidity"]["levels"] = ["关注9999压力。"]
    candidate["15m"]["summary"] = "主方向偏多。"
    merged, audit = validate_and_merge_llm_sections(
        candidate, rule_sections=rules, facts=facts, mode="llm", threshold=0.65,
    )
    assert merged["liquidity"]["source"] == "fallback"
    assert audit["liquidity"]["fallback_reason"] == "unapproved price 9999"
    assert merged["15m"]["source"] == "fallback"
    assert "direction conflicts" in audit["15m"]["fallback_reason"]


def test_llm_section_accepts_overlong_lists_after_display_caps() -> None:
    """LLM often returns extra list items; merge truncates instead of falling back."""
    report = _report()
    rules = build_rule_narrative_sections(report)
    facts = build_narrative_facts(report, {"quality": {"score": 1.0}})
    candidate = _candidate()
    candidate["1h"]["context"] = ["背景一", "背景二", "背景三"]
    candidate["1h"]["levels"] = ["4130", "4140", "4150", "4160"]
    candidate["1h"]["conditions"] = ["条件一", "条件二", "条件三"]
    merged, audit = validate_and_merge_llm_sections(
        candidate, rule_sections=rules, facts=facts, mode="llm", threshold=0.65,
    )
    assert merged["1h"]["source"] == "llm"
    assert audit["1h"]["accepted"] is True
    assert merged["1h"]["context"] == ["背景一"]
    assert merged["1h"]["levels"] == ["4130", "4140"]
    assert merged["1h"]["conditions"] == ["条件一"]


def test_missing_overlong_or_win_rate_sections_fall_back_independently() -> None:
    report = _report()
    rules = build_rule_narrative_sections(report)
    facts = build_narrative_facts(report, {"quality": {"score": 1.0}})
    candidate = _candidate()
    del candidate["4h"]
    candidate["1h"]["context"] = ["a", "b", "c"]
    candidate["15m"]["summary"] = "结构胜率55%。"
    merged, _ = validate_and_merge_llm_sections(
        candidate, rule_sections=rules, facts=facts, mode="llm", threshold=0.65,
    )
    assert merged["market_overview"]["source"] == "llm"
    assert merged["4h"]["source"] == "fallback"
    assert merged["1h"]["source"] == "llm"
    assert merged["1h"]["context"] == ["a"]
    assert merged["15m"]["source"] == "fallback"


def test_llm_transport_error_keeps_complete_rule_copy_as_fallback() -> None:
    report = _report()
    report["meta"] = {"stage_sources": {}}
    report["narrative_sections"] = build_rule_narrative_sections(report)
    result = _error_result(report, "network timeout")
    apply_llm_to_report(report, result)
    assert set(report["narrative_sections"]) == set(SECTION_KEYS)
    assert all(section["source"] == "fallback" for section in report["narrative_sections"].values())
    assert report["meta"]["stage_sources"]["narrative_sections"]["4h"]["fallback_reason"] == "network timeout"
