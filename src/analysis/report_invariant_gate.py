"""Apply deterministic remediations when report invariants fail (final gate)."""

from __future__ import annotations

from typing import Any

from src.analysis.narrative_sections import _executable_wording_on_wait
from src.run.archive.completion import PIPELINE_STATUS_DEGRADED

_AUTH_REVOCATION_CODES = frozenset(
    {
        "INV-AUTH-001",
        "INV-AUTH-002",
        "INV-AUTH-003",
        "INV-MGR-001",
        "INV-MGR-002",
        "INV-TRIG-001",
        "INV-CLAIM-001",
        "INV-FRESH-001",
    }
)


def _revoke_execution(report: dict[str, Any], remediations: list[str]) -> None:
    meta = report.setdefault("meta", {})
    meta["execution_authorized"] = False
    meta["execution_ready"] = False
    meta["plan_authorized"] = False
    meta["authorized_signal_ids"] = []
    meta["plan_signal_ids"] = []
    meta["authorized_position_scale"] = 0.0
    meta["primary_trigger_state"] = None
    meta["observation_mode"] = True
    for sig in report.get("signals") or []:
        sig["signal_role"] = "rejected"
        sig["position_size"] = "0% 观望"
        sig["position_scale"] = 0.0
    report["strategy_plans"] = []
    remediations.append("revoked_execution_authorization")


def _sanitize_llm_fields(report: dict[str, Any], violations: list[dict[str, str]], remediations: list[str]) -> None:
    llm = report.setdefault("llm_analysis", {})
    for row in violations:
        code = str(row.get("code") or "")
        field = str(row.get("field") or "")
        if not code.startswith("INV-AUTH") and code != "INV-FRESH-001":
            continue
        if field in llm and str(llm.get(field) or "").strip():
            llm[field] = ""
            remediations.append(f"cleared_llm.{field}")
    for key in ("action_plan", "market_summary", "trade_thesis"):
        text = str(llm.get(key) or "")
        if text and _executable_wording_on_wait(text):
            llm[key] = ""
            remediations.append(f"cleared_llm.{key}")


def _sanitize_conclusion(report: dict[str, Any], remediations: list[str]) -> None:
    conclusion = report.setdefault("conclusion", {})
    action = str(conclusion.get("action") or "")
    if action and _executable_wording_on_wait(action):
        conclusion["action"] = "暂不执行交易计划；以下为结构背景与候选假设，仅供参考。"
        remediations.append("rewrote_conclusion.action")
    header = str(conclusion.get("header_conclusion") or "")
    if "今日决策：执行" in header and not report.get("meta", {}).get("execution_authorized"):
        conclusion.pop("header_conclusion", None)
        remediations.append("cleared_conclusion.header_conclusion")


def apply_report_invariant_gate(
    report: dict[str, Any],
    invariants: dict[str, Any],
) -> dict[str, Any]:
    """Enforce invariant failures: revoke auth, sanitize fields, mark run degraded."""
    from src.analysis.report_engine import align_conclusion_with_manager_decision, build_final_decision_meta

    meta = report.setdefault("meta", {})
    violations = list(invariants.get("violations") or [])
    codes = {str(v.get("code") or "") for v in violations}

    if invariants.get("passed"):
        meta["invariant_gate"] = {"status": "passed", "remediated": False}
        meta.setdefault("pipeline_status", "complete")
        return {**invariants, "remediated": False}

    remediations: list[str] = []
    if codes & _AUTH_REVOCATION_CODES:
        _revoke_execution(report, remediations)
    _sanitize_llm_fields(report, violations, remediations)
    _sanitize_conclusion(report, remediations)
    align_conclusion_with_manager_decision(report)
    meta["final_decision"] = build_final_decision_meta(report)

    meta["pipeline_status"] = PIPELINE_STATUS_DEGRADED
    meta["invariant_gate"] = {
        "status": PIPELINE_STATUS_DEGRADED,
        "remediated": True,
        "remediations": remediations,
        "violation_codes": sorted(codes),
    }
    invariants["remediated"] = True
    invariants["gate_applied"] = True
    return invariants
