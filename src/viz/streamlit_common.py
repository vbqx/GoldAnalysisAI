"""Shared Streamlit bootstrap, report session cache, sidebar."""

from __future__ import annotations

import os
import threading
from datetime import timedelta
from pathlib import Path

import streamlit as st

from src.core.progress import ProgressReporter, reset_progress, set_progress
from src.indicators.verify import indicator_snapshot, indicator_table_rows
from src.log import get_logger
from src.pipeline import run_analysis
from src.viz.dashboard_components import DASHBOARD_CSS

log = get_logger(__name__)

REPORT_SESSION_KEY = "report_bundle"
FORCE_REFRESH_KEY = "force_refresh_report"
REFRESH_COUNTER_KEY = "report_refresh_counter"

_GEN_THREADS: dict[int, threading.Thread] = {}
_GEN_RESULTS: dict[int, tuple[dict, dict, dict]] = {}
_GEN_ERRORS: dict[int, BaseException] = {}
_LIVE_GEN_STATE: dict[int, dict] = {}
_GEN_LOCK = threading.Lock()


class _ModuleSyncProgressReporter(ProgressReporter):
    """Sync pipeline progress to module state for live UI polling (thread-safe enough)."""

    def __init__(self, counter: int) -> None:
        super().__init__()
        self._counter = counter
        self._sync()

    def _sync(self) -> None:
        _LIVE_GEN_STATE[self._counter] = {
            "steps": self.snapshot(),
            "llm_io": self.llm_io_snapshot(),
        }

    def _on_change(self) -> None:
        self._sync()

    def _on_llm_chunk(self, stage: str, chunk: str) -> None:
        rec = self._find_llm(stage)
        if rec:
            rec.output += chunk
        self._sync()

    def llm_begin(self, stage: str, model: str, messages: list[dict[str, str]]) -> None:
        super().llm_begin(stage, model, messages)
        self._sync()

    def llm_end(self, stage: str, output: str, *, error: str | None = None, latency_ms: int | None = None) -> None:
        super().llm_end(stage, output, error=error, latency_ms=latency_ms)
        self._sync()

    def fail(self, step_id: str, detail: str = "") -> None:
        super().fail(step_id, detail)
        self._sync()

    def done(self, step_id: str, detail: str = "") -> None:
        super().done(step_id, detail)
        self._sync()

    def update(self, step_id: str, *, detail: str | None = None, label: str | None = None) -> None:
        super().update(step_id, detail=detail, label=label)
        self._sync()

    def stage_io(self, stage: str, *, input_text: str, output_text: str, latency_ms: int | None = None, label: str | None = None) -> None:
        super().stage_io(stage, input_text=input_text, output_text=output_text, latency_ms=latency_ms, label=label)
        self._sync()


def bootstrap_env() -> None:
    env_path = Path(__file__).resolve().parents[2] / ".env"
    if env_path.exists():
        for line in env_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, val = line.split("=", 1)
            os.environ[key.strip()] = val.strip()

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


def page_setup() -> None:
    """Per-page bootstrap (navigation entry already called set_page_config)."""
    from src.log import setup_logging

    bootstrap_env()
    setup_logging()
    st.markdown(DASHBOARD_CSS, unsafe_allow_html=True)


def init_page(*, title_suffix: str = "") -> None:
    """Legacy single-app bootstrap; prefer app.py navigation + page_setup()."""
    from src.log import setup_logging

    bootstrap_env()
    setup_logging()
    title = "GoldAnalysisAI · XAUUSD"
    if title_suffix:
        title = f"{title} — {title_suffix}"
    st.set_page_config(page_title=title, page_icon="🥇", layout="wide")
    st.markdown(DASHBOARD_CSS, unsafe_allow_html=True)


def render_page_hero(title: str, subtitle: str = "") -> None:
    sub = f"<p>{subtitle}</p>" if subtitle else ""
    st.markdown(
        f'<div class="page-hero"><h1>{title}</h1>{sub}</div>',
        unsafe_allow_html=True,
    )


def render_sidebar_header() -> None:
    st.sidebar.markdown("**GoldAnalysisAI**")
    st.sidebar.caption("数据源: TradingView · OANDA:XAUUSD")
    # Fix #7 [Improvement] 侧边栏仅显示 STRONG 模型，与研究阶段 FAST 模型不一致
    from src.config import LLM_MODEL, LLM_MODEL_FAST, LLM_MODEL_STRONG, short_model_name

    fast = short_model_name(LLM_MODEL_FAST)
    strong = short_model_name(LLM_MODEL_STRONG)
    report = short_model_name(LLM_MODEL)
    if fast == strong == report:
        st.sidebar.caption(f"LLM: {fast}")
    else:
        st.sidebar.caption(f"LLM 研究: {fast}")
        st.sidebar.caption(f"LLM 辩论/文案: {strong}" + (f" · 报告 {report}" if report not in (fast, strong) else ""))
    st.sidebar.caption("切换页面不重新生成；点「刷新报告」才重跑流水线")


def render_sidebar_footer(data: dict) -> None:
    with st.sidebar.expander("指标校验", expanded=False):
        st.table(indicator_table_rows([
            indicator_snapshot(data["5m"], "5m"),
            indicator_snapshot(data["15m"], "15m"),
        ]))
    if st.sidebar.button("刷新报告", type="primary"):
        log.info("user requested report refresh")
        st.session_state[FORCE_REFRESH_KEY] = True
        st.rerun()


def _next_refresh_counter() -> int:
    if REFRESH_COUNTER_KEY not in st.session_state:
        st.session_state[REFRESH_COUNTER_KEY] = 0
    return int(st.session_state[REFRESH_COUNTER_KEY])


def _clear_generation_state(counter: int) -> None:
    _GEN_RESULTS.pop(counter, None)
    _GEN_ERRORS.pop(counter, None)
    _LIVE_GEN_STATE.pop(counter, None)
    thread = _GEN_THREADS.pop(counter, None)
    if thread and thread.is_alive():
        log.info("refresh requested while generation running counter=%s", counter)


def _start_generation(counter: int) -> None:
    with _GEN_LOCK:
        if counter in _GEN_RESULTS or counter in _GEN_ERRORS:
            return
        thread = _GEN_THREADS.get(counter)
        if thread and thread.is_alive():
            return

        def worker() -> None:
            from src.data.fetcher import clear_cache

            reporter = _ModuleSyncProgressReporter(counter)
            token = set_progress(reporter)
            try:
                clear_cache()
                bundle = run_analysis()
                _GEN_RESULTS[counter] = bundle
                log.info(
                    "report ready price=%.2f counter=%s",
                    bundle[0]["metrics"]["current_price"],
                    counter,
                )
            except BaseException as exc:
                log.exception("report generation failed counter=%s", counter)
                _GEN_ERRORS[counter] = exc
            finally:
                reset_progress(token)

        thread = threading.Thread(target=worker, daemon=True, name=f"report-gen-{counter}")
        _GEN_THREADS[counter] = thread
        thread.start()


def _render_waiting_ui(counter: int, *, show_generation_ui: bool) -> None:
    from src.viz.decision_page import render_live_generation_panel

    # Fix #3 [Bug] 子页面残留「报告尚未生成」提示
    # 原因：st.info 在 rerun 后仍残留在子页面；改用 st.empty() 容器，完成时可显式清除。
    placeholder = st.empty()
    with placeholder.container():
        if show_generation_ui:
            render_page_hero(
                "正在生成机构级分析报告…",
                "约 2–3 分钟 · 下方可实时查看生成步骤与 LLM 输入/输出",
            )
        else:
            # Fix #8 [Improvement] 子页面首次加载缺少流水线进度 UI
            # 原因：子页面 waiting 仅 st.info，无分步进度；与主页共用 hero + live panel。
            render_page_hero(
                "正在生成报告…",
                "约 2–3 分钟 · 下方可实时查看生成步骤与 LLM 输入/输出",
            )

    @st.fragment(run_every=timedelta(seconds=1))
    def _live_poll() -> None:
        render_live_generation_panel(_LIVE_GEN_STATE.get(counter, {}))
        if counter in _GEN_RESULTS or counter in _GEN_ERRORS:
            placeholder.empty()
            st.rerun()

    _live_poll()


def ensure_report(*, show_generation_ui: bool = True) -> tuple[dict, dict, dict]:
    """
    Return cached (report, data, analyses). Regenerate only on first visit or「刷新报告」.

    Generation runs in a background thread so widget clicks do not restart the pipeline.
    While waiting, the live decision-chain tabs are shown on the institutional page.
    """
    if st.session_state.pop(FORCE_REFRESH_KEY, False):
        old = _next_refresh_counter()
        st.session_state[REFRESH_COUNTER_KEY] = old + 1
        st.session_state.pop(REPORT_SESSION_KEY, None)
        _clear_generation_state(old)

    counter = _next_refresh_counter()

    if REPORT_SESSION_KEY in st.session_state:
        cached_counter = st.session_state.get(f"{REPORT_SESSION_KEY}_counter")
        if cached_counter == counter:
            return st.session_state[REPORT_SESSION_KEY]

    if counter in _GEN_ERRORS:
        exc = _GEN_ERRORS.pop(counter)
        live = _LIVE_GEN_STATE.pop(counter, {})
        steps = live.get("steps") or []
        log.exception("report generation failed")
        if steps:
            from src.viz.pipeline_progress import render_progress_steps

            st.markdown("**生成进度（失败前）**")
            render_progress_steps(steps, title="")
        st.error(f"数据获取失败: {exc}")
        st.caption("可在 `.env` 调整 `TV_FETCH_RETRIES` / `TV_FETCH_ROUND_RETRIES`；确认代理可用后点「刷新报告」重试。")
        st.stop()

    _start_generation(counter)

    if counter not in _GEN_RESULTS:
        _render_waiting_ui(counter, show_generation_ui=show_generation_ui)
        st.stop()

    bundle = _GEN_RESULTS.pop(counter)
    _LIVE_GEN_STATE.pop(counter, None)
    _GEN_THREADS.pop(counter, None)

    st.session_state[REPORT_SESSION_KEY] = bundle
    st.session_state[f"{REPORT_SESSION_KEY}_counter"] = counter

    # Fix #3 [Bug] 子页面残留「报告尚未生成」提示
    # 原因：show_generation_ui=False 时未 rerun，waiting fragment 与 st.info 残留在子页面。
    # 生成完成后统一 rerun 一次，下次从 session 缓存返回，页面不再显示等待 UI。
    st.rerun()
