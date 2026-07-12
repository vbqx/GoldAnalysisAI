"""Deterministic final-report consistency and invariant gate."""

from __future__ import annotations

import re
from typing import Any

from src.analysis.fact_registry import allowed_prices, build_fact_registry
from src.analysis.level_validator import _geometry_error, _tp_ladder_error
from src.analysis.narrative_facts import build_narrative_facts_for_llm
from src.analysis.narrative_sections import (
    validate_llm_top_level_fields,
    _executable_wording_on_wait,
)
from src.core.types import LevelProposal


def _violation(code: str, field: str, message: str) -> dict[str, str]:
    return {"code": code, "field": field, "message": message}


def _manager_wait(meta: dict[str, Any]) -> bool:
    decision = meta.get("manager_decision") or (meta.get("final_decision") or {})
    return str(decision.get("action") or "") == "wait" or not meta.get("execution_authorized")


def _observation_mode(meta: dict[str, Any]) -> bool:
    return bool(meta.get("observation_mode"))


def _normalize_direction(raw: str) -> str:
    d = str(raw or "").lower()
    if d in ("sell", "short", "bearish"):
        return "SELL"
    if d in ("buy", "long", "bullish"):
        return "BUY"
    return str(raw or "SELL").upper()


def _check_signal_geometry(report: dict[str, Any]) -> list[dict[str, str]]:
    out: list[dict[str, str]] = []
    price = float((report.get("metrics") or {}).get("current_price") or 0)
    for idx, sig in enumerate(report.get("signals") or []):
        label = str(sig.get("name") or f"signal[{idx}]")
        direction = _normalize_direction(str(sig.get("direction") or "SELL"))
        try:
            proposal = LevelProposal(
                direction=direction,  # type: ignore[arg-type]
                entry_low=float(sig["entry_low"]),
                entry_high=float(sig["entry_high"]),
                stop_loss=float(sig["stop_loss"]),
                take_profits=[float(x) for x in sig.get("take_profits") or []],
                setup_type=str(sig.get("setup_type") or "plan"),
                reason="invariant",
                confidence=0.5,
            )
        except (KeyError, TypeError, ValueError):
            out.append(_violation("INV-GEO-001", label, "signal missing numeric geometry"))
            continue
        err = _geometry_error(proposal) or _tp_ladder_error(proposal)
        if err:
            out.append(_violation("INV-GEO-002", label, err))
        if proposal.direction == "SELL" and proposal.entry_high < price:
            out.append(_violation("INV-GEO-003", label, "SELL zone below current price"))
        if proposal.direction == "BUY" and proposal.entry_low > price:
            out.append(_violation("INV-GEO-004", label, "BUY zone above current price"))
    return out


def _check_authorization_narrative(report: dict[str, Any]) -> list[dict[str, str]]:
    out: list[dict[str, str]] = []
    meta = report.get("meta") or {}
    llm = report.get("llm_analysis") or {}
    facts = build_narrative_facts_for_llm(report, compact_for_llm=True)
    field_reasons = validate_llm_top_level_fields(llm, facts=facts)
    for field, reason in field_reasons.items():
        if reason:
            out.append(_violation("INV-AUTH-001", field, reason))

    if _manager_wait(meta) or _observation_mode(meta):
        action_plan = str(llm.get("action_plan") or "").strip()
        if action_plan and _executable_wording_on_wait(action_plan):
            out.append(_violation("INV-AUTH-002", "action_plan", "executable wording while unauthorized"))
        conclusion_action = str((report.get("conclusion") or {}).get("action") or "")
        if _executable_wording_on_wait(conclusion_action):
            out.append(_violation("INV-AUTH-003", "conclusion.action", "executable wording in conclusion"))
    return out


def _check_manager_alignment(report: dict[str, Any]) -> list[dict[str, str]]:
    out: list[dict[str, str]] = []
    meta = report.get("meta") or {}
    final = meta.get("final_decision") or {}
    conclusion = report.get("conclusion") or {}
    action = str(final.get("action") or meta.get("manager_decision", {}).get("action") or "")
    if action == "wait" and meta.get("execution_authorized"):
        out.append(_violation("INV-MGR-001", "meta.execution_authorized", "wait but execution_authorized=true"))
    header = str(conclusion.get("header_conclusion") or "")
    if action == "wait" and "今日决策：执行" in header:
        out.append(_violation("INV-MGR-002", "conclusion.header_conclusion", "wait contradicts execute headline"))
    return out


def _check_fact_prices(report: dict[str, Any], registry: dict[str, Any]) -> list[dict[str, str]]:
    out: list[dict[str, str]] = []
    allowed = allowed_prices(registry)
    if not allowed:
        return out
    tol = 0.51
    llm = report.get("llm_analysis") or {}
    blob = " ".join(
        str(llm.get(key) or "")
        for key in ("market_summary", "trade_thesis", "action_plan")
    )
    for token in re.findall(r"\d{4}(?:\.\d+)?", blob):
        try:
            number = float(token)
        except ValueError:
            continue
        if number < 100:
            continue
        if not any(abs(number - p) <= tol for p in allowed):
            out.append(
                _violation(
                    "INV-PRICE-001",
                    "llm_narrative",
                    f"unregistered price {token}",
                )
            )
    return out


def _check_freshness_language(report: dict[str, Any]) -> list[dict[str, str]]:
    out: list[dict[str, str]] = []
    meta = report.get("meta") or {}
    as_of = meta.get("data_as_of") or {}
    if as_of.get("executable"):
        return out
    llm = report.get("llm_analysis") or {}
    blob = " ".join(str(llm.get(k) or "") for k in ("market_summary", "trade_thesis"))
    urgent = ("立即", "马上", "当前可执行", "now entry", "market order")
    if any(word in blob.lower() or word in blob for word in urgent):
        out.append(_violation("INV-FRESH-001", "llm_narrative", "urgent execution language on stale snapshot"))
    return out


def _check_audit_metadata(report: dict[str, Any]) -> list[dict[str, str]]:
    out: list[dict[str, str]] = []
    meta = report.get("meta") or {}
    stage_sources = meta.get("stage_sources") or {}
    if report.get("llm_analysis", {}).get("enabled") and "narrative_top_level" not in stage_sources:
        out.append(_violation("INV-META-001", "stage_sources", "missing narrative_top_level audit"))
    registry = meta.get("fact_registry") or {}
    if registry.get("conflict_fact_ids"):
        out.append(
            _violation(
                "INV-FACT-001",
                "fact_registry",
                f"conflicting facts: {registry['conflict_fact_ids'][:3]}",
            )
        )
    return out


def validate_report_invariants(
    report: dict[str, Any],
    *,
    registry: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Run deterministic invariant checks; returns machine-readable violations."""
    registry = registry or build_fact_registry(report)
    violations: list[dict[str, str]] = []
    violations.extend(_check_signal_geometry(report))
    violations.extend(_check_authorization_narrative(report))
    violations.extend(_check_manager_alignment(report))
    violations.extend(_check_fact_prices(report, registry))
    violations.extend(_check_freshness_language(report))
    violations.extend(_check_audit_metadata(report))
    return {
        "passed": not violations,
        "violation_count": len(violations),
        "violations": violations,
    }
