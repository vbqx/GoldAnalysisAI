"""Report invariant gate remediations (#30)."""

from __future__ import annotations

from src.analysis.report_invariant_gate import apply_report_invariant_gate
from src.analysis.report_invariants import validate_report_invariants


def _contradictory_report() -> dict:
    return {
        "metrics": {"current_price": 4140.0},
        "conclusion": {
            "header_conclusion": "今日决策：执行 · 做空",
            "action": "立即入场做空",
            "direction_summary": "偏空",
        },
        "signals": [
            {
                "signal_id": "s1",
                "name": "test",
                "direction": "short",
                "entry_low": 4150.0,
                "entry_high": 4160.0,
                "stop_loss": 4170.0,
                "take_profits": [4130.0],
                "signal_role": "primary",
                "status": "active",
                "trigger_confirmed": True,
            }
        ],
        "llm_analysis": {
            "enabled": True,
            "action_plan": "立即入场做空4140",
            "market_summary": "测试",
        },
        "meta": {
            "execution_authorized": True,
            "observation_mode": False,
            "manager_decision": {"action": "wait"},
            "final_decision": {"action": "wait"},
            "data_as_of": {"executable": True},
        },
    }


def test_rule_mode_empty_llm_does_not_degrade_or_revoke() -> None:
    """#34: disabled LLM empty payload must keep complete authorization."""
    report = {
        "metrics": {"current_price": 3996.12},
        "conclusion": {
            "header_conclusion": "今日决策：缩仓 · 做空",
            "action": "按授权计划缩仓执行，确认拒绝后入场",
            "direction_summary": "偏空",
        },
        "signals": [
            {
                "signal_id": "s1",
                "name": "rule short",
                "direction": "SELL",
                "entry_low": 4002.0,
                "entry_high": 4007.0,
                "stop_loss": 4013.0,
                "take_profits": [3988.0],
                "signal_role": "primary",
                "position_scale": 0.4,
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
        "meta": {
            "execution_authorized": True,
            "authorized_signal_ids": ["s1"],
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
            "data_as_of": {"executable": True},
            "run_config": {"agent_mode": "rule", "llm_enabled": False},
        },
    }
    inv = validate_report_invariants(report)
    assert inv["passed"] is True
    apply_report_invariant_gate(report, inv)
    assert report["meta"]["execution_authorized"] is True
    assert report["meta"]["observation_mode"] is False
    assert report["meta"].get("pipeline_status", "complete") == "complete"
    assert report["meta"]["invariant_gate"]["status"] == "passed"


def test_invariant_gate_revokes_execution_and_rewrites_conclusion() -> None:
    report = _contradictory_report()
    inv = validate_report_invariants(report)
    assert inv["passed"] is False
    assert any(v["code"] == "INV-MGR-001" for v in inv["violations"])

    apply_report_invariant_gate(report, inv)
    assert report["meta"]["execution_authorized"] is False
    assert report["meta"]["pipeline_status"] == "degraded"
    assert report["meta"]["invariant_gate"]["remediated"] is True
    assert report["llm_analysis"]["action_plan"] == ""
    assert "立即入场" not in str(report["conclusion"].get("action") or "")
    assert "今日决策：执行" not in str(report.get("conclusion", {}).get("header_conclusion") or "")
