"""Audit summary meta block tests."""

from __future__ import annotations

from src.analysis.audit_summary import build_audit_summary
from src.core.types import ManagerDecision


def test_build_audit_summary_includes_authorization_fields() -> None:
    signal_id = "sig-deadbeeffeed"
    report = {
        "signals": [
            {"signal_id": signal_id, "signal_role": "primary", "theme": "short"},
            {"signal_id": "sig-other", "signal_role": "rejected", "theme": "long"},
        ],
        "meta": {
            "run_config_fingerprint": "abc123",
            "agent_mode": "rule",
            "execution_authorized": True,
            "authorized_signal_ids": [signal_id],
            "authorized_position_scale": 0.4,
            "observation_mode": False,
            "stage_sources": {},
        },
    }
    decision = ManagerDecision(
        action="reduce",
        primary_direction="short",
        selected_signal_indices=[0],
        confidence=0.55,
        summary="test",
        position_scale=0.4,
    )
    summary = build_audit_summary(report, decision=decision, stage_meta={"risk": {"source": "rule"}})
    assert summary["primary_signal_id"] == signal_id
    assert summary["manager_action"] == "reduce"
    assert summary["authorized_signal_ids"] == [signal_id]
    assert summary["signals_digest"]
