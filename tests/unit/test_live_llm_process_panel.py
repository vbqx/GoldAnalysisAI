"""Live LLM process panel smoke tests."""

from __future__ import annotations

from src.viz.pipeline_progress import render_live_llm_process_panel


def test_render_live_llm_process_panel_callable() -> None:
    assert callable(render_live_llm_process_panel)
