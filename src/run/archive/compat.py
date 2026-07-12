"""Compatibility layer — inspect, migrate, and normalize archived pipeline runs."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from src.run.archive.schema import (
    ARTIFACT_ANALYSIS,
    ARTIFACT_FETCH,
    ARTIFACT_FRAME,
    MAX_READER_SCHEMA_VERSION,
    MIN_READER_SCHEMA_VERSION,
    NARRATIVE_SECTION_KEYS,
    REPORT_CONTRACT_VERSION,
    REPORT_TOP_LEVEL_DEFAULTS,
    SCHEMA_VERSION,
    ArchiveInspection,
    CompatibilityLevel,
    build_manifest,
    unwrap_artifact,
)
from src.run.archive.completion import (
    NON_REPLAY_STATUSES,
    generation_step_statuses,
    pipeline_replay_errors,
)
from src.log import get_logger

log = get_logger(__name__)

# Legacy v1: meta.json with top-level "version": 1, no manifest.json, bare fetch.json
LEGACY_SCHEMA_VERSION = 1


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def synthesize_manifest_from_legacy(run_id: str, directory: Path) -> dict[str, Any]:
    """Build a v2 manifest from pre-manifest archives (schema v1 folders)."""
    meta_path = directory / "meta.json"
    meta = _read_json(meta_path) if meta_path.is_file() else {}
    legacy_version = int(meta.get("version") or meta.get("schema_version") or LEGACY_SCHEMA_VERSION)
    summary = {
        "source_label": meta.get("source_label"),
        "current_price": meta.get("current_price"),
        "bars_summary": meta.get("bars_summary") or {},
        "elapsed_s": meta.get("elapsed_s"),
        "observation_mode": meta.get("observation_mode"),
    }
    return build_manifest(
        run_id=run_id,
        saved_at=str(meta.get("saved_at") or ""),
        run_config=meta.get("run_config") if isinstance(meta.get("run_config"), dict) else {},
        summary=summary,
        legacy={"detected_schema_version": legacy_version, "migrated_on_read": True},
    )


def load_manifest(run_id: str, directory: Path) -> dict[str, Any]:
    manifest_path = directory / "manifest.json"
    if manifest_path.is_file():
        manifest = _read_json(manifest_path)
        if not isinstance(manifest, dict):
            raise ValueError(f"invalid manifest.json for run {run_id}")
        manifest.setdefault("run_id", run_id)
        return manifest
    if (directory / "meta.json").is_file():
        log.info("run archive %s: synthesizing manifest from legacy layout", run_id)
        return synthesize_manifest_from_legacy(run_id, directory)
    raise FileNotFoundError(f"run archive manifest not found: {directory}")


def inspect_archive(run_id: str, directory: Path) -> ArchiveInspection:
    warnings: list[str] = []
    errors: list[str] = []

    try:
        manifest = load_manifest(run_id, directory)
    except FileNotFoundError as exc:
        return ArchiveInspection(
            run_id=run_id,
            level=CompatibilityLevel.INCOMPATIBLE,
            schema_version=0,
            errors=[str(exc)],
        )

    try:
        schema_version = int(manifest.get("schema_version") or LEGACY_SCHEMA_VERSION)
    except (TypeError, ValueError):
        schema_version = LEGACY_SCHEMA_VERSION
        warnings.append("manifest schema_version invalid; treated as legacy")

    if schema_version > MAX_READER_SCHEMA_VERSION:
        errors.append(
            f"archive schema v{schema_version} is newer than reader max v{MAX_READER_SCHEMA_VERSION}"
        )
    elif schema_version < MIN_READER_SCHEMA_VERSION:
        errors.append(
            f"archive schema v{schema_version} is below reader min v{MIN_READER_SCHEMA_VERSION}"
        )

    artifacts = manifest.get("artifacts") or {}
    summary_status = str((manifest.get("summary") or {}).get("pipeline_status") or "")
    forensic_only = summary_status in NON_REPLAY_STATUSES

    report_path = directory / str((artifacts.get("report") or {}).get("path") or "report.json")
    if not report_path.is_file():
        msg = f"missing required report artifact: {report_path.name}"
        if forensic_only:
            warnings.append(msg)
        elif not (directory / "failure.json").is_file():
            errors.append(msg)

    enriched_dir = directory / str((artifacts.get("enriched") or {}).get("dir") or "enriched")
    if not enriched_dir.is_dir() or not any(enriched_dir.glob("*.json")):
        msg = f"missing or empty enriched artifact dir: {enriched_dir.name}"
        if forensic_only:
            warnings.append(msg)
        else:
            errors.append(msg)

    analyses_path = directory / str((artifacts.get("analyses") or {}).get("path") or "analyses.json")
    if not analyses_path.is_file():
        warnings.append("analyses.json missing — replay will rebuild structure from enriched bars")

    fetch_path = directory / str((artifacts.get("fetch") or {}).get("path") or "fetch.json")
    if not fetch_path.is_file():
        warnings.append("fetch.json missing — external/K-line raw replay unavailable")

    replay = manifest.get("replay") or {}
    saved_contract = int(replay.get("report_contract_version") or REPORT_CONTRACT_VERSION)
    if saved_contract > REPORT_CONTRACT_VERSION:
        warnings.append(
            f"report contract v{saved_contract} is newer than reader v{REPORT_CONTRACT_VERSION}; "
            "unknown fields preserved, defaults applied for missing keys"
        )

    if (manifest.get("legacy") or {}).get("migrated_on_read"):
        warnings.append("legacy archive layout — manifest synthesized on read")

    if report_path.is_file():
        try:
            report = _read_json(report_path)
            if isinstance(report, dict):
                completion_errors = pipeline_replay_errors(report, manifest)
                if completion_errors:
                    warnings.extend(completion_errors)
                if not completion_errors and not generation_step_statuses(report):
                    summary_status = str((manifest.get("summary") or {}).get("pipeline_status") or "")
                    if not summary_status:
                        warnings.append(
                            "generation_steps missing; legacy archive assumed complete"
                        )
        except (OSError, json.JSONDecodeError, TypeError) as exc:
            errors.append(f"report.json unreadable: {exc}")
            report = None
    else:
        report = None

    replay_errors: list[str] = []
    if isinstance(report, dict):
        replay_errors = pipeline_replay_errors(report, manifest)
    replayable = not replay_errors

    if errors:
        level = CompatibilityLevel.INCOMPATIBLE
    elif warnings:
        level = CompatibilityLevel.DEGRADED
    else:
        level = CompatibilityLevel.COMPATIBLE

    return ArchiveInspection(
        run_id=run_id,
        level=level,
        schema_version=schema_version,
        warnings=warnings,
        errors=errors,
        manifest=manifest,
        replayable=replayable,
    )


def normalize_report(report: Any, *, contract_version: int = REPORT_CONTRACT_VERSION) -> tuple[dict[str, Any], list[str]]:
    """Fill missing top-level report keys so UI code survives schema drift."""
    warnings: list[str] = []
    if not isinstance(report, dict):
        warnings.append("report payload is not a dict; replaced with empty report")
        report = {}

    normalized: dict[str, Any] = dict(report)
    for key, default in REPORT_TOP_LEVEL_DEFAULTS.items():
        if key not in normalized or normalized[key] is None:
            normalized[key] = default() if callable(default) else default
            if key not in report:
                warnings.append(f"report missing '{key}'; filled with default")

    sections = normalized.get("narrative_sections")
    if not isinstance(sections, dict):
        sections = {}
        normalized["narrative_sections"] = sections
        warnings.append("narrative_sections invalid; reset to empty object")
    for key in NARRATIVE_SECTION_KEYS:
        if key not in sections or not isinstance(sections.get(key), dict):
            sections[key] = {
                "summary": "（归档回放）该板块在保存时无数据。",
                "context": [],
                "levels": [],
                "conditions": [],
                "invalidation": "—",
                "source": "archive",
            }
            warnings.append(f"narrative_sections.{key} missing; filled placeholder")

    meta = normalized.setdefault("meta", {})
    if not isinstance(meta, dict):
        meta = {}
        normalized["meta"] = meta
    meta.setdefault("archive_report_contract_version", contract_version)

    return normalized, warnings


def migrate_fetch_payload(raw: Any) -> dict[str, Any]:
    version, payload = unwrap_artifact(raw, kind="fetch", default_version=ARTIFACT_FETCH)
    if not isinstance(payload, dict):
        raise ValueError("fetch artifact payload must be a dict")
    if version > ARTIFACT_FETCH:
        log.warning("fetch artifact v%s newer than reader v%s — best-effort load", version, ARTIFACT_FETCH)
    # v1 bare layout used top-level version + raw/external without envelope
    if "raw" not in payload and "payload" not in payload:
        raise ValueError("fetch artifact missing raw bars")
    return payload


def migrate_analyses_payload(raw: Any) -> dict[str, Any]:
    version, payload = unwrap_artifact(raw, kind="analysis", default_version=ARTIFACT_ANALYSIS)
    if not isinstance(payload, dict):
        return {}
    if version > ARTIFACT_ANALYSIS:
        log.warning("analysis artifact v%s newer than reader v%s — best-effort load", version, ARTIFACT_ANALYSIS)
    return payload


def migrate_frame_payload(raw: Any) -> dict[str, Any]:
    version, payload = unwrap_artifact(raw, kind="frame", default_version=ARTIFACT_FRAME)
    if not isinstance(payload, dict):
        raise ValueError("frame artifact payload must be a dict")
    if version > ARTIFACT_FRAME:
        log.warning("frame artifact v%s newer than reader v%s — best-effort load", version, ARTIFACT_FRAME)
    return payload


def upgrade_manifest_if_needed(manifest: dict[str, Any], run_id: str, directory: Path) -> dict[str, Any]:
    """Persist synthesized/upgraded manifest so future reads skip legacy detection."""
    try:
        schema_version = int(manifest.get("schema_version") or 0)
    except (TypeError, ValueError):
        schema_version = 0
    if schema_version >= SCHEMA_VERSION and not manifest.get("legacy"):
        return manifest
    upgraded = dict(manifest)
    upgraded["schema_version"] = SCHEMA_VERSION
    legacy = dict(upgraded.get("legacy") or {})
    legacy["upgraded_from"] = schema_version or LEGACY_SCHEMA_VERSION
    legacy["upgraded_at"] = upgraded.get("saved_at")
    upgraded["legacy"] = legacy
    path = directory / "manifest.json"
    if not path.is_file():
        path.write_text(json.dumps(upgraded, ensure_ascii=False, indent=2), encoding="utf-8")
        log.info("run archive %s: wrote upgraded manifest.json", run_id)
    return upgraded
