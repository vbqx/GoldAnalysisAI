"""Single entry point for UI replay — inspect + load_bundle or forensic snapshot."""

from __future__ import annotations

from typing import Any

import pandas as pd

from src.run import RunConfig, inspect_run_archive, load_bundle
from src.run.archive.schema import CompatibilityLevel
from src.run.archive.store import load_forensic_bundle


def load_replay_bundle(
    run_config: RunConfig,
) -> tuple[dict[str, Any], dict[str, pd.DataFrame], dict[str, Any]]:
    """Load a saved run for replay or forensic review."""
    cfg = run_config.normalized()
    if not cfg.replay_mode or not cfg.replay_run_id:
        raise ValueError("replay mode requires replay_run_id")

    run_id = cfg.replay_run_id
    inspection = inspect_run_archive(run_id)
    if inspection.level == CompatibilityLevel.INCOMPATIBLE:
        detail = "; ".join(inspection.errors) or "incompatible archive"
        raise ValueError(f"run archive {run_id}: {detail}")

    if inspection.loadable:
        try:
            return load_bundle(run_id)
        except (FileNotFoundError, ValueError):
            if inspection.replayable:
                raise
    return load_forensic_bundle(run_id)

