"""LLM process page smoke tests."""

from __future__ import annotations

from src.viz.llm_process_view import render_llm_process_page


def test_render_llm_process_page_accepts_minimal_report() -> None:
    assert callable(render_llm_process_page)
