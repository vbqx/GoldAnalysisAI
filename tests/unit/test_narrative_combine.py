"""Tests for SMC + PA narrative combination."""

from __future__ import annotations

from src.analysis.narrative_combine import build_pa_llm_summary, entry_resonance_text
from src.analysis.narrative_sections import build_narrative_facts, build_rule_narrative_sections


def _minimal_report() -> dict:
    return {
        "metrics": {"current_price": 4120.0, "daily_low": 4072.8, "daily_high": 4134.92},
        "conclusion": {
            "action": "不追多，优先等待反弹至阻力区做空",
            "direction_summary": "主方向偏空，当前处于逆势反弹阶段",
        },
        "sentiment": {"bearish": 55, "bullish": 30, "ranging": 15},
        "signals": [
            {
                "entry_low": 4136.0,
                "entry_high": 4139.0,
                "status": "candidate",
                "theme": "short",
            }
        ],
        "liquidity": [
            {"price": 4134.0, "timeframe": "4h", "kind": "swing_high"},
            {"price": 4075.0, "timeframe": "4h", "kind": "swing_low"},
        ],
        "timeframes": {
            "4h": {"trend": "bearish", "bos": "bearish @ 4150", "choch": "无", "premium_discount": "discount",
                   "order_blocks": [{"low": 4135, "high": 4140, "direction": "bearish"}],
                   "fvgs": [], "swing_high": 4150, "swing_low": 4070},
            "1h": {"trend": "bearish", "bos": "无", "choch": "无", "premium_discount": "discount",
                   "order_blocks": [], "fvgs": [], "swing_high": 4145, "swing_low": 4080},
            "15m": {"trend": "ranging", "bos": "无", "choch": "无", "premium_discount": "equilibrium",
                    "order_blocks": [], "fvgs": [], "swing_high": 4138, "swing_low": 4100},
        },
        "price_action": {
            "5m": {
                "volume_ok": True,
                "sr_levels": [
                    {"price": 4137.0, "direction": "resistance", "kind": "consecutive_sr", "label": "量价连续阻力", "time": "2026-01-01T00:00:00"},
                ],
                "volume_profile": {"poc": 4125.0, "vah": 4138.0, "val": 4122.0},
            },
            "4h": {"volume_ok": True, "volume_profile": {"poc": 4125.0, "vah": 4138.0, "val": 4122.0}, "sr_levels": []},
            "1h": {"volume_ok": True, "volume_profile": {"poc": 4125.0, "vah": 4138.0, "val": 4122.0}, "sr_levels": []},
            "15m": {"volume_ok": True, "volume_profile": {"poc": 4125.0, "vah": 4138.0, "val": 4122.0}, "sr_levels": []},
        },
    }


def test_market_overview_prefers_session_day_poc() -> None:
    report = _minimal_report()
    report["price_action"]["session"] = {
        "timeframe": "session",
        "volume_profile": {"poc": 4100.0, "vah": 4110.0, "val": 4090.0},
        "sr_levels": [],
    }
    report["price_action"]["15m"]["volume_profile"] = {"poc": 4125.0, "vah": 4138.0, "val": 4122.0}
    report["price_action"]["5m"]["volume_profile"] = {"poc": 9999.0, "vah": 9998.0, "val": 9997.0}
    ov = build_rule_narrative_sections(report)["market_overview"]
    text = " ".join([ov["summary"], *ov.get("levels", [])])
    assert "当日 POC" in text
    assert "4100" in text
    assert "4125" not in text
    assert "9999" not in text


def test_market_overview_uses_15m_volume_profile_not_5m() -> None:
    report = _minimal_report()
    report["price_action"]["5m"]["volume_profile"] = {"poc": 9999.0, "vah": 9998.0, "val": 9997.0}
    report["price_action"]["15m"]["volume_profile"] = {"poc": 4125.0, "vah": 4138.0, "val": 4122.0}
    ov = build_rule_narrative_sections(report)["market_overview"]
    text = " ".join([ov["summary"], *ov.get("levels", [])])
    assert "4125" in text
    assert "9999" not in text
    assert "15m POC" in text


def test_narrative_combines_smc_and_pa_in_overview() -> None:
    sections = build_rule_narrative_sections(_minimal_report())
    ov = sections["market_overview"]
    text = " ".join([ov["summary"], *ov.get("levels", [])])
    assert "震荡" in ov["summary"] or "偏空" in ov["summary"] or "偏空" in text
    assert "POC" in text
    assert "PA 入场区" in text
    assert "4136" in text


def test_narrative_liquidity_uses_intraday_pa_not_5m() -> None:
    report = _minimal_report()
    report["price_action"]["session"] = {
        "timeframe": "session",
        "volume_profile": {"poc": 4125.0, "vah": 4138.0, "val": 4122.0},
        "sr_levels": [
            {"price": 4137.0, "direction": "resistance", "label": "量价连续阻力", "kind": "consecutive_sr"},
        ],
    }
    report["price_action"]["5m"]["sr_levels"] = [
        {"price": 9999.0, "direction": "resistance", "label": "5m不应出现", "kind": "consecutive_sr"},
    ]
    sections = build_rule_narrative_sections(report)
    liq = sections["liquidity"]
    levels_text = " ".join(liq.get("levels", []))
    context = liq.get("context", [""])[0]
    assert "量价" in levels_text or "4137" in levels_text
    assert "9999" not in levels_text
    assert "5m" not in context
    assert "日内" in context
    assert "结构" not in levels_text


def test_narrative_liquidity_uses_pa_only() -> None:
    report = _minimal_report()
    report["price_action"]["15m"]["sr_levels"] = [
        {"price": 4137.0, "direction": "resistance", "label": "量价连续阻力", "kind": "consecutive_sr"},
    ]
    sections = build_rule_narrative_sections(report)
    liq = sections["liquidity"]
    levels_text = " ".join(liq.get("levels", []))
    assert "量价" in levels_text
    assert "结构" not in levels_text


def test_narrative_facts_include_price_action_for_llm() -> None:
    report = _minimal_report()
    facts = build_narrative_facts(
        report,
        {"price_action": report["price_action"], "quality": {}},
        compact_for_llm=True,
    )
    assert "price_action" not in facts
    assert "price_action_summary" in facts
    assert "combination_rules" in facts
    assert facts["price_action_summary"]["5m"]["poc"] == 4125.0
    assert "_hint" in facts["price_action_summary"]
    assert any(x["kind"] == "volume_profile" for x in facts["allowed_levels"])


def test_entry_resonance_near_vah() -> None:
    text = entry_resonance_text(
        {"entry_low": 4136.0, "entry_high": 4139.0},
        {"volume_profile": {"poc": 4120.0, "vah": 4138.0, "val": 4110.0}, "sr_levels": []},
    )
    assert "VAH" in text or "共振" in text


def test_pa_llm_summary_compact() -> None:
    summary = build_pa_llm_summary(_minimal_report()["price_action"], price=4120.0)
    assert "nearest_resistance" in summary["5m"]
    assert summary["5m"]["poc"] == 4125.0
    assert "_hint" in summary
    assert len(summary["_hint"]) == 3
