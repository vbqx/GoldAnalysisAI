"""Single entry point for UI replay — always inspect + load_bundle."""

from __future__ import annotations

from typing import Any

import pandas as pd

from src.run import RunConfig, inspect_run_archive, load_bundle
from src.run.archive.schema import CompatibilityLevel


def load_replay_bundle(
    run_config: RunConfig,
) -> tuple[dict[str, Any], dict[str, pd.DataFrame], dict[str, Any]]:
    """Load a saved run for replay. Raises ValueError when not loadable."""
    cfg = run_config.normalized()
    if not cfg.replay_mode or not cfg.replay_run_id:
        raise ValueError("replay mode requires replay_run_id")

    run_id = cfg.replay_run_id
    inspection = inspect_run_archive(run_id)
    if not inspection.loadable:
        detail = "; ".join(inspection.errors) or "archive not loadable"
        raise ValueError(f"run archive {run_id}: {detail}")

    if inspection.level == CompatibilityLevel.INCOMPATIBLE:
        detail = "; ".join(inspection.errors) or "incompatible archive"
        raise ValueError(f"run archive {run_id}: {detail}")

    return load_bundle(run_id)
