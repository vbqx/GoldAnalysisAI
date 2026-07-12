"""LRU pruning for run archive folders."""

from __future__ import annotations

import shutil
from pathlib import Path
from typing import Any

from src.config import RUN_ARCHIVE_MAX_COUNT, RUN_ARCHIVE_MAX_MB
from src.run.archive.index import remove_index_entries
from src.log import get_logger

log = get_logger(__name__)


def _dir_size_bytes(path: Path) -> int:
    total = 0
    for child in path.rglob("*"):
        if child.is_file():
            try:
                total += child.stat().st_size
            except OSError:
                continue
    return total


def prune_archives(
    root: Path,
    rows: list[dict[str, Any]],
    *,
    max_count: int | None = None,
    max_mb: int | None = None,
) -> list[str]:
    """Delete oldest archives when count or total size exceeds limits. Returns removed run_ids."""
    max_count = RUN_ARCHIVE_MAX_COUNT if max_count is None else max_count
    max_mb = RUN_ARCHIVE_MAX_MB if max_mb is None else max_mb
    if max_count <= 0 and max_mb <= 0:
        return []

    ordered = sorted(rows, key=lambda row: str(row.get("saved_at") or ""), reverse=True)
    to_remove: list[str] = []

    if max_count > 0 and len(ordered) > max_count:
        for row in ordered[max_count:]:
            run_id = str(row.get("run_id") or "")
            if run_id:
                to_remove.append(run_id)

    if max_mb > 0:
        max_bytes = max_mb * 1024 * 1024
        sizes: dict[str, int] = {}
        total = 0
        for row in ordered:
            run_id = str(row.get("run_id") or "")
            folder = root / run_id
            if not folder.is_dir():
                continue
            size = _dir_size_bytes(folder)
            sizes[run_id] = size
            total += size
        while total > max_bytes and ordered:
            victim = ordered.pop()
            run_id = str(victim.get("run_id") or "")
            if not run_id or run_id in to_remove:
                continue
            to_remove.append(run_id)
            total -= sizes.get(run_id, 0)

    removed: list[str] = []
    for run_id in dict.fromkeys(to_remove):
        folder = root / run_id
        if not folder.is_dir():
            continue
        try:
            shutil.rmtree(folder)
            removed.append(run_id)
            log.info("pruned run archive id=%s", run_id)
        except OSError as exc:
            log.warning("failed to prune run archive id=%s: %s", run_id, exc)

    if removed:
        remove_index_entries(root, set(removed))
    return removed
