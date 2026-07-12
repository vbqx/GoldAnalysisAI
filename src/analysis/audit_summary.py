"""Per-run audit summary for Codex / regression review."""

from __future__ import annotations

import hashlib
import json
from typing import Any


def _hash_payload(payload: dict[str, Any]) -> str:
    raw = json.dumps(payload, ensure_ascii=False, sort_keys=True, default=str)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]


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
        "authorized_signal_ids": meta.get("authorized_signal_ids") or [],
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
        "stage_sources_digest": _hash_payload(stage_meta or meta.get("stage_sources") or {}),
    }
