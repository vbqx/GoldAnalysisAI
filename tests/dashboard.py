"""Streamlit test dashboard — live progress and logs.

Launch:
    streamlit run tests/dashboard.py --server.port 8502
"""
from __future__ import annotations

import html
import re
import sys
from datetime import timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st

from tests.runner import Suite, TestRunManager, load_catalog_summary

st.set_page_config(
    page_title="GoldAnalysisAI · 测试面板",
    page_icon="🧪",
    layout="wide",
)

st.markdown(
    """
<style>
.test-hero { background: linear-gradient(135deg,#0f172a,#1e3a5f); color:#f8fafc;
  padding:1.2rem 1.5rem; border-radius:12px; margin-bottom:1rem; }
.test-hero h1 { margin:0; font-size:1.5rem; }
.test-hero p { margin:.35rem 0 0; opacity:.85; font-size:.9rem; }
.log-box { font-family: ui-monospace, monospace; font-size: 12px;
  background:#0f172a; color:#e2e8f0; padding:12px; border-radius:8px;
  max-height:420px; overflow-y:auto; white-space:pre-wrap; }
</style>
""",
    unsafe_allow_html=True,
)

STATUS_CN = {
    "idle": "待机",
    "running": "运行中",
    "done": "全部通过",
    "failed": "有失败",
    "stopped": "已停止",
}

manager = TestRunManager.get()


def _format_elapsed(seconds: float) -> str:
    if seconds < 60:
        return f"{seconds:.0f}s"
    return f"{int(seconds // 60)}m {int(seconds % 60)}s"


def _fin_id_from_test(name: str) -> str:
    """Map pytest node name to catalog FIN-* id."""
    short = name.split("::")[-1]
    m = re.match(r"test_fin_(\d+)", short)
    if m:
        return f"FIN-{int(m.group(1)):02d}"
    return "—"


def _filter_catalog(cases: list[dict], mode: str) -> list[dict]:
    active = [c for c in cases if not c.get("deprecated")]
    if mode == "自动化":
        return [c for c in active if c.get("automated") == "true"]
    if mode == "金融 FIN":
        return [c for c in active if str(c.get("id", "")).startswith("FIN")]
    if mode == "手工":
        return [c for c in active if c.get("automated") != "true" and not str(c.get("id", "")).startswith("UI-")]
    return active


def render_header() -> None:
    st.markdown(
        """
<div class="test-hero">
  <h1>🧪 GoldAnalysisAI 测试面板</h1>
  <p>catalog 含 UIL / IND / FN / FIN / PERF 用例。快速套件 34 项（含 FIN #9–#13 修复验证）。集成测试每条约 3 分钟。</p>
</div>
""",
        unsafe_allow_html=True,
    )
    st.caption(
        "用例设计：tests/cases/test-plan.md · "
        "金融 Review：tests/cases/financial-review-cases.md"
    )


def render_controls() -> None:
    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
    with col1:
        suite_key = st.selectbox(
            "测试套件",
            options=[s.value for s in Suite],
            format_func=lambda v: Suite(v).label,
            disabled=manager.is_running(),
        )
    with col2:
        run = st.button("▶ 开始", type="primary", disabled=manager.is_running(), width="stretch")
    with col3:
        stop = st.button("⏹ 停止", disabled=not manager.is_running(), width="stretch")
    with col4:
        reset = st.button("↺ 清空", disabled=manager.is_running(), width="stretch")

    if run:
        manager.start(Suite(suite_key))
        st.rerun()
    if stop:
        manager.stop()
        st.rerun()
    if reset:
        manager.reset()
        st.rerun()


def _render_panel_body() -> None:
    state = manager.snapshot()

    m1, m2, m3, m4, m5, m6 = st.columns(6)
    m1.metric("状态", STATUS_CN.get(state.status, state.status))
    m2.metric("阶段", state.phase or "—")
    m3.metric("通过", state.passed)
    m4.metric("失败", state.failed)
    m5.metric("耗时", _format_elapsed(state.elapsed))
    m6.metric("Pipeline", f"{state.pipeline_elapsed:.0f}s" if state.pipeline_elapsed else "—")

    st.progress(state.progress, text=f"进度 {state.passed + state.failed + state.skipped}/{state.collected or '?'}")
    if state.current_test:
        st.caption(f"当前：**{state.current_test}**")

    tab_log, tab_results, tab_catalog = st.tabs(["实时日志", "用例结果", "用例目录"])

    with tab_log:
        log_text = html.escape("\n".join(state.logs[-200:]) if state.logs else "（等待开始…）")
        st.markdown(f'<div class="log-box">{log_text}</div>', unsafe_allow_html=True)

    with tab_results:
        if state.results:
            rows = [
                {
                    "用例ID": _fin_id_from_test(name),
                    "测试": name.split("::")[-1],
                    "状态": status,
                    "耗时(s)": round(state.durations.get(name, 0), 2),
                    "路径": name,
                }
                for name, status in state.results.items()
            ]
            st.dataframe(rows, width="stretch", hide_index=True)
        else:
            st.info("尚无结果，点击「开始」运行测试。")

    with tab_catalog:
        cases = load_catalog_summary()
        mode = st.radio("筛选", ["全部", "自动化", "金融 FIN", "手工"], horizontal=True, label_visibility="collapsed")
        shown = _filter_catalog(cases, mode)
        if shown:
            display = [
                {
                    "ID": c.get("id", ""),
                    "标题": c.get("title", ""),
                    "层": c.get("layer", c.get("suite", "")),
                    "优先级": c.get("priority", ""),
                    "自动化": c.get("automated", ""),
                    "Finding": c.get("finding", ""),
                    "Issue": c.get("issue", ""),
                }
                for c in shown
            ]
            st.dataframe(display, width="stretch", hide_index=True)
            st.caption(f"共 {len(shown)} 条（来源 catalog.yaml）")
        else:
            st.caption("无匹配用例。")

    if state.status == "done":
        st.success(f"测试完成：{state.passed} 通过，耗时 {_format_elapsed(state.elapsed)}")
    elif state.status == "failed":
        st.error(f"测试结束：{state.passed} 通过，{state.failed} 失败")
    elif state.status == "stopped":
        st.warning("测试已停止")


def render_live_panel() -> None:
    @st.fragment(run_every=timedelta(seconds=1))
    def _tick() -> None:
        _render_panel_body()
        if not manager.is_running():
            st.rerun()

    _tick()


def main() -> None:
    render_header()
    render_controls()
    if manager.is_running():
        render_live_panel()
    elif manager.snapshot().status != "idle":
        _render_panel_body()
    else:
        st.info("选择套件后点击 **开始**。推荐：**快速** 或 **金融 Review（FIN-*）**。")
        cases = load_catalog_summary()
        layers: dict[str, int] = {}
        for c in cases:
            if c.get("deprecated"):
                continue
            lid = c.get("id", "")
            if lid.startswith("FIN"):
                key = "financial"
            else:
                key = c.get("layer") or c.get("suite", "other")
            layers[key] = layers.get(key, 0) + 1
        if layers:
            st.caption("catalog 分布：" + " · ".join(f"{k}: {v}" for k, v in sorted(layers.items())))


if __name__ == "__main__":
    main()
else:
    main()
