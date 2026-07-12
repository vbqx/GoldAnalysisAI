"""Pipeline completion checks — only fully finished runs are replayable."""

from __future__ import annotations

from typing import Any

PIPELINE_STATUS_COMPLETE = "complete"
PIPELINE_STATUS_PARTIAL = "partial"
PIPELINE_STATUS_FAILED = "failed"

NON_REPLAY_STATUSES = frozenset({PIPELINE_STATUS_PARTIAL, PIPELINE_STATUS_FAILED})

# Must match docs/reference/pipeline-steps.yaml progress steps.
REPLAY_REQUIRED_STEP_IDS = (
    "fetch",
    "indicators",
    "ict",
    "analyst_team",
    "bullish",
    "bearish",
    "debate",
    "trader",
    "risk",
    "manager",
    "report",
    "llm_narrative",
)

TERMINAL_STEP_STATUSES = frozenset({"done", "skipped", "error"})


def generation_step_statuses(report: dict[str, Any]) -> dict[str, str]:
    steps = (report.get("meta") or {}).get("generation_steps") or []
    out: dict[str, str] = {}
    if not isinstance(steps, list):
        return out
    for row in steps:
        if not isinstance(row, dict):
            continue
        step_id = str(row.get("id") or "").strip()
        if not step_id:
            continue
        out[step_id] = str(row.get("status") or "").strip().lower()
    return out


def pipeline_replay_errors(
    report: dict[str, Any],
    manifest: dict[str, Any] | None = None,
) -> list[str]:
    """Return human-readable errors when a saved run must not be replayed."""
    errors: list[str] = []
    summary = (manifest or {}).get("summary") or {}
    status = str(summary.get("pipeline_status") or "").strip().lower()
    if status in NON_REPLAY_STATUSES:
        errors.append(f"pipeline run did not finish (status={status})")
    elif status and status != PIPELINE_STATUS_COMPLETE:
        errors.append(f"unsupported pipeline_status: {status}")

    step_map = generation_step_statuses(report)
    if not step_map:
        return errors

    for step_id in REPLAY_REQUIRED_STEP_IDS:
        step_status = step_map.get(step_id)
        if not step_status:
            errors.append(f"generation_steps missing required step: {step_id}")
            continue
        if step_status not in TERMINAL_STEP_STATUSES:
            errors.append(f"generation_steps.{step_id} is {step_status!r} (not finished)")

    return errors


def assert_pipeline_replay_ready(report: dict[str, Any]) -> None:
    errors = pipeline_replay_errors(report, manifest={"summary": {"pipeline_status": PIPELINE_STATUS_COMPLETE}})
    if errors:
        raise ValueError("; ".join(errors))
