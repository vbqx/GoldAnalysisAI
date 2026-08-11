"""Tests for archive index, prune, replay loader, and narrative facts."""

from __future__ import annotations

import pandas as pd
import pytest

from src.analysis.ict_pa import analyze_timeframe
from src.core.run_config import RunConfig, run_config_for_mode
from src.core.types import ExternalFactors
from src.data.fetch_pipeline import DataFetchResult
from src.data.run_archive import allocate_run_id, archive_run, list_archives
from src.data.run_archive_index import list_index_entries
from src.data.run_archive_prune import prune_archives


from tests._archive_helpers import report_for_archive


def _minimal_archive(tmp_path, monkeypatch, *, run_id: str | None = None) -> str:
    monkeypatch.setattr("src.run.archive.store.archives_root", lambda: tmp_path)
    run_id = run_id or allocate_run_id()
    idx = pd.date_range("2026-06-01", periods=12, freq="5min", tz="UTC")
    close = pd.Series(2650.0, index=idx)
    df = pd.DataFrame(
        {"Open": close, "High": close + 1, "Low": close - 1, "Close": close, "Volume": 100},
        index=idx,
    )
    timeframes = {tf: df.copy() for tf in ("5m", "15m", "1h", "4h", "1d")}
    fetched = DataFetchResult(raw=timeframes, external=ExternalFactors(), source_label="test")
    archive_run(
        run_id,
        fetched=fetched,
        report=report_for_archive(),
        enriched=timeframes,
        analyses={tf: analyze_timeframe(frame, tf) for tf, frame in timeframes.items()},
        run_config=run_config_for_mode("rule"),
        elapsed_s=1.0,
    )
    return run_id


def test_archive_index_updated_on_save(tmp_path, monkeypatch) -> None:
    run_id = _minimal_archive(tmp_path, monkeypatch)
    rows = list_index_entries(tmp_path)
    assert any(row["run_id"] == run_id for row in rows)
    assert (tmp_path / "index.json").is_file()


def test_list_archives_uses_index(tmp_path, monkeypatch) -> None:
    run_id = _minimal_archive(tmp_path, monkeypatch)
    rows = list_archives(limit=10)
    assert rows[0]["run_id"] == run_id


def test_prune_archives_by_count(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr("src.run.archive.store.archives_root", lambda: tmp_path)
    ids = []
    for n in range(3):
        ids.append(_minimal_archive(tmp_path, monkeypatch, run_id=f"2026010{n}T120000Z"))
    rows = list_archives(limit=10)
    removed = prune_archives(tmp_path, rows, max_count=1, max_mb=0)
    assert len(removed) == 2
    remaining = [p.name for p in tmp_path.iterdir() if p.is_dir()]
    assert len(remaining) == 1


def test_load_replay_bundle_degraded_completed_archive(tmp_path, monkeypatch) -> None:
    import json

    from src.run import inspect_run_archive
    from src.run.archive.completion import PIPELINE_STATUS_DEGRADED
    from src.run.archive.schema import CompatibilityLevel
    from src.viz.replay_loader import load_replay_bundle

    run_id = _minimal_archive(tmp_path, monkeypatch)
    run_dir = tmp_path / run_id
    manifest = json.loads((run_dir / "manifest.json").read_text(encoding="utf-8"))
    manifest["summary"]["pipeline_status"] = PIPELINE_STATUS_DEGRADED
    (run_dir / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    report = json.loads((run_dir / "report.json").read_text(encoding="utf-8"))
    report["meta"]["pipeline_status"] = PIPELINE_STATUS_DEGRADED
    (run_dir / "report.json").write_text(json.dumps(report), encoding="utf-8")

    inspection = inspect_run_archive(run_id)
    assert inspection.loadable
    assert inspection.replayable is False
    assert inspection.level == CompatibilityLevel.DEGRADED

    cfg = RunConfig(replay_mode=True, replay_run_id=run_id).normalized()
    loaded, enriched, analyses = load_replay_bundle(cfg)
    assert loaded["meta"]["viewing_replay"] is True
    assert not loaded["meta"].get("viewing_replay_forensic")
    assert "5m" in enriched


def test_load_replay_bundle_gate(tmp_path, monkeypatch) -> None:
    from src.viz.replay_loader import load_replay_bundle

    run_id = _minimal_archive(tmp_path, monkeypatch)
    cfg = RunConfig(replay_mode=True, replay_run_id=run_id).normalized()
    report, enriched, analyses = load_replay_bundle(cfg)
    assert report["meta"]["viewing_replay"] is True
    assert "5m" in enriched
    assert "5m" in analyses


def test_legacy_replay_rebuilds_without_fetch_snapshot(tmp_path, monkeypatch) -> None:
    from src.viz.replay_loader import load_replay_bundle

    run_id = _minimal_archive(tmp_path, monkeypatch)
    run_dir = tmp_path / run_id
    (run_dir / "fetch.json").unlink()

    cfg = RunConfig(replay_mode=True, replay_run_id=run_id).normalized()
    report, enriched, analyses = load_replay_bundle(cfg)

    assert report["artifact_kind"] == "human_review_advice"
    assert report["meta"]["rebuilt_from_legacy_archive"] is True
    assert any("外部背景快照不可用" in item for item in report["meta"]["archive_replay_warnings"])
    assert "5m" in enriched
    assert "5m" in analyses


def test_prune_archives_by_size_mb(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr("src.run.archive.store.archives_root", lambda: tmp_path)
    ids = [f"2026010{n}T120000Z" for n in range(3)]
    for run_id in ids:
        _minimal_archive(tmp_path, monkeypatch, run_id=run_id)
    oldest = tmp_path / ids[0]
    (oldest / "padding.bin").write_bytes(b"x" * (2 * 1024 * 1024))
    rows = list_archives(limit=10)
    removed = prune_archives(tmp_path, rows, max_count=0, max_mb=0)
    assert removed == []
    removed = prune_archives(tmp_path, rows, max_count=10, max_mb=1)
    assert removed
    assert not (tmp_path / ids[0]).exists()


def test_rebuild_index_from_disk(tmp_path, monkeypatch) -> None:
    from src.data.run_archive_index import rebuild_index_from_disk

    run_id = _minimal_archive(tmp_path, monkeypatch)
    index_file = tmp_path / "index.json"
    assert index_file.is_file()
    index_file.unlink()
    rows = list_archives(limit=10)
    rebuild_index_from_disk(tmp_path, rows)
    assert index_file.is_file()
    rebuilt = list_index_entries(tmp_path)
    assert any(row["run_id"] == run_id for row in rebuilt)


def test_load_replay_bundle_requires_replay_run_id() -> None:
    from src.viz.replay_loader import load_replay_bundle

    with pytest.raises(ValueError, match="replay_run_id"):
        load_replay_bundle(RunConfig(replay_mode=True, replay_run_id="").normalized())


def test_load_replay_bundle_incompatible_archive(tmp_path, monkeypatch) -> None:
    from src.viz.replay_loader import load_replay_bundle

    monkeypatch.setattr("src.run.archive.store.archives_root", lambda: tmp_path)
    run_id = "broken-replay"
    folder = tmp_path / run_id
    folder.mkdir()
    cfg = RunConfig(replay_mode=True, replay_run_id=run_id).normalized()
    with pytest.raises(ValueError, match="manifest not found|not loadable|incompatible"):
        load_replay_bundle(cfg)
