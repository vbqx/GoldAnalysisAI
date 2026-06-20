"""Rule-mode pipeline coherence check — structure vs debate vs signals vs indicators."""

from __future__ import annotations

import json
import sys

from tests._bootstrap import ROOT, configure_stdio, load_dotenv, setup_path

setup_path()
load_dotenv()
configure_stdio()

from src.core.progress import ProgressReporter, reset_progress, set_progress
from src.core.run_config import apply_run_config, run_config_for_mode
from src.pipeline import run_analysis
from tests.tools.coherence_validate import validate_pipeline_coherence


def main() -> int:
    apply_run_config(run_config_for_mode("rule"))
    reporter = ProgressReporter()
    token = set_progress(reporter)
    try:
        report, data, analyses = run_analysis()
    finally:
        reset_progress(token)

    issues, notes, summary = validate_pipeline_coherence(report, data, analyses)

    out = ROOT / "tests" / "reports" / "coherence_check.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")

    print("=== Coherence Check (rule mode) ===")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    print(f"Saved: {out}")
    return 1 if issues else 0


if __name__ == "__main__":
    sys.exit(main())
