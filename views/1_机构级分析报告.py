"""机构级分析报告 — 主页面。"""

from __future__ import annotations

from src.viz.report_views import render_institutional_report
from src.viz.streamlit_common import (
    ensure_report,
    page_setup,
    render_page_hero,
    render_sidebar_footer,
)

page_setup()

report, data, analyses = ensure_report()
meta = report["meta"]
render_page_hero(
    meta["title"],
    f"{meta['updated_at']} · {meta.get('methodology', 'PA + ICT + SMC')}",
)
render_institutional_report(report, data, analyses, hide_title=True)
render_sidebar_footer(data)
