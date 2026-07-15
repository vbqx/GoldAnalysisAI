from __future__ import annotations

import json
from pathlib import Path

from src.analysis.fact_registry import build_fact_registry
from src.analysis.report_invariants import validate_report_invariants

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "golden_reports"


def _load(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def test_wait_observation_passes_invariants() -> None:
    report = _load("wait_observation.json")
    registry = build_fact_registry(report)
    report["meta"]["fact_registry"] = registry
    result = validate_report_invariants(report, registry=registry)
    assert result["passed"] is True
    assert result["violation_count"] == 0


def test_bad_geometry_flags_sell_below_price() -> None:
    report = _load("bad_geometry.json")
    result = validate_report_invariants(report)
    codes = {v["code"] for v in result["violations"]}
    assert "INV-GEO-003" in codes
    assert result["passed"] is False


def test_stale_data_flags_urgent_language() -> None:
    report = _load("stale_urgent_narrative.json")
    result = validate_report_invariants(report)
    codes = {v["code"] for v in result["violations"]}
    assert "INV-FRESH-001" in codes


def test_geometry_ignores_rejected_candidate_inventory() -> None:
    """Stale BUY still in signal list must not fail consistency if not authorized."""
    report = {
        "metrics": {"current_price": 3999.0},
        "signals": [
            {
                "name": "LLM路径A·做空",
                "direction": "SELL",
                "entry_low": 4060.0,
                "entry_high": 4065.0,
                "stop_loss": 4068.5,
                "take_profits": [4049.62, 4029.8],
                "signal_id": "sig-a",
                "signal_role": "primary",
                "status": "active",
                "trigger_confirmed": True,
            },
            {
                "name": "右侧扫低做多",
                "direction": "BUY",
                "entry_low": 4044.62,
                "entry_high": 4049.62,
                "stop_loss": 4040.0,
                "take_profits": [4060.0, 4070.0],
                "signal_id": "sig-stale-buy",
                "signal_role": "rejected",
            },
        ],
        "meta": {
            "execution_authorized": True,
            "authorized_signal_ids": ["sig-a"],
            "manager_decision": {"action": "execute"},
            "final_decision": {"action": "execute"},
            "stage_sources": {},
        },
        "llm_analysis": {},
        "conclusion": {},
    }
    result = validate_report_invariants(report)
    codes = {v["code"] for v in result["violations"]}
    assert "INV-GEO-004" not in codes
    assert not any(c.startswith("INV-GEO") for c in codes)


def test_rule_mode_disabled_llm_skips_empty_top_level_auth() -> None:
    """#34: rule + llm_enabled=false must not emit INV-AUTH-001 on empty fields."""
    report = {
        "metrics": {"current_price": 3996.12},
        "signals": [
            {
                "signal_id": "sig-rule-0",
                "name": "规则做空",
                "direction": "SELL",
                "entry_low": 4002.0,
                "entry_high": 4007.0,
                "stop_loss": 4013.0,
                "take_profits": [3988.0, 3974.0],
                "signal_role": "primary",
                "status": "active",
                "trigger_confirmed": True,
            }
        ],
        "llm_analysis": {
            "enabled": False,
            "market_summary": "",
            "trade_thesis": "",
            "action_plan": "",
        },
        "conclusion": {
            "action": "缩仓观察授权计划，确认拒绝后执行",
            "header_conclusion": "今日决策：缩仓 · 做空",
        },
        "meta": {
            "execution_authorized": True,
            "authorized_signal_ids": ["sig-rule-0"],
            "authorized_position_scale": 0.4,
            "observation_mode": False,
            "manager_decision": {
                "action": "reduce",
                "primary_direction": "short",
                "confidence": 0.72,
                "selected_signal_indices": [0],
                "position_scale": 0.4,
            },
            "final_decision": {"action": "reduce", "primary_direction": "short"},
            "run_config": {"agent_mode": "rule", "llm_enabled": False},
            "data_as_of": {"executable": True, "data_age_hours": 0.0},
            "stage_sources": {},
        },
    }
    result = validate_report_invariants(report)
    auth_codes = [v["code"] for v in result["violations"] if v["code"] == "INV-AUTH-001"]
    assert auth_codes == []
    assert result["passed"] is True


def test_execution_authorized_without_trigger_fails_invariant() -> None:
    report = {
        "metrics": {"current_price": 4072.0},
        "signals": [
            {
                "name": "cand short",
                "direction": "SELL",
                "entry_low": 4067.31,
                "entry_high": 4070.71,
                "stop_loss": 4073.50,
                "take_profits": [4060.0, 4050.0],
                "signal_id": "sig-cand",
                "signal_role": "primary",
                "status": "candidate",
                "trigger_confirmed": False,
            }
        ],
        "meta": {
            "execution_authorized": True,
            "authorized_signal_ids": ["sig-cand"],
            "manager_decision": {"action": "reduce"},
            "final_decision": {"action": "reduce", "execution_authorized": True},
            "stage_sources": {},
        },
        "llm_analysis": {},
        "conclusion": {},
    }
    result = validate_report_invariants(report)
    codes = {v["code"] for v in result["violations"]}
    assert "INV-TRIG-001" in codes
    assert result["passed"] is False


def test_enabled_llm_empty_top_level_still_flags_auth() -> None:
    """LLM 已启用但顶层文案全空时，仍须 INV-AUTH-001 降级。"""
    report = {
        "metrics": {"current_price": 3996.12},
        "signals": [],
        "llm_analysis": {
            "enabled": True,
            "market_summary": "",
            "trade_thesis": "",
            "action_plan": "",
        },
        "conclusion": {"action": "观望"},
        "meta": {
            "execution_authorized": False,
            "observation_mode": True,
            "manager_decision": {"action": "wait"},
            "final_decision": {"action": "wait"},
            "data_as_of": {"executable": True},
            "stage_sources": {"narrative_top_level": {"accepted": False}},
        },
    }
    result = validate_report_invariants(report)
    assert result["passed"] is False
    assert sum(1 for v in result["violations"] if v["code"] == "INV-AUTH-001") == 3


def test_price_tolerance_allows_rounded_narrative_levels() -> None:
    """Bare integers get ±5; decimal tokens remain on the original 0.51 gate."""
    report = {
        "metrics": {"current_price": 3999.0},
        "signals": [],
        "meta": {
            "execution_authorized": False,
            "authorized_signal_ids": [],
            "observation_mode": True,
            "manager_decision": {"action": "wait"},
            "final_decision": {"action": "wait"},
            "stage_sources": {"narrative_top_level": {"source": "llm"}},
            "data_as_of": {"executable": False},
        },
        "llm_analysis": {
            "enabled": True,
            "market_summary": "金价失守4000关口，远低于价值区下沿4049。",
            "trade_thesis": "结构偏空，等待反抽。",
            "action_plan": "",
        },
        "conclusion": {},
    }
    registry = {
        "facts": {
            "pa.session.val": {"fact_id": "pa.session.val", "value": 4049.62, "value_type": "numeric"},
            "pa.session.poc": {"fact_id": "pa.session.poc", "value": 4002.88, "value_type": "numeric"},
        }
    }
    result = validate_report_invariants(report, registry=registry)
    codes = {v["code"] for v in result["violations"]}
    assert "INV-PRICE-001" not in codes

    # Decimal token still strict: 4049.10 is more than 0.51 from 4049.62.
    report["llm_analysis"]["market_summary"] = "关注 4049.10 支撑。"
    result_strict = validate_report_invariants(report, registry=registry)
    codes_strict = {v["code"] for v in result_strict["violations"]}
    assert "INV-PRICE-001" in codes_strict
