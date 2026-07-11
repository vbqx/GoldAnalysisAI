"""GoldAnalysisAI — Streamlit 入口（纯导航，不显示为侧边栏页面）。

启动方式（官方，跨平台）：
    python run_app.py
    # Windows 也可: .\\run_app.bat
    # Linux/macOS 也可: ./run_app.sh

请勿直接运行 ``streamlit run app.py``。
详见 AGENTS.md、README.md。
"""

from __future__ import annotations

import os
from pathlib import Path

# Load .env before any src.config import (via downstream modules).
_env = Path(__file__).resolve().parent / ".env"
if _env.exists():
    for line in _env.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, val = line.split("=", 1)
        os.environ[key.strip()] = val.strip()

import streamlit as st

from src.log import setup_logging
from src.viz.dashboard_components import DASHBOARD_CSS
from src.viz.streamlit_common import bootstrap_env, render_sidebar_header

bootstrap_env()
setup_logging()

st.set_page_config(
    page_title="GoldAnalysisAI · XAUUSD",
    page_icon="🥇",
    layout="wide",
)
st.markdown(DASHBOARD_CSS, unsafe_allow_html=True)
render_sidebar_header()

pg = st.navigation(
    [
        st.Page(
            "views/1_机构级分析报告.py",
            title="机构级分析报告",
            icon="📊",
            default=True,
        ),
        st.Page("views/4_外部数据.py", title="外部数据", icon="🌐"),
        st.Page("views/2_短线策略.py", title="短线策略", icon="📈"),
        st.Page("views/3_LLM决策链.py", title="LLM决策链", icon="🤖"),
    ]
)
pg.run()
