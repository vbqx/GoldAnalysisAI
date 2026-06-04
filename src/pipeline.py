"""Main analysis pipeline — delegates to TradeAgent-style orchestrator."""

from __future__ import annotations

from src.core.orchestrator import run_trade_agent_pipeline
from src.log import get_logger

log = get_logger(__name__)


def run_analysis() -> tuple[dict, dict, dict]:
    log.debug("run_analysis invoked")
    return run_trade_agent_pipeline()
