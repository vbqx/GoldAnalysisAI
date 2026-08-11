"""Shared Advice V2 coherence validation."""

from __future__ import annotations

from typing import Any

from src.analysis.ict_pa import TimeframeAnalysis
from src.indicators.verify import indicator_snapshot


def validate_pipeline_coherence(
    report: dict[str, Any],
    data: dict[str, Any],
    analyses: dict[str, TimeframeAnalysis],
) -> tuple[list[str], list[str], dict[str, Any]]:
    issues: list[str] = []
    notes: list[str] = []
    advice = report.get("advice", {})
    decision = advice.get("decision")
    setup = advice.get("primary_setup")

    if report.get("artifact_kind") != "human_review_advice" or report.get("artifact_version") != 2:
        issues.append("report is not an Advice V2 artifact")
    if decision not in {"WAIT", "WATCH_LONG", "WATCH_SHORT", "AVOID"}:
        issues.append(f"invalid advice decision: {decision}")
    if not advice.get("audit", {}).get("passed"):
        issues.append("advice deterministic audit did not pass")
    if decision in {"WAIT", "AVOID"} and setup is not None:
        issues.append("non-watch decision contains a primary setup")
    if decision in {"WATCH_LONG", "WATCH_SHORT"} and setup is None:
        issues.append("watch decision is missing a primary setup")

    if setup:
        zone = setup["attention_zone"]
        low, high = float(zone["low"]), float(zone["high"])
        invalidation = float(setup["invalidation_level"])
        targets = [float(value) for value in setup.get("targets", [])]
        if setup["direction"] == "BUY":
            if decision != "WATCH_LONG" or invalidation >= low or any(target <= high for target in targets):
                issues.append("BUY setup geometry or decision is inconsistent")
        elif setup["direction"] == "SELL":
            if decision != "WATCH_SHORT" or invalidation <= high or any(target >= low for target in targets):
                issues.append("SELL setup geometry or decision is inconsistent")
        else:
            issues.append("primary setup has invalid direction")
        evidence_ids = {row.get("evidence_id") for row in advice.get("evidence", [])}
        if not set(setup.get("evidence_ids", [])) <= evidence_ids:
            issues.append("primary setup references missing evidence")
        if not setup.get("confirmation_checklist"):
            issues.append("primary setup lacks a human confirmation checklist")

    for timeframe in ("5m", "15m"):
        snapshot = indicator_snapshot(data[timeframe], timeframe)
        missing = [name for name in ("RSI14", "MACD", "ADX14", "ATR14", "EMA20", "VWAP") if name not in snapshot]
        if missing:
            issues.append(f"{timeframe} indicator snapshot missing: {', '.join(missing)}")

    legacy_keys = sorted({"signals", "agent_trace", "validated_plans", "projections"} & report.keys())
    if legacy_keys:
        issues.append("legacy V1 keys remain: " + ", ".join(legacy_keys))

    summary = {
        "artifact_version": report.get("artifact_version"),
        "price": report.get("metrics", {}).get("current_price"),
        "decision": decision,
        "bias": advice.get("bias"),
        "confidence": advice.get("confidence"),
        "has_primary_setup": setup is not None,
        "structure": {timeframe: analyses[timeframe].trend for timeframe in ("1d", "4h", "1h", "15m", "5m")},
        "issues": issues,
        "notes": notes,
    }
    return issues, notes, summary
