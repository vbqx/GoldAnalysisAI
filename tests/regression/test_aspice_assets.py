"""Regression checks for ASPICE document, traceability, and baseline assets."""

from __future__ import annotations

import csv
import subprocess
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[2]


@pytest.mark.regression
def test_aspice_assets_are_complete_and_current() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/check_aspice_assets.py", "--check"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=60,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr


@pytest.mark.regression
def test_every_function_and_document_has_an_aspice_mapping() -> None:
    with (ROOT / "docs/aspice/software-function-map.csv").open(encoding="utf-8-sig", newline="") as handle:
        functions = list(csv.DictReader(handle))
    with (ROOT / "docs/aspice/document-register.csv").open(encoding="utf-8-sig", newline="") as handle:
        documents = list(csv.DictReader(handle))

    assert functions
    assert documents
    assert all(row["software_unit_id"] and row["architecture_id"] and row["requirement_ids"] for row in functions)
    assert all(row["primary_process"] and row["information_item"] and row["lifecycle_status"] for row in documents)
    assert {row["path"] for row in documents} >= {
        "README.md",
        "AGENTS.md",
        "docs/README.md",
        "docs/aspice/software-requirements.yaml",
        "docs/aspice/software-architecture.yaml",
    }
