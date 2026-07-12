#!/usr/bin/env python3
"""Inspect, list, and validate run archives without opening Streamlit."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def _cmd_list(args: argparse.Namespace) -> int:
    from src.run import archive_label, list_archives

    rows = list_archives(limit=args.limit)
    if not rows:
        print("No loadable run archives found.")
        return 0
    for row in rows:
        print(f"{row['run_id']}\t{archive_label(row)}")
    return 0


def _cmd_inspect(args: argparse.Namespace) -> int:
    from src.run import inspect_run_archive

    inspection = inspect_run_archive(args.run_id)
    payload = {
        "run_id": args.run_id,
        "loadable": inspection.loadable,
        "schema_version": inspection.schema_version,
        "compatibility": inspection.level.value,
        "warnings": inspection.warnings,
        "errors": inspection.errors,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if inspection.loadable else 1


def _cmd_validate(args: argparse.Namespace) -> int:
    from src.run import RunConfig
    from src.viz.replay_loader import load_replay_bundle

    cfg = RunConfig(replay_mode=True, replay_run_id=args.run_id).normalized()
    report, enriched, analyses = load_replay_bundle(cfg)
    print(
        json.dumps(
            {
                "run_id": args.run_id,
                "price": report.get("metrics", {}).get("current_price"),
                "timeframes": sorted(enriched.keys()),
                "analyses": sorted(analyses.keys()),
                "llm_enabled": bool((report.get("llm_analysis") or {}).get("enabled")),
                "forensic": bool((report.get("meta") or {}).get("viewing_replay_forensic")),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


def _cmd_export(args: argparse.Namespace) -> int:
    from src.run.archive.transfer import export_archive_zip

    payload = export_archive_zip(args.run_id)
    out = Path(args.output)
    out.write_bytes(payload)
    print(f"exported {args.run_id} -> {out} ({len(payload)} bytes)")
    return 0


def _cmd_import(args: argparse.Namespace) -> int:
    from src.run.archive.transfer import import_archive_zip

    data = Path(args.zip_path).read_bytes()
    run_id = import_archive_zip(data, run_id=args.run_id or None, overwrite=args.overwrite)
    print(f"imported {run_id}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Run archive CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    list_p = sub.add_parser("list", help="List saved runs")
    list_p.add_argument("--limit", type=int, default=50)
    list_p.set_defaults(func=_cmd_list)

    inspect_p = sub.add_parser("inspect", help="Inspect compatibility for one run")
    inspect_p.add_argument("run_id")
    inspect_p.set_defaults(func=_cmd_inspect)

    validate_p = sub.add_parser("validate", help="Load bundle via replay gate")
    validate_p.add_argument("run_id")
    validate_p.set_defaults(func=_cmd_validate)

    export_p = sub.add_parser("export", help="Export run folder as zip")
    export_p.add_argument("run_id")
    export_p.add_argument("-o", "--output", required=True)
    export_p.set_defaults(func=_cmd_export)

    import_p = sub.add_parser("import", help="Import zip bundle into local archives")
    import_p.add_argument("zip_path")
    import_p.add_argument("--run-id", default="")
    import_p.add_argument("--overwrite", action="store_true")
    import_p.set_defaults(func=_cmd_import)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
