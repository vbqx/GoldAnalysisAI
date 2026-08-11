"""Advice V2 — 人工审核建议主页面。"""

from __future__ import annotations

from src.viz.advice_view import render_advice_report
from src.viz.streamlit_common import (
    ensure_report,
    page_setup,
    render_page_hero,
    render_sidebar_footer,
)

page_setup()

report, data, analyses = ensure_report()
render_page_hero(
    "XAUUSD 人工审核交易建议",
    f"{report['meta']['updated_at']} · 一次只给一个首选建议 · 最终执行由你确认",
)
render_advice_report(report, data, analyses)
render_sidebar_footer(data)
