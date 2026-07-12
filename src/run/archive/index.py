"""Global index for run archives — avoids scanning every folder on list."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from src.run.archive.schema import SCHEMA_VERSION
from src.log import get_logger

log = get_logger(__name__)

INDEX_VERSION = 1
INDEX_FILENAME = "index.json"


def index_path(root: Path) -> Path:
    return root / INDEX_FILENAME


def load_index(root: Path) -> dict[str, Any]:
    path = index_path(root)
    if not path.is_file():
        return {"version": INDEX_VERSION, "schema_version": SCHEMA_VERSION, "runs": []}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {"version": INDEX_VERSION, "schema_version": SCHEMA_VERSION, "runs": []}
    if not isinstance(payload, dict):
        return {"version": INDEX_VERSION, "schema_version": SCHEMA_VERSION, "runs": []}
    payload.setdefault("runs", [])
    return payload


def save_index(root: Path, index: dict[str, Any]) -> None:
    root.mkdir(parents=True, exist_ok=True)
    index["version"] = INDEX_VERSION
    index["schema_version"] = SCHEMA_VERSION
    index["updated_at"] = datetime.now(timezone.utc).isoformat()
    index_path(root).write_text(
        json.dumps(index, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def upsert_index_entry(root: Path, entry: dict[str, Any]) -> None:
    index = load_index(root)
    runs: list[dict[str, Any]] = list(index.get("runs") or [])
    run_id = str(entry.get("run_id") or "")
    runs = [row for row in runs if str(row.get("run_id") or "") != run_id]
    runs.append(entry)
    runs.sort(key=lambda row: str(row.get("saved_at") or ""), reverse=True)
    index["runs"] = runs
    save_index(root, index)


def remove_index_entries(root: Path, run_ids: set[str]) -> None:
    if not run_ids:
        return
    index = load_index(root)
    runs = [row for row in (index.get("runs") or []) if str(row.get("run_id") or "") not in run_ids]
    index["runs"] = runs
    save_index(root, index)


def list_index_entries(root: Path, *, limit: int = 100) -> list[dict[str, Any]]:
    index = load_index(root)
    runs = list(index.get("runs") or [])
    runs.sort(key=lambda row: str(row.get("saved_at") or ""), reverse=True)
    return runs[:limit]


def rebuild_index_from_disk(root: Path, rows: list[dict[str, Any]]) -> None:
    """Replace index contents from freshly scanned archive rows."""
    index = load_index(root)
    index["runs"] = sorted(rows, key=lambda row: str(row.get("saved_at") or ""), reverse=True)
    save_index(root, index)
