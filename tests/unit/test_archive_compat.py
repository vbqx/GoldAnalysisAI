"""Archive compatibility — normalize, inspect, upgrade, artifact unwrap."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from src.run.archive.compat import (
    inspect_archive,
    migrate_fetch_payload,
    normalize_report,
    synthesize_manifest_from_legacy,
    upgrade_manifest_if_needed,
)
from src.run.archive.completion import pipeline_replay_errors
from src.run.archive.schema import (
    ARTIFACT_FETCH,
    CompatibilityLevel,
    REPORT_TOP_LEVEL_DEFAULTS,
    artifact_envelope,
    unwrap_artifact,
)


def test_normalize_report_fills_missing_defaults() -> None:
    normalized, warnings = normalize_report({"metrics": {"current_price": 2650.0}})
    for key in REPORT_TOP_LEVEL_DEFAULTS:
        assert key in normalized
    assert normalized["metrics"]["current_price"] == 2650.0
    assert any("missing" in w for w in warnings)
    sections = normalized["narrative_sections"]
    assert set(sections.keys()) == {"market_overview", "liquidity", "4h", "1h", "15m"}


def test_normalize_report_preserves_extra_keys() -> None:
    normalized, _ = normalize_report({"custom_field": 42, "meta": {"x": 1}})
    assert normalized["custom_field"] == 42
    assert normalized["meta"]["x"] == 1


def test_normalize_report_replaces_non_dict_payload() -> None:
    normalized, warnings = normalize_report("not-a-dict")  # type: ignore[arg-type]
    assert isinstance(normalized, dict)
    assert any("not a dict" in w for w in warnings)


def test_inspect_archive_incompatible_without_manifest(tmp_path: Path) -> None:
    folder = tmp_path / "broken-run"
    folder.mkdir()
    inspection = inspect_archive("broken-run", folder)
    assert inspection.level == CompatibilityLevel.INCOMPATIBLE
    assert not inspection.loadable
    assert inspection.errors


def test_inspect_archive_incompatible_missing_report(tmp_path: Path) -> None:
    folder = tmp_path / "no-report"
    folder.mkdir()
    (folder / "meta.json").write_text(
        json.dumps({"version": 1, "run_id": "no-report", "saved_at": "2026-01-01T00:00:00+00:00"}),
        encoding="utf-8",
    )
    enriched = folder / "enriched"
    enriched.mkdir()
    (enriched / "5m.json").write_text("{}", encoding="utf-8")
    inspection = inspect_archive("no-report", folder)
    assert inspection.level == CompatibilityLevel.INCOMPATIBLE
    assert any("report" in err for err in inspection.errors)


def test_upgrade_manifest_if_needed_writes_manifest(tmp_path: Path) -> None:
    folder = tmp_path / "legacy-run"
    folder.mkdir()
    manifest = synthesize_manifest_from_legacy("legacy-run", folder)
    manifest["schema_version"] = 1
    upgraded = upgrade_manifest_if_needed(manifest, "legacy-run", folder)
    assert upgraded["schema_version"] >= 2
    assert (folder / "manifest.json").is_file()


def test_unwrap_artifact_envelope() -> None:
    payload = {"raw": {"5m": []}, "external": {}}
    wrapped = artifact_envelope(kind="fetch", artifact_version=ARTIFACT_FETCH, payload=payload)
    version, inner = unwrap_artifact(wrapped, kind="fetch", default_version=ARTIFACT_FETCH)
    assert version == ARTIFACT_FETCH
    assert inner == payload


def test_migrate_fetch_payload_warns_on_newer_version(caplog) -> None:
    payload = {"raw": {"5m": []}, "external": {}}
    wrapped = artifact_envelope(kind="fetch", artifact_version=ARTIFACT_FETCH + 5, payload=payload)
    with caplog.at_level("WARNING"):
        result = migrate_fetch_payload(wrapped)
    assert result == payload


def test_inspect_archive_rejects_partial_pipeline_status(tmp_path: Path) -> None:
    folder = tmp_path / "partial-run"
    folder.mkdir()
    enriched = folder / "enriched"
    enriched.mkdir()
    (enriched / "5m.json").write_text("{}", encoding="utf-8")
    (folder / "report.json").write_text(
        json.dumps(
            {
                "metrics": {"current_price": 2650.0},
                "meta": {
                    "generation_steps": [
                        {"id": "fetch", "status": "done"},
                        {"id": "trader", "status": "running"},
                    ]
                },
            }
        ),
        encoding="utf-8",
    )
    (folder / "manifest.json").write_text(
        json.dumps(
            {
                "schema_version": 2,
                "run_id": "partial-run",
                "saved_at": "2026-01-01T00:00:00+00:00",
                "summary": {"pipeline_status": "partial"},
                "artifacts": {
                    "report": {"path": "report.json"},
                    "enriched": {"dir": "enriched"},
                },
            }
        ),
        encoding="utf-8",
    )
    inspection = inspect_archive("partial-run", folder)
    assert inspection.level == CompatibilityLevel.INCOMPATIBLE
    assert not inspection.loadable
    assert any("partial" in err for err in inspection.errors)


def test_pipeline_replay_errors_flags_running_step() -> None:
    report = {
        "meta": {
            "generation_steps": [
                {"id": "fetch", "status": "done"},
                {"id": "trader", "status": "running"},
            ]
        }
    }
    errors = pipeline_replay_errors(report, manifest={"summary": {"pipeline_status": "complete"}})
    assert any("trader" in err for err in errors)
