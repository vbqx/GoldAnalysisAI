from __future__ import annotations

from pathlib import Path

import pytest
import yaml

pytestmark = pytest.mark.regression

ROOT = Path(__file__).resolve().parents[2]

KEY_DOCS = [
    "docs/overview/project.md",
    "docs/overview/status.md",
    "docs/overview/codex-autonomy.md",
    "docs/architecture/architecture.md",
    "docs/architecture/review.md",
    "docs/architecture/backtesting.md",
    "docs/operations/setup.md",
    "docs/testing/strategy.md",
    "docs/reference/handbook.md",
    "docs/reference/examples/report-schema.md",
    "docs/archive/README.md",
]

OLD_DOC_FRAGMENTS = [
    "docs/design/",
    "docs/getting-started/",
    "docs/domain/",
    "docs/examples/",
    "docs/integrations/",
]


def test_docs_information_architecture_entrypoints_exist() -> None:
    missing = [path for path in KEY_DOCS if not (ROOT / path).is_file()]
    assert not missing, "Missing docs entrypoints:\n" + "\n".join(missing)


def test_top_level_docs_do_not_link_to_old_doc_paths() -> None:
    checked = [
        ROOT / "README.md",
        ROOT / "docs" / "README.md",
        ROOT / "tests" / "README.md",
    ]
    offenders: list[str] = []
    for path in checked:
        text = path.read_text(encoding="utf-8")
        for fragment in OLD_DOC_FRAGMENTS:
            if fragment in text:
                offenders.append(f"{path.relative_to(ROOT)}: {fragment}")
    assert not offenders, "Old docs paths remain:\n" + "\n".join(offenders)


def test_removed_doc_directories_stay_removed() -> None:
    removed = [
        ROOT / "docs" / "design",
        ROOT / "docs" / "getting-started",
        ROOT / "docs" / "domain",
        ROOT / "docs" / "examples",
        ROOT / "docs" / "integrations",
    ]
    existing = [str(path.relative_to(ROOT)) for path in removed if path.exists()]
    assert not existing, "Old docs directories should not return:\n" + "\n".join(existing)


def test_test_output_boundaries_are_ignored() -> None:
    gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
    required = [
        ".codex-remote-attachments/",
        "tests/reports/*",
        "!tests/reports/.gitkeep",
        ".pytest_cache/",
    ]
    missing = [pattern for pattern in required if pattern not in gitignore]
    assert not missing, "Missing generated-output ignore rules:\n" + "\n".join(missing)


def test_cases_catalog_points_to_existing_test_files() -> None:
    catalog = yaml.safe_load((ROOT / "tests" / "cases" / "catalog.yaml").read_text(encoding="utf-8"))
    missing: list[str] = []
    for case in catalog.get("cases", []):
        test_path = case.get("test_path")
        if test_path and not (ROOT / test_path).exists():
            missing.append(f"{case.get('id')}: {test_path}")
    assert not missing, "Catalog test_path entries do not exist:\n" + "\n".join(missing)
