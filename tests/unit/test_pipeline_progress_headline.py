"""Pipeline progress headline + step completion helpers."""

from __future__ import annotations

from src.core.progress import ProgressReporter
from src.viz.pipeline_progress import pipeline_progress_headline


def test_pipeline_progress_headline_running_step() -> None:
    steps = [
        {"id": "fetch", "label": "数据拉取", "status": "done"},
        {"id": "analyst_team", "label": "Analyst Team", "status": "running", "detail": "LLM 四位分析师…"},
    ]
    assert "Analyst Team" in pipeline_progress_headline(steps)
    assert "LLM" in pipeline_progress_headline(steps)


def test_pipeline_progress_headline_after_done_shows_follow_up() -> None:
    steps = [
        {"id": "fetch", "label": "数据拉取", "status": "done"},
        {"id": "ict", "label": "ICT 结构分析", "status": "done"},
    ]
    headline = pipeline_progress_headline(steps)
    assert "ICT 结构分析" in headline
    assert "继续运行" in headline


def test_start_finishes_all_running_steps() -> None:
    reporter = ProgressReporter()
    reporter.start("fetch", "数据拉取")
    reporter.start_sibling("context", "上下文")
    reporter.start("indicators", "计算技术指标")
    statuses = {s.id: s.status for s in reporter.state.steps}
    assert statuses["fetch"] == "done"
    assert statuses["context"] == "done"
    assert statuses["indicators"] == "running"
