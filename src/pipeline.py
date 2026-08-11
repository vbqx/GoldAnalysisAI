"""Main pipeline — generates one Advice V2 packet for human review."""

from __future__ import annotations

from src.core.orchestrator import run_advice_pipeline
from src.log import get_logger

log = get_logger(__name__)


def run_analysis() -> tuple[dict, dict, dict]:
    log.debug("run_analysis invoked")
    return run_advice_pipeline()
