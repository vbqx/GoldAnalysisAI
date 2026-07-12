"""Tests for archive zip export/import and failure snapshots."""

from __future__ import annotations

import json

import pandas as pd
import pytest

from src.analysis.ict_pa import analyze_timeframe
from src.core.progress import ProgressReporter, reset_progress, set_progress
from src.core.run_config import run_config_for_mode
from src.core.types import ExternalFactors
from src.data.fetch_pipeline import DataFetchResult
from src.run.archive.completion import PIPELINE_STATUS_COMPLETE, PIPELINE_STATUS_PARTIAL
from src.run.archive.store import (
    allocate_run_id,
    archive_failure_run,
    archive_label,
    archive_run,
    inspect_run_archive,
    list_archives,
    load_forensic_bundle,
    run_dir,
)
from src.run.archive.transfer import export_archive_zip, import_archive_zip

from tests._archive_helpers import report_for_archive


def _sample_fetch() -> DataFetchResult:
    idx = pd.date_range("2026-06-01", periods=24, freq="5min", tz="UTC")
    close = pd.Series(2650.0, index=idx)
    df = pd.DataFrame(
        {
            "Open": close - 0.5,
            "High": close + 1.0,
            "Low": close - 1.0,
            "Close": close,
            "Volume": [100] * len(idx),
        },
        index=idx,
    )
    return DataFetchResult(
        raw={"5m": df, "15m": df},
        external=ExternalFactors(),
        source_label="test",
    )


def test_archive_failure_run_marked_not_replayable(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr("src.run.archive.store.archives_root", lambda: tmp_path)
    run_id = allocate_run_id()
    reporter = ProgressReporter()
    reporter.start("fetch", "数据拉取")
    reporter.fail("fetch", "TradingView fetch failed")
    token = set_progress(reporter)
    try:
        path = archive_failure_run(
            run_id,
            "TradingView fetch failed",
            run_config=run_config_for_mode("llm"),
            elapsed_s=3.2,
            fetched=_sample_fetch(),
            failure_step="fetch",
        )
    finally:
        reset_progress(token)

    assert path.is_dir()
    meta = json.loads((path / "meta.json").read_text(encoding="utf-8"))
    assert meta["pipeline_status"] in (PIPELINE_STATUS_PARTIAL, "failed")
    inspection = inspect_run_archive(run_id)
    assert inspection.replayable is False
    assert (path / "failure.json").is_file()
    label = archive_label({"run_id": run_id, **meta, "replayable": False})
    assert "⚠" in label or "失败" in label


def test_list_archives_includes_partial(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr("src.run.archive.store.archives_root", lambda: tmp_path)
    run_id = allocate_run_id()
    archive_failure_run(
        run_id,
        "boom",
        run_config=run_config_for_mode("rule"),
        elapsed_s=1.0,
    )
    rows = list_archives()
    assert any(row["run_id"] == run_id for row in rows)
    assert rows[0]["replayable"] is False


def test_export_import_roundtrip(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr("src.run.archive.store.archives_root", lambda: tmp_path)
    run_id = allocate_run_id()
    fetched = _sample_fetch()
    enriched = {"5m": fetched.raw["5m"]}
    analyses = {"5m": analyze_timeframe(enriched["5m"], "5m")}
    report = report_for_archive(agent_mode="llm")
    archive_run(
        run_id,
        fetched=fetched,
        report=report,
        enriched=enriched,
        analyses=analyses,
        run_config=run_config_for_mode("llm"),
        elapsed_s=1.0,
    )
    blob = export_archive_zip(run_id)

    import_root = tmp_path / "imported"
    import_root.mkdir()
    monkeypatch.setattr("src.run.archive.transfer.archives_root", lambda: import_root)
    monkeypatch.setattr("src.run.archive.store.archives_root", lambda: import_root)

    new_id = import_archive_zip(blob)
    assert new_id == run_id
    assert (import_root / run_id / "manifest.json").is_file()
    inspection = inspect_run_archive(run_id)
    assert inspection.replayable is True
    meta = json.loads((import_root / run_id / "meta.json").read_text(encoding="utf-8"))
    assert meta["pipeline_status"] == PIPELINE_STATUS_COMPLETE


def test_load_forensic_bundle_partial(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr("src.run.archive.store.archives_root", lambda: tmp_path)
    run_id = allocate_run_id()
    archive_failure_run(
        run_id,
        "debate timeout",
        run_config=run_config_for_mode("llm", llm_enabled=False),
        elapsed_s=2.0,
        fetched=_sample_fetch(),
    )
    report, enriched, analyses = load_forensic_bundle(run_id)
    assert report["meta"]["viewing_replay_forensic"] is True
    assert report["meta"]["failure_reason"] == "debate timeout"
    assert isinstance(enriched, dict)
