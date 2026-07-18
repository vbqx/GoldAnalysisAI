from __future__ import annotations

from pathlib import Path

import pytest
import yaml

pytestmark = pytest.mark.regression

ROOT = Path(__file__).resolve().parents[2]

KEY_DOCS = [
    "docs/documentation-center.md",
    "docs/aspice/software-domain.md",
    "docs/aspice/SWE.1-software-requirements.md",
    "docs/aspice/SWE.2-architecture/software-architecture.md",
    "docs/aspice/SWE.3-detailed-design/software-detailed-design.md",
    "docs/aspice/SWE.4-unit-testing.md",
    "docs/aspice/SWE.5-integration-testing.md",
    "docs/aspice/SWE.6-validation-testing.md",
    "docs/operations/operations-guide.md",
    "docs/management/project-management.md",
    "docs/aspice/governance/verification-strategy.md",
    "docs/aspice/SWE.3-detailed-design/reference/handbook.md",
    "docs/aspice/records/reviews/review-index.md",
    "docs/archive/archive-policy.md",
]

OLD_DOC_FRAGMENTS = [
    "docs/design/",
    "docs/getting-started/",
    "docs/domain/",
    "docs/examples/",
    "docs/integrations/",
    "docs/architecture/",
    "docs/reference/",
    "docs/testing/",
    "docs/reviews/",
    "docs/overview/",
    "docs/planning/",
]


def test_docs_information_architecture_entrypoints_exist() -> None:
    missing = [path for path in KEY_DOCS if not (ROOT / path).is_file()]
    assert not missing, "Missing docs entrypoints:\n" + "\n".join(missing)


def test_repository_root_is_the_only_readme() -> None:
    readmes = [
        path.relative_to(ROOT).as_posix()
        for path in ROOT.rglob("README.md")
        if not any(part in {".git", ".venv", ".cache", ".pytest_cache"} for part in path.relative_to(ROOT).parts)
        and path.relative_to(ROOT).parts[:2] != ("tests", "reports")
    ]
    assert readmes == ["README.md"]


def test_top_level_docs_do_not_link_to_old_doc_paths() -> None:
    checked = [
        ROOT / "README.md",
        ROOT / "docs" / "documentation-center.md",
        ROOT / "tests" / "testing-system.md",
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
        ROOT / "docs" / "architecture",
        ROOT / "docs" / "reference",
        ROOT / "docs" / "testing",
        ROOT / "docs" / "reviews",
        ROOT / "docs" / "overview",
        ROOT / "docs" / "planning",
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


def test_architecture_docs_keep_human_readable_visual_flows() -> None:
    required_mermaid_counts = {
        "software-architecture.md": 5,
        "system-overview.md": 2,
        "analyst-context.md": 1,
        "backtesting.md": 3,
        "chart-layers.md": 1,
        "llm-agents.md": 2,
        "report-trust.md": 1,
        "health-review.md": 1,
        "smc-pa-narrative.md": 1,
        "technical-analysis.md": 1,
    }
    architecture_dir = ROOT / "docs" / "aspice" / "SWE.2-architecture"
    problems: list[str] = []

    for filename, minimum in required_mermaid_counts.items():
        text = (architecture_dir / filename).read_text(encoding="utf-8")
        actual = text.count("```mermaid")
        if actual < minimum:
            problems.append(f"{filename}: expected >= {minimum} Mermaid diagrams, got {actual}")

    backtesting = (architecture_dir / "backtesting.md").read_text(encoding="utf-8")
    stale_english_headings = [
        "# Backtesting Design",
        "## Backtest Layers",
        "## Current MVP Scope",
        "## Target LLM Full Pipeline Replay",
        "## Limitations",
    ]
    problems.extend(
        f"backtesting.md: untranslated heading {heading}"
        for heading in stale_english_headings
        if heading in backtesting
    )

    assert not problems, "Architecture readability regressions:\n" + "\n".join(problems)
