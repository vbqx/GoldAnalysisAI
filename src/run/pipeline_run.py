"""Active pipeline run id — for partial/failure archives from worker/orchestrator."""

from __future__ import annotations

from contextvars import ContextVar

_current_run_id: ContextVar[str | None] = ContextVar("pipeline_run_id", default=None)


def set_current_run_id(run_id: str | None) -> None:
    _current_run_id.set(run_id)


def get_current_run_id() -> str | None:
    return _current_run_id.get()
