"""Tests for archived run config summary formatting."""

from __future__ import annotations

from src.viz.archive_config_summary import format_archived_run_config, pipeline_status_label


def test_format_archived_run_config() -> None:
    text = format_archived_run_config(
        {
            "agent_mode": "llm",
            "llm_enabled": False,
            "llm_stage_analysts": True,
            "llm_stage_debate": True,
            "llm_stage_manager": True,
        }
    )
    assert "llm" in text
    assert "关" in text
    assert "辩论" in text


def test_pipeline_status_label() -> None:
    assert pipeline_status_label("partial") == "中断（partial）"
    assert pipeline_status_label("failed") == "失败（failed）"
