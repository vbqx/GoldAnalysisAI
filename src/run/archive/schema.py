"""Run archive schema — versioned manifest and artifact envelopes.

Design goals
------------
* **Manifest-first**: every run folder has ``manifest.json`` describing artifacts.
* **Independent artifact versions**: fetch/report/frame/analysis can evolve separately.
* **Forward-compatible reads**: unknown JSON fields are preserved; missing fields get defaults.
* **Explicit migrations**: ``run_archive_compat.migrate_*`` upgrade legacy layouts on read.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any

ARCHIVE_KIND = "pipeline_run"

# Bump when folder layout or manifest shape changes (migrations required).
SCHEMA_VERSION = 2

# Per-artifact payload format versions (independent of SCHEMA_VERSION).
ARTIFACT_FETCH = 1
ARTIFACT_REPORT = 1
ARTIFACT_ANALYSIS = 1
ARTIFACT_FRAME = 1

# Report JSON contract — bump when required top-level keys change.
REPORT_CONTRACT_VERSION = 1

MIN_READER_SCHEMA_VERSION = 1
MAX_READER_SCHEMA_VERSION = SCHEMA_VERSION

APP_NAME = "goldAianalysis"

REQUIRED_REPLAY_ARTIFACTS = ("report", "enriched")
OPTIONAL_REPLAY_ARTIFACTS = ("fetch", "analyses")

REPORT_TOP_LEVEL_DEFAULTS: dict[str, Any] = {
    "meta": {},
    "metrics": {},
    "sentiment": {},
    "conclusion": {},
    "narrative_sections": {},
    "timeframes": {},
    "signals": [],
    "projections": [],
    "fibonacci": [],
    "external": {},
    "market_overview": [],
    "liquidity": [],
    "invalidation": [],
    "risk_control": [],
    "path_summary": [],
    "price_action": {},
    "agent_trace": {},
    "llm_analysis": {},
    "calendar_events": [],
    "llm_levels": [],
    "validated_plans": [],
}

NARRATIVE_SECTION_KEYS = ("market_overview", "liquidity", "4h", "1h", "15m")


class CompatibilityLevel(str, Enum):
    COMPATIBLE = "compatible"
    DEGRADED = "degraded"
    INCOMPATIBLE = "incompatible"


@dataclass
class ArchiveInspection:
    run_id: str
    level: CompatibilityLevel
    schema_version: int
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    manifest: dict[str, Any] = field(default_factory=dict)

    @property
    def loadable(self) -> bool:
        return self.level != CompatibilityLevel.INCOMPATIBLE


def app_build_version() -> str:
    """Best-effort build id for manifest (git short sha or 'dev')."""
    import subprocess

    try:
        root = __file__.replace("\\", "/").rsplit("/src/", 1)[0]
        sha = subprocess.check_output(
            ["git", "-C", root, "rev-parse", "--short", "HEAD"],
            stderr=subprocess.DEVNULL,
            text=True,
        ).strip()
        if sha:
            return sha
    except (OSError, subprocess.SubprocessError):
        pass
    return "dev"


def artifact_envelope(*, kind: str, artifact_version: int, payload: Any) -> dict[str, Any]:
    return {
        "artifact_kind": kind,
        "artifact_version": artifact_version,
        "payload": payload,
    }


def unwrap_artifact(raw: Any, *, kind: str, default_version: int) -> tuple[int, Any]:
    """Return (artifact_version, payload) for enveloped or legacy bare payloads."""
    if not isinstance(raw, dict):
        return default_version, raw
    if raw.get("artifact_kind") == kind and "payload" in raw:
        try:
            version = int(raw.get("artifact_version") or default_version)
        except (TypeError, ValueError):
            version = default_version
        return version, raw["payload"]
    if "artifact_version" in raw and "payload" in raw:
        try:
            version = int(raw.get("artifact_version") or default_version)
        except (TypeError, ValueError):
            version = default_version
        return version, raw["payload"]
    return default_version, raw


def build_manifest(
    *,
    run_id: str,
    saved_at: str | None = None,
    run_config: dict[str, Any] | None = None,
    summary: dict[str, Any] | None = None,
    legacy: dict[str, Any] | None = None,
) -> dict[str, Any]:
    saved_at = saved_at or datetime.now(timezone.utc).isoformat()
    return {
        "schema_version": SCHEMA_VERSION,
        "archive_kind": ARCHIVE_KIND,
        "run_id": run_id,
        "saved_at": saved_at,
        "producer": {
            "app": APP_NAME,
            "build": app_build_version(),
            "schema_version": SCHEMA_VERSION,
        },
        "replay": {
            "min_reader_schema_version": MIN_READER_SCHEMA_VERSION,
            "report_contract_version": REPORT_CONTRACT_VERSION,
        },
        "artifacts": {
            "report": {
                "artifact_version": ARTIFACT_REPORT,
                "path": "report.json",
                "required": True,
            },
            "fetch": {
                "artifact_version": ARTIFACT_FETCH,
                "path": "fetch.json",
                "required": False,
            },
            "analyses": {
                "artifact_version": ARTIFACT_ANALYSIS,
                "path": "analyses.json",
                "required": False,
            },
            "enriched": {
                "artifact_version": ARTIFACT_FRAME,
                "dir": "enriched",
                "pattern": "{tf}.json",
                "required": True,
            },
        },
        "summary": summary or {},
        "run_config": run_config or {},
        "legacy": legacy,
    }
