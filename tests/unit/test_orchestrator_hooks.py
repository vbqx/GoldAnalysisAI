"""Orchestrator hook functions — begin, fetch, publish, finalize archive."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pandas as pd

from src.core.orchestrator_hooks import (
    begin_pipeline_run,
    fetch_market_data,
    finalize_pipeline_archive,
    publish_external_snapshot,
)
from src.core.run_config import RunConfig, run_config_for_mode
from src.core.types import ExternalFactors
from src.data.fetch_pipeline import DataFetchResult


def _sample_fetch() -> DataFetchResult:
    idx = pd.date_range("2026-06-01", periods=6, freq="5min", tz="UTC")
    close = pd.Series(2650.0, index=idx)
    df = pd.DataFrame(
        {"Open": close, "High": close + 1, "Low": close - 1, "Close": close, "Volume": 100},
        index=idx,
    )
    return DataFetchResult(raw={"5m": df}, external=ExternalFactors(), source_label="test")


def test_begin_pipeline_run_returns_id_and_timer() -> None:
    with patch("src.core.orchestrator_hooks.allocate_run_id", return_value="20260712T100000Z"):
        run_id, started = begin_pipeline_run()
    assert run_id == "20260712T100000Z"
    assert isinstance(started, float)
    assert started > 0


def test_fetch_market_data_returns_fetch_result() -> None:
    fetched = _sample_fetch()
    with patch("src.core.orchestrator_hooks.fetch_all_data", return_value=fetched):
        assert fetch_market_data() is fetched


def test_publish_external_snapshot_sets_prog_snapshot() -> None:
    fetched = _sample_fetch()
    prog = MagicMock()
    snapshot = {"sources": ["test"]}
    with patch(
        "src.viz.external_data_view.external_snapshot_from_fetch",
        return_value=snapshot,
    ):
        publish_external_snapshot(fetched, prog)
    prog.set_external_snapshot.assert_called_once_with(snapshot)


def test_finalize_pipeline_archive_calls_archive_run_with_normalized_config() -> None:
    fetched = _sample_fetch()
    report = {"metrics": {"current_price": 2650.0}, "meta": {}}
    enriched = {"5m": fetched.raw["5m"]}
    analyses: dict = {}
    cfg = RunConfig(agent_mode="llm", llm_enabled=True, llm_stage_trader=True)
    with patch("src.core.orchestrator_hooks.archive_run") as archive_run:
        finalize_pipeline_archive(
            "20260712T100000Z",
            fetched=fetched,
            report=report,
            enriched=enriched,
            analyses=analyses,
            elapsed_s=9.5,
            run_config=cfg,
        )
    archive_run.assert_called_once()
    kwargs = archive_run.call_args.kwargs
    assert archive_run.call_args.args[0] == "20260712T100000Z"
    assert kwargs["elapsed_s"] == 9.5
    assert kwargs["run_config"] == cfg.normalized()
    assert kwargs["report"] is report


def test_finalize_pipeline_archive_uses_thread_run_config_when_none() -> None:
    fetched = _sample_fetch()
    with patch("src.core.orchestrator_hooks.get_run_config", return_value=run_config_for_mode("rule")), patch(
        "src.core.orchestrator_hooks.archive_run"
    ) as archive_run:
        finalize_pipeline_archive(
            "run-x",
            fetched=fetched,
            report={"meta": {}},
            enriched={},
            analyses={},
            elapsed_s=1.0,
            run_config=None,
        )
    assert archive_run.call_args.kwargs["run_config"].agent_mode == "rule"
