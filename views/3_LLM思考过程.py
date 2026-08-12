"""LLM 思考过程 — 流水线步骤与 Prompt/响应审计（生成中自动流式显示）。"""

from __future__ import annotations

from src.viz.llm_process_view import render_llm_process_page
from src.viz.streamlit_common import (
    ensure_report,
    page_setup,
    render_sidebar_footer,
)

page_setup()

report, data, analyses = ensure_report(show_generation_ui=False)
render_llm_process_page(report)
render_sidebar_footer(data)
