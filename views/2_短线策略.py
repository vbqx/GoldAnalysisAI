"""短线策略图 — 独立页面。"""

from __future__ import annotations

from src.viz.report_views import render_strategy_map
from src.viz.streamlit_common import (
    ensure_report,
    page_setup,
    render_page_hero,
    render_sidebar_footer,
)

page_setup()

render_page_hero("短线策略图", "复用已生成报告，切换页面无需重新跑流水线")

report, data, analyses = ensure_report(show_generation_ui=False)
render_strategy_map(report, data, analyses)
render_sidebar_footer(data)
