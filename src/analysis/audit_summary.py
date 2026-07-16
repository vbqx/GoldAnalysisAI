"""Per-run audit summary for Codex / regression review."""

from __future__ import annotations

import hashlib
import json
from typing import Any


def _hash_payload(payload: dict[str, Any]) -> str:
    raw = json.dumps(payload, ensure_ascii=False, sort_keys=True, default=str)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]


def _llm_usage_summary(llm_io: list[dict[str, Any]]) -> dict[str, Any]:
    """Compact per-run LLM telemetry for Runtime Ledger (Issue #37)."""
    rows = [r for r in llm_io if r.get("kind") != "rule"]
    total_in = sum(int(r.get("input_chars") or 0) for r in rows)
    total_out = sum(int(r.get("output_chars") or 0) for r in rows)
    total_attempts = sum(int(r.get("attempt") or 0) for r in rows)
    retry_reasons: list[dict[str, Any]] = []
    for r in rows:
        for a in r.get("attempts") or []:
            if a.get("reason"):
                retry_reasons.append(
                    {
                        "stage": r.get("stage"),
                        "attempt": a.get("attempt"),
                        "reason": a.get("reason"),
                    }
                )
    return {
        "stage_count": len(rows),
        "input_chars": total_in,
        "input_tokens_est": int(round(total_in / 1.8)) if total_in else 0,
        "output_chars": total_out,
        "output_tokens_est": int(round(total_out / 1.8)) if total_out else 0,
        "total_attempts": total_attempts,
        "budget_actions": {
            r.get("stage"): r.get("budget_action")
            for r in rows
            if r.get("budget_action") and r.get("budget_action") != "none"
        },
        "retry_reasons": retry_reasons[:40],
        "provider_usage_available": any(r.get("usage") for r in rows),
    }


def build_audit_summary(
    report: dict[str, Any],
    *,
    decision: Any | None = None,
    stage_meta: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Compact audit block stored in report meta."""
    meta = report.get("meta") or {}
    signals = report.get("signals") or []
    primary = next((s for s in signals if s.get("signal_role") == "primary"), None)
    llm_io = meta.get("llm_io") or []
    slow_stages = [
        {"stage": row.get("stage"), "latency_ms": row.get("latency_ms")}
        for row in llm_io
        if (row.get("latency_ms") or 0) >= 60_000
    ]
    narrative_audit = (meta.get("stage_sources") or {}).get("narrative_sections") or {}
    fallbacks = {
        key: val.get("fallback_reason")
        for key, val in narrative_audit.items()
        if isinstance(val, dict) and val.get("fallback_reason")
    }
    top_audit = (meta.get("stage_sources") or {}).get("narrative_top_level") or {}
    decision_dict = decision.to_dict() if decision is not None and hasattr(decision, "to_dict") else (decision or {})
    return {
        "run_config_fingerprint": meta.get("run_config_fingerprint"),
        "agent_mode": meta.get("agent_mode"),
        "data_as_of": meta.get("data_as_of"),
        "observation_mode": meta.get("observation_mode"),
        "execution_authorized": meta.get("execution_authorized"),
        "plan_authorized": meta.get("plan_authorized"),
        "execution_ready": meta.get("execution_ready"),
        "primary_trigger_state": meta.get("primary_trigger_state"),
        "authorized_signal_ids": meta.get("authorized_signal_ids") or [],
        "plan_signal_ids": meta.get("plan_signal_ids") or [],
        "authorized_position_scale": meta.get("authorized_position_scale"),
        "primary_signal_id": (primary or {}).get("signal_id"),
        "manager_action": decision_dict.get("action"),
        "manager_selected_indices": decision_dict.get("selected_signal_indices"),
        "signals_digest": _hash_payload(
            {
                "ids": [s.get("signal_id") for s in signals],
                "roles": [s.get("signal_role") for s in signals],
                "themes": [s.get("theme") for s in signals],
            }
        ),
        "narrative_fallbacks": fallbacks,
        "narrative_top_level_rejected": top_audit.get("fallback_reason"),
        "slow_llm_stages": slow_stages,
        "llm_routing": meta.get("llm_routing") or {},
        "llm_usage_summary": _llm_usage_summary(llm_io),
        "stage_sources_digest": _hash_payload(stage_meta or meta.get("stage_sources") or {}),
        "report_invariants_passed": (meta.get("report_invariants") or {}).get("passed"),
        "report_invariant_codes": [
            v.get("code") for v in (meta.get("report_invariants") or {}).get("violations", [])
        ],
        "overall_reliability": (meta.get("report_reliability") or {}).get("overall_reliability"),
        "fact_registry_count": (meta.get("fact_registry") or {}).get("fact_count"),
    }
