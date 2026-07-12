"""Export/import run archive folders as portable zip bundles."""

from __future__ import annotations

import io
import json
import zipfile
from pathlib import Path
from typing import Any

from src.run.archive.compat import inspect_archive, upgrade_manifest_if_needed
from src.run.archive.index import upsert_index_entry
from src.run.archive.schema import SCHEMA_VERSION
from src.run.archive.store import _archive_row_from_path, archives_root, run_dir
from src.log import get_logger

log = get_logger(__name__)

BUNDLE_MANIFEST = "bundle_manifest.json"


def export_archive_zip(run_id: str) -> bytes:
    """Zip an entire run folder for sharing or backup."""
    directory = run_dir(run_id)
    if not directory.is_dir():
        raise FileNotFoundError(f"run archive not found: {run_id}")

    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(directory.rglob("*")):
            if path.is_file():
                arcname = f"{run_id}/{path.relative_to(directory).as_posix()}"
                zf.write(path, arcname=arcname)
        zf.writestr(
            BUNDLE_MANIFEST,
            json.dumps(
                {"schema_version": SCHEMA_VERSION, "run_id": run_id, "kind": "pipeline_run_bundle"},
                ensure_ascii=False,
                indent=2,
            ),
        )
    return buf.getvalue()


def import_archive_zip(data: bytes, *, run_id: str | None = None, overwrite: bool = False) -> str:
    """Extract a bundle zip into ``.cache/run_archives/`` and refresh the index."""
    root = archives_root()
    root.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(io.BytesIO(data)) as zf:
        bundle_meta: dict[str, Any] = {}
        if BUNDLE_MANIFEST in zf.namelist():
            bundle_meta = json.loads(zf.read(BUNDLE_MANIFEST).decode("utf-8"))

        top_levels = {name.split("/")[0] for name in zf.namelist() if name and not name.endswith("/")}
        if not top_levels:
            raise ValueError("empty archive bundle")
        inferred_id = run_id or str(bundle_meta.get("run_id") or "")
        if not inferred_id:
            if len(top_levels) == 1:
                inferred_id = next(iter(top_levels))
            else:
                raise ValueError("cannot infer run_id; pass run_id= explicitly")

        target = run_dir(inferred_id)
        if target.exists() and not overwrite:
            raise FileExistsError(f"run archive already exists: {inferred_id}")

        target.mkdir(parents=True, exist_ok=True)
        prefix = f"{inferred_id}/"
        for name in zf.namelist():
            if name in (BUNDLE_MANIFEST,):
                continue
            if not name.startswith(prefix):
                continue
            rel = name[len(prefix) :]
            if not rel or rel.endswith("/"):
                continue
            out_path = target / rel
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_bytes(zf.read(name))

    inspection = inspect_archive(inferred_id, target)
    manifest = upgrade_manifest_if_needed(inspection.manifest, inferred_id, target)
    row = _archive_row_from_path(inferred_id, target)
    if row:
        upsert_index_entry(root, row)
    log.info(
        "imported run archive id=%s replayable=%s compatibility=%s",
        inferred_id,
        inspection.replayable,
        inspection.level.value,
    )
    return inferred_id
