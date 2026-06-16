"""外部数据 — 新闻、日历、DXY、社媒；fetch 完成后即可查看。"""

from __future__ import annotations

import streamlit as st

from src.viz.external_data_view import render_external_data_page
from src.viz.streamlit_common import (
    REPORT_SESSION_KEY,
    ensure_external_data,
    page_setup,
    render_sidebar_footer,
)

page_setup()

payload = ensure_external_data()
render_external_data_page(payload)

data = None
if REPORT_SESSION_KEY in st.session_state:
    _, data, _ = st.session_state[REPORT_SESSION_KEY]
render_sidebar_footer(data)
