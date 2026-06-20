"""Integration test fixtures — shared pipeline runs to reduce wall time."""

from __future__ import annotations

from collections.abc import Iterator

import pytest

from src.core.progress import ProgressReporter, reset_progress, set_progress
from src.core.run_config import apply_run_config, run_config_for_mode, run_config_from_env
from src.pipeline import run_analysis


@pytest.fixture(scope="module")
def env_pipeline_result() -> Iterator[tuple]:
    """One full pipeline run using .env / default runtime config."""
    baseline = run_config_from_env()
    apply_run_config(baseline)
    reporter = ProgressReporter()
    token = set_progress(reporter)
    try:
        yield run_analysis()
    finally:
        reset_progress(token)
        apply_run_config(baseline)


@pytest.fixture(scope="module")
def rule_pipeline_result() -> Iterator[tuple]:
    """Rule-mode pipeline for FIN-INT-03 coherence checks."""
    baseline = run_config_from_env()
    apply_run_config(run_config_for_mode("rule"))
    reporter = ProgressReporter()
    token = set_progress(reporter)
    try:
        yield run_analysis()
    finally:
        reset_progress(token)
        apply_run_config(baseline)
