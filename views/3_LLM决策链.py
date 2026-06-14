"""LLM 决策链 — 独立页面。"""

from __future__ import annotations

from src.viz.decision_page import render_llm_decision_page
from src.viz.streamlit_common import (
    ensure_report,
    page_setup,
    render_sidebar_footer,
)

page_setup()

report, data, analyses = ensure_report(show_generation_ui=False)
render_llm_decision_page(report)
render_sidebar_footer(data)
