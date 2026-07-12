"""Shared helpers for run archive unit tests."""

from __future__ import annotations

from src.run.archive.completion import REPLAY_REQUIRED_STEP_IDS


def complete_generation_steps(**status_overrides: str) -> list[dict[str, str]]:
    statuses = {step_id: "done" for step_id in REPLAY_REQUIRED_STEP_IDS}
    statuses.update(status_overrides)
    return [{"id": step_id, "label": step_id, "status": status} for step_id, status in statuses.items()]


def report_for_archive(**meta_overrides) -> dict:
    meta = {"generation_steps": complete_generation_steps()}
    meta.update(meta_overrides)
    return {"metrics": {"current_price": 2650.0}, "meta": meta}
