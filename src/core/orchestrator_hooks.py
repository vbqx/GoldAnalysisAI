"""Small hooks extracted from orchestrator for readability and testing."""

from __future__ import annotations

import time
from typing import Any

from src.data.fetch_pipeline import DataFetchResult, fetch_all_data
from src.run import RunConfig, allocate_run_id, archive_run, get_run_config
from src.log import get_logger

log = get_logger(__name__)


def begin_pipeline_run() -> tuple[str, float]:
    run_id = allocate_run_id()
    log.info("pipeline start run_id=%s", run_id)
    return run_id, time.perf_counter()


def fetch_market_data() -> DataFetchResult:
    return fetch_all_data()


def publish_external_snapshot(fetched: DataFetchResult, prog: Any) -> None:
    from src.viz.external_data_view import external_snapshot_from_fetch

    prog.set_external_snapshot(external_snapshot_from_fetch(fetched))


def finalize_pipeline_archive(
    run_id: str,
    *,
    fetched: DataFetchResult,
    report: dict[str, Any],
    enriched: dict,
    analyses: dict,
    elapsed_s: float,
    run_config: RunConfig | None = None,
) -> None:
    cfg = (run_config or get_run_config()).normalized()
    archive_run(
        run_id,
        fetched=fetched,
        report=report,
        enriched=enriched,
        analyses=analyses,
        run_config=cfg,
        elapsed_s=elapsed_s,
    )
