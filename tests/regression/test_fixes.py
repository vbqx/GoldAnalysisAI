"""Regression tests — Issue fixes & project conventions (RG-01 ~ RG-07)."""
from __future__ import annotations

import os
import subprocess
import sys

import pytest

from tests._bootstrap import ROOT, setup_path

setup_path()


@pytest.mark.regression
def test_pytest_runs_without_pythonpath() -> None:
    """RG-01: test suite discoverable without PYTHONPATH (#5)."""
    env = {k: v for k, v in os.environ.items() if k != "PYTHONPATH"}
    proc = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/unit", "--collect-only", "-q"],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=env,
    )
    assert proc.returncode == 0, (proc.stdout or "") + (proc.stderr or "")
    assert "test_llm_json" in (proc.stdout or "")


@pytest.mark.regression
def test_no_deprecated_use_container_width() -> None:
    """RG-02: no use_container_width in src/ (#6)."""
    src_text = "\n".join(p.read_text(encoding="utf-8") for p in (ROOT / "src").rglob("*.py"))
    assert "use_container_width=True" not in src_text
    assert "use_container_width=False" not in src_text


@pytest.mark.regression
def test_sidebar_shows_research_and_debate_models() -> None:
    """RG-03: sidebar dual model labels (#7)."""
    from src.config import llm_sidebar_models

    sidebar_src = (ROOT / "src" / "viz" / "streamlit_common.py").read_text(encoding="utf-8")
    assert "LLM 研究" in sidebar_src
    assert "LLM 辩论/文案" in sidebar_src
    assert llm_sidebar_models()


@pytest.mark.regression
def test_subpage_waiting_ui_has_hero_and_live_panel() -> None:
    """RG-04: subpage progress UI (#8)."""
    common_src = (ROOT / "src" / "viz" / "streamlit_common.py").read_text(encoding="utf-8")
    strategy_src = (ROOT / "views" / "2_短线策略.py").read_text(encoding="utf-8")
    assert "正在生成报告…" in common_src
    assert "render_live_llm_status_lightweight" in common_src
    assert strategy_src.index("ensure_report") < strategy_src.index("render_page_hero")


@pytest.mark.regression
def test_ensure_report_reruns_on_complete() -> None:
    """RG-05: fragment rerun on generation complete; no double-rerun blank (#3)."""
    common_src = (ROOT / "src" / "viz" / "streamlit_common.py").read_text(encoding="utf-8")
    assert "st.rerun()" in common_src
    assert "_store_report_bundle" in common_src
    assert "            placeholder.empty()" not in common_src


@pytest.mark.regression
def test_report_generation_requires_run_config_panel() -> None:
    """RG-08: first page load gates generation behind run config."""
    common_src = (ROOT / "src" / "viz" / "streamlit_common.py").read_text(encoding="utf-8")
    panel_src = (ROOT / "src" / "viz" / "run_config_panel.py").read_text(encoding="utf-8")
    worker_src = (ROOT / "src" / "viz" / "generation_worker.py").read_text(encoding="utf-8")
    run_config_src = (ROOT / "src" / "run" / "config.py").read_text(encoding="utf-8")
    assert "生成前配置" in panel_src
    assert "开始生成报告" in panel_src
    assert "RUN_CONFIG_READY_KEY" in common_src
    assert "start_generation(" in common_src
    assert "generation_state" in common_src
    assert "RUN_CONFIG_WIDGETS_SEEDED_KEY" in panel_src
    assert "_seed_run_config_widgets_if_needed" in panel_src
    assert "run_config_widget_state" in run_config_src
    assert "default_panel_run_config" in panel_src
    assert "默认选择规则引擎" in panel_src
    assert "apply_run_config" in run_config_src
    assert "load_replay_bundle" in worker_src


@pytest.mark.regression
def test_llm_json_retry_helpers_present() -> None:
    """RG-06: LLM JSON parse + unified attempt budget (#4 / #37)."""
    base_src = (ROOT / "src" / "agents" / "llm" / "base.py").read_text(encoding="utf-8")
    policy_src = (ROOT / "src" / "llm" / "stage_policy.py").read_text(encoding="utf-8")
    assert "_parse_llm_json" in base_src
    assert "get_stage_policy" in base_src
    assert "max_attempts" in base_src
    assert "LLM_MAX_RETRIES" in policy_src
    assert "apply_input_budget" in policy_src


@pytest.mark.regression
@pytest.mark.parametrize(
    "module",
    [
        "src.viz.streamlit_common",
        "src.viz.agent_trace_view",
        "src.viz.decision_page",
        "src.agents.llm.base",
    ],
)
def test_core_modules_import(module: str) -> None:
    """RG-07: core modules import cleanly."""
    __import__(module)
