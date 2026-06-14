"""Streamlit test dashboard — live progress and logs.

Launch:
    streamlit run tests/dashboard.py --server.port 8502
"""
from __future__ import annotations

import html
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
.status-idle { color:#64748b; } .status-running { color:#38bdf8; }
.status-done { color:#22c55e; } .status-failed { color:#ef4444; }
.status-stopped { color:#f59e0b; }
.log-box { font-family: ui-monospace, monospace; font-size: 12px;
  background:#0f172a; color:#e2e8f0; padding:12px; border-radius:8px;
  max-height:420px; overflow-y:auto; white-space:pre-wrap; }
</style>
""",
    unsafe_allow_html=True,
)

STATUS_CN = {
    "idle": ("待机", "status-idle"),
    "running": ("运行中", "status-running"),
    "done": ("全部通过", "status-done"),
    "failed": ("有失败", "status-failed"),
    "stopped": ("已停止", "status-stopped"),
}

manager = TestRunManager.get()


def _format_elapsed(seconds: float) -> str:
    if seconds < 60:
        return f"{seconds:.0f}s"
    return f"{int(seconds // 60)}m {int(seconds % 60)}s"


def render_header() -> None:
    st.markdown(
        """
<div class="test-hero">
  <h1>🧪 GoldAnalysisAI 测试面板</h1>
  <p>实时查看 pytest 进度、通过/失败统计与流水线日志。集成测试每条约 3 分钟，请勿重复点击「开始」。</p>
</div>
""",
        unsafe_allow_html=True,
    )


def render_controls() -> Suite:
    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
    with col1:
        suite_key = st.selectbox(
            "测试套件",
            options=[s.value for s in Suite],
            format_func=lambda v: Suite(v).label,
            disabled=manager.is_running(),
        )
    suite = Suite(suite_key)
    with col2:
        run = st.button("▶ 开始", type="primary", disabled=manager.is_running(), use_container_width=True)
    with col3:
        stop = st.button("⏹ 停止", disabled=not manager.is_running(), use_container_width=True)
    with col4:
        reset = st.button("↺ 清空", disabled=manager.is_running(), use_container_width=True)

    if run:
        manager.start(suite)
        st.rerun()
    if stop:
        manager.stop()
        st.rerun()
    if reset:
        manager.reset()
        st.rerun()
    return suite


def _render_panel_body() -> None:
    state = manager.snapshot()
    label, css = STATUS_CN.get(state.status, ("未知", "status-idle"))

    m1, m2, m3, m4, m5, m6 = st.columns(6)
    m1.metric("状态", label)
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
                    "测试": name.split("::")[-1],
                    "完整路径": name,
                    "状态": status,
                    "耗时(s)": round(state.durations.get(name, 0), 2),
                }
                for name, status in state.results.items()
            ]
            st.dataframe(rows, use_container_width=True, hide_index=True)
        else:
            st.info("尚无结果，点击「开始」运行测试。")

    with tab_catalog:
        cases = load_catalog_summary()
        auto = [c for c in cases if c.get("automated") == "true" and not c.get("deprecated")]
        if auto:
            st.dataframe(auto, use_container_width=True, hide_index=True)
        else:
            st.caption("catalog.yaml 未解析到自动化用例。")

    if state.status in ("done", "failed", "stopped"):
        if state.status == "done":
            st.success(f"测试完成：{state.passed} 通过，耗时 {_format_elapsed(state.elapsed)}")
        elif state.status == "failed":
            st.error(f"测试结束：{state.passed} 通过，{state.failed} 失败")
        else:
            st.warning("测试已停止")


def render_live_panel() -> None:
    """Auto-refresh while running; rerun full page when finished so buttons unlock."""

    @st.fragment(run_every=timedelta(seconds=1))
    def _tick() -> None:
        _render_panel_body()
        if not manager.is_running():
            st.rerun()

    _tick()


def render_static_panel() -> None:
    _render_panel_body()


def main() -> None:
    render_header()
    render_controls()
    if manager.is_running():
        render_live_panel()
    else:
        state = manager.snapshot()
        if state.status != "idle":
            render_static_panel()
        else:
            st.info("选择套件后点击 **开始**。推荐先用「快速（单元 + 回归）」约 3 秒完成。")
            cases = load_catalog_summary()
            layers = {}
            for c in cases:
                if c.get("deprecated"):
                    continue
                layer = c.get("layer") or c.get("suite", "other")
                layers.setdefault(layer, 0)
                layers[layer] += 1
            if layers:
                st.caption("catalog 用例分布：" + " · ".join(f"{k}: {v}" for k, v in sorted(layers.items())))


if __name__ == "__main__":
    main()
else:
    main()
