"""回归测试：流水线文档与代码 prog.start() 步骤保持同步。"""

from __future__ import annotations

import re
from pathlib import Path

import pytest
import yaml

pytestmark = pytest.mark.regression

ROOT = Path(__file__).resolve().parents[2]
REFERENCE = ROOT / "docs" / "aspice" / "SWE.3-detailed-design" / "reference"
PIPELINE_YAML = REFERENCE / "pipeline-steps.yaml"
ORCHESTRATOR = ROOT / "src" / "core" / "orchestrator.py"
FETCH_PIPELINE = ROOT / "src" / "data" / "fetch_pipeline.py"

DOC_FILES = [
    ROOT / "docs" / "operations" / "onboarding.md",
    REFERENCE / "handbook.md",
    ROOT / "docs" / "operations" / "walkthrough.md",
    REFERENCE / "cheat-sheet.md",
]


def _prog_start_keys(*paths: Path) -> set[str]:
    pattern = re.compile(r"""prog\.start\(\s*["']([^"']+)["']""")
    keys: set[str] = set()
    for path in paths:
        text = path.read_text(encoding="utf-8")
        keys.update(pattern.findall(text))
    return keys


def _yaml_step_ids(*, progress_only: bool = False) -> list[str]:
    data = yaml.safe_load(PIPELINE_YAML.read_text(encoding="utf-8"))
    steps = data["steps"]
    if progress_only:
        return [step["id"] for step in steps if step.get("progress", True)]
    return [step["id"] for step in steps]


def test_pipeline_yaml_exists() -> None:
    assert PIPELINE_YAML.is_file()


def test_yaml_steps_match_prog_start_keys() -> None:
    code_keys = _prog_start_keys(ORCHESTRATOR, FETCH_PIPELINE)
    yaml_ids = set(_yaml_step_ids(progress_only=True))
    assert code_keys == yaml_ids, (
        f"prog.start keys {sorted(code_keys)} != pipeline-steps.yaml ids {sorted(yaml_ids)}"
    )


def test_docs_mention_all_pipeline_steps() -> None:
    yaml_ids = _yaml_step_ids()
    data = yaml.safe_load(PIPELINE_YAML.read_text(encoding="utf-8"))
    labels = {step["id"]: step["label"] for step in data["steps"]}

    missing: list[str] = []
    for doc in DOC_FILES:
        if not doc.is_file():
            missing.append(f"{doc.name} (file missing)")
            continue
        text = doc.read_text(encoding="utf-8")
        for step_id in yaml_ids:
            if step_id not in text and labels[step_id] not in text:
                missing.append(f"{doc.name}: {step_id} / {labels[step_id]}")

    assert not missing, "Pipeline steps missing from docs:\n" + "\n".join(missing)


def test_onboarding_links_pipeline_yaml() -> None:
    onboarding = (ROOT / "docs" / "operations" / "onboarding.md").read_text(encoding="utf-8")
    assert "pipeline-steps.yaml" in onboarding
