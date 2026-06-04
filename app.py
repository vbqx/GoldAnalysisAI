"""Streamlit dashboard — dual report modes (institutional + strategy map)."""

from __future__ import annotations

import os

def _inject_proxy() -> None:
    for key in ("HTTPS_PROXY", "https_proxy", "HTTP_PROXY", "http_proxy"):
        if val := os.environ.get(key):
            os.environ.setdefault("http_proxy", val)
            os.environ.setdefault("https_proxy", val)
            return
    try:
        import winreg
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Internet Settings",
        )
        enable, _ = winreg.QueryValueEx(key, "ProxyEnable")
        if enable:
            server, _ = winreg.QueryValueEx(key, "ProxyServer")
            server = server.split(";")[0].strip()
            proxy = f"http://{server}" if "://" not in server else server
            os.environ.setdefault("http_proxy", proxy)
            os.environ.setdefault("https_proxy", proxy)
        winreg.CloseKey(key)
    except Exception:
        pass

_inject_proxy()

from src.log import setup_logging

setup_logging()

import streamlit as st

from src.indicators.verify import indicator_snapshot, indicator_table_rows
from src.log import get_logger
from src.pipeline import run_analysis
from src.viz.agent_trace_view import render_agent_trace_sidebar
from src.viz.dashboard_components import DASHBOARD_CSS
from src.viz.report_views import render_institutional_report, render_strategy_map

log = get_logger(__name__)

st.set_page_config(page_title="GoldAnalysisAI · XAUUSD", page_icon="🥇", layout="wide")

st.sidebar.markdown("**GoldAnalysisAI**")
st.sidebar.caption("数据源: TradingView · OANDA:XAUUSD")

st.markdown(DASHBOARD_CSS, unsafe_allow_html=True)


@st.cache_data(ttl=300, show_spinner=False)
def load_report(_cache_version: int = 8):
    from src.data.fetcher import clear_cache
    log.info("load_report: cache miss, running pipeline")
    clear_cache()
    report, data, analyses = run_analysis()
    log.info(
        "load_report: done price=%.2f mode_cache=v%d",
        report["metrics"]["current_price"],
        _cache_version,
    )
    return report, data, analyses


try:
    with st.spinner("正在生成报告..."):
        report, data, analyses = load_report()
except Exception as exc:
    log.exception("report generation failed")
    st.error(f"数据获取失败: {exc}")
    st.stop()

mode = st.sidebar.radio("报告模式", ["机构完整报告", "短线策略图"], index=0)

if mode == "机构完整报告":
    render_institutional_report(report, data, analyses)
else:
    render_strategy_map(report, data, analyses)

with st.sidebar.expander("智能体决策链", expanded=False):
    render_agent_trace_sidebar(report)

with st.sidebar.expander("指标校验", expanded=False):
    st.table(indicator_table_rows([
        indicator_snapshot(data["5m"], "5m"),
        indicator_snapshot(data["15m"], "15m"),
    ]))

if st.sidebar.button("刷新报告"):
    log.info("user requested report refresh")
    load_report.clear()
    st.rerun()
