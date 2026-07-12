"""Offline LLM narrative replay — no API tokens."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from src.analysis.narrative_sections import build_rule_narrative_sections
from src.llm.analyst import validate_llm_payload

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "tests/fixtures/llm_narrative_overlong.json"
SAMPLE = ROOT / "tests/fixtures/replay_min_report.json"


def test_replay_overlong_fixture_accepts_all_sections() -> None:
    report = json.loads(SAMPLE.read_text(encoding="utf-8"))
    report["narrative_sections"] = build_rule_narrative_sections(report)
    payload = json.loads(FIXTURE.read_text(encoding="utf-8"))
    result = validate_llm_payload(payload, report, mode="llm", threshold=0.65)
    assert all(
        (result.narrative_sections or {}).get(key, {}).get("source") == "llm"
        for key in ("market_overview", "liquidity", "4h", "1h", "15m")
    )
    for audit in (result.narrative_section_audit or {}).values():
        reason = str(audit.get("fallback_reason") or "")
        assert "visible lines" not in reason


def test_replay_script_runs_offline() -> None:
    proc = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts/replay_llm_narrative.py"),
            "--report",
            str(SAMPLE),
            "--llm",
            str(FIXTURE),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    assert proc.returncode == 0, proc.stderr or proc.stdout
    assert "SUMMARY llm_sections=5/5" in (proc.stdout or "")
