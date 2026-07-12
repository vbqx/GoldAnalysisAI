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
