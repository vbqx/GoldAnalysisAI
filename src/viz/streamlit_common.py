"""Shared Streamlit bootstrap, report session cache, sidebar."""

from __future__ import annotations

import os
import uuid
from datetime import timedelta
from pathlib import Path

import streamlit as st

from src.core.run_config import RunConfig, coerce_run_config
from src.indicators.verify import indicator_snapshot, indicator_table_rows
from src.log import get_logger
from src.viz.dashboard_components import DASHBOARD_CSS
from src.viz.generation_state import drop_job, get_job, purge_expired
from src.viz.generation_worker import format_generation_error, start_generation
from src.viz.page_layout import render_page_hero
from src.viz.replay_loader import load_replay_bundle
from src.viz.run_config_panel import mode_value_to_label, render_run_config_panel, render_sidebar_replay
from src.viz.session_keys import (
    FORCE_REFRESH_KEY,
    GENERATION_ID_KEY,
    REPORT_CONFIG_FINGERPRINT_KEY,
    REPORT_GENERATION_ID_KEY,
    REPORT_SESSION_KEY,
    RUN_CONFIG_KEY,
    RUN_CONFIG_READY_KEY,
    RUN_CONFIG_REFRESH_UI_KEY,
    RUN_CONFIG_WIDGETS_SEEDED_KEY,
    SESSION_ID_KEY,
    invalidate_report_cache,
)

log = get_logger(__name__)

# Re-export session keys for legacy imports
__all__ = [
    "FORCE_REFRESH_KEY",
    "GENERATION_ID_KEY",
    "REPORT_SESSION_KEY",
    "RUN_CONFIG_KEY",
    "RUN_CONFIG_READY_KEY",
    "SESSION_ID_KEY",
    "bootstrap_env",
    "ensure_external_data",
    "ensure_report",
    "init_page",
    "page_setup",
    "render_page_hero",
    "render_sidebar_footer",
    "render_sidebar_header",
    "render_sidebar_refresh_button",
]


def _session_id() -> str:
    if SESSION_ID_KEY not in st.session_state:
        st.session_state[SESSION_ID_KEY] = str(uuid.uuid4())
    return str(st.session_state[SESSION_ID_KEY])


def _generation_id() -> str:
    if GENERATION_ID_KEY not in st.session_state:
        st.session_state[GENERATION_ID_KEY] = str(uuid.uuid4())
    return str(st.session_state[GENERATION_ID_KEY])


def _job_key() -> str:
    return f"{_session_id()}:{_generation_id()}"


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


def missing_runtime_dependencies() -> list[str]:
    """Packages required for live report generation (not replay-only)."""
    missing: list[str] = []
    try:
        import tvDatafeed  # noqa: F401
    except ModuleNotFoundError:
        missing.append("tvdatafeed-enhanced (import tvDatafeed)")
    return missing


def render_runtime_dependency_banner() -> None:
    missing = missing_runtime_dependencies()
    if not missing:
        return
    st.error(
        "缺少运行依赖："
        + "、".join(missing)
        + "。请在项目根目录执行 `python -m pip install -r requirements.txt`，"
        "然后用 `python run_app.py` 重启（不要用裸 `streamlit run`）。"
    )


def page_setup() -> None:
    from src.log import setup_logging

    bootstrap_env()
    setup_logging()
    st.markdown(DASHBOARD_CSS, unsafe_allow_html=True)


def init_page(*, title_suffix: str = "") -> None:
    from src.log import setup_logging

    bootstrap_env()
    setup_logging()
    title = "GoldAnalysisAI · XAUUSD"
    if title_suffix:
        title = f"{title} — {title_suffix}"
    st.set_page_config(page_title=title, page_icon="🥇", layout="wide")
    st.markdown(DASHBOARD_CSS, unsafe_allow_html=True)


def _on_request_reconfigure() -> None:
    log.info("user requested report reconfiguration")
    st.session_state[FORCE_REFRESH_KEY] = True
    st.session_state[RUN_CONFIG_READY_KEY] = False
    st.session_state[RUN_CONFIG_REFRESH_UI_KEY] = True
    st.session_state.pop(RUN_CONFIG_KEY, None)
    st.session_state.pop(RUN_CONFIG_WIDGETS_SEEDED_KEY, None)


def render_sidebar_refresh_button() -> None:
    st.sidebar.button(
        "重新配置 / 刷新报告",
        type="primary",
        on_click=_on_request_reconfigure,
        key="sidebar_refresh_report",
    )


def render_sidebar_header() -> None:
    st.sidebar.markdown("**GoldAnalysisAI**")
    from src.config import TV_EXCHANGE, TV_SYMBOL

    st.sidebar.caption(f"数据源: TradingView · {TV_EXCHANGE}:{TV_SYMBOL}")
    from src.config import LLM_MODEL, LLM_MODEL_FAST, LLM_MODEL_STRONG, short_model_name

    fast = short_model_name(LLM_MODEL_FAST)
    strong = short_model_name(LLM_MODEL_STRONG)
    report = short_model_name(LLM_MODEL)
    if fast == strong == report:
        st.sidebar.caption(f"LLM: {fast}")
    else:
        st.sidebar.caption(f"LLM 研究: {fast}")
        st.sidebar.caption(f"LLM 辩论/文案: {strong}" + (f" · 报告 {report}" if report not in (fast, strong) else ""))
    st.sidebar.caption("先选择运行模式再生成；切换页面不重新生成")
    render_sidebar_replay()
    render_sidebar_refresh_button()


def render_sidebar_footer(data: dict | None = None) -> None:
    active_config = coerce_run_config(st.session_state.get(RUN_CONFIG_KEY))
    if active_config is not None:
        mode = mode_value_to_label(active_config.agent_mode)
        st.sidebar.caption(f"当前模式: {mode} · `{active_config.fingerprint()}`")
    if data:
        with st.sidebar.expander("指标校验", expanded=False):
            st.table(indicator_table_rows([
                indicator_snapshot(data["5m"], "5m"),
                indicator_snapshot(data["15m"], "15m"),
            ]))


def _resolve_confirmed_run_config() -> RunConfig | None:
    return coerce_run_config(st.session_state.get(RUN_CONFIG_KEY))


def _render_waiting_ui(job_key_str: str, *, show_generation_ui: bool) -> None:
    from src.viz.pipeline_progress import (
        pipeline_progress_headline,
        render_live_llm_status_lightweight,
        render_progress_steps,
    )

    title = "正在生成机构级分析报告…" if show_generation_ui else "正在生成报告…"
    render_page_hero(
        title,
        "约 2–8 分钟 · 下方显示流水线步骤；完整 LLM I/O 生成后见「LLM 决策链」",
    )
    steps_slot = st.empty()
    llm_slot = st.empty()

    @st.fragment(run_every=timedelta(milliseconds=1000))
    def _live_poll() -> None:
        try:
            job = get_job(job_key_str, session_id=_session_id())
            live = job.live if job else {}
            steps = live.get("steps") or []
            with steps_slot.container():
                if steps:
                    render_progress_steps(steps, title="当前进度")
                else:
                    headline = pipeline_progress_headline(steps)
                    if headline:
                        st.caption(headline)
            with llm_slot.container():
                render_live_llm_status_lightweight(live)
            if job and (job.result is not None or job.error is not None):
                st.rerun()
        except Exception as exc:
            log.exception("live waiting UI render failed job=%s", job_key_str)
            st.warning(f"进度面板刷新异常（后台生成仍在继续）：{exc}")

    _live_poll()


def _render_external_waiting(job_key_str: str) -> None:
    from src.viz.pipeline_progress import (
        pipeline_progress_headline,
        render_live_llm_status_lightweight,
        render_progress_steps,
    )

    render_page_hero(
        "正在生成报告数据…",
        "K 线 · 金十 · DXY · 社媒 — 外部数据就绪后本页自动刷新",
    )
    steps_slot = st.empty()
    llm_slot = st.empty()

    @st.fragment(run_every=timedelta(milliseconds=1000))
    def _poll() -> None:
        try:
            job = get_job(job_key_str, session_id=_session_id())
            live = job.live if job else {}
            if live.get("external"):
                st.rerun()
            if job and (job.result is not None or job.error is not None):
                st.rerun()
            steps = live.get("steps") or []
            with steps_slot.container():
                if steps:
                    render_progress_steps(steps, title="流水线进度")
                else:
                    headline = pipeline_progress_headline(steps)
                    st.info(headline or "等待后台线程同步进度…")
            with llm_slot.container():
                render_live_llm_status_lightweight(live)
        except Exception as exc:
            log.exception("external waiting UI render failed job=%s", job_key_str)
            st.warning(f"进度面板刷新异常（后台生成仍在继续）：{exc}")

    _poll()


def ensure_external_data() -> dict:
    purge_expired()
    if st.session_state.pop(FORCE_REFRESH_KEY, False):
        invalidate_report_cache()
        st.session_state[RUN_CONFIG_READY_KEY] = False
        st.session_state.pop(RUN_CONFIG_KEY, None)
        st.session_state.pop(RUN_CONFIG_WIDGETS_SEEDED_KEY, None)

    if not st.session_state.get(RUN_CONFIG_READY_KEY):
        render_run_config_panel()

    run_config = _resolve_confirmed_run_config()
    if run_config is None:
        st.session_state[RUN_CONFIG_READY_KEY] = False
        render_run_config_panel()
    run_config_fingerprint = run_config.fingerprint()
    job_key_str = _job_key()

    if run_config.replay_mode and run_config.replay_run_id:
        from src.viz.external_data_view import external_payload_from_report

        try:
            bundle = load_replay_bundle(run_config)
        except ValueError as exc:
            st.error(f"回放记录加载失败: {exc}")
            st.stop()
        return external_payload_from_report(bundle[0], bundle[1])

    if REPORT_SESSION_KEY in st.session_state:
        cached_gen = st.session_state.get(REPORT_GENERATION_ID_KEY)
        cached_config = st.session_state.get(REPORT_CONFIG_FINGERPRINT_KEY)
        if cached_gen == _generation_id() and cached_config == run_config_fingerprint:
            from src.viz.external_data_view import external_payload_from_report

            report, data, _ = st.session_state[REPORT_SESSION_KEY]
            return external_payload_from_report(report, data)

    job = get_job(job_key_str, session_id=_session_id())
    if job and job.error is not None:
        exc = job.error
        job.error = None
        log.exception("report generation failed during external page wait")
        st.error(f"报告生成失败: {format_generation_error(exc)}")
        st.stop()

    if job and job.result is not None:
        from src.viz.external_data_view import external_payload_from_report

        return external_payload_from_report(job.result[0], job.result[1])

    if job and job.live.get("external"):
        return job.live["external"]

    start_generation(job_key_str, run_config, session_id=_session_id())
    _render_external_waiting(job_key_str)
    st.stop()


def ensure_report(*, show_generation_ui: bool = True) -> tuple[dict, dict, dict]:
    purge_expired()
    if st.session_state.pop(FORCE_REFRESH_KEY, False):
        invalidate_report_cache()
        st.session_state[RUN_CONFIG_READY_KEY] = False
        st.session_state.pop(RUN_CONFIG_KEY, None)
        st.session_state.pop(RUN_CONFIG_WIDGETS_SEEDED_KEY, None)

    if not st.session_state.get(RUN_CONFIG_READY_KEY):
        render_run_config_panel()

    run_config = _resolve_confirmed_run_config()
    if run_config is None:
        st.session_state[RUN_CONFIG_READY_KEY] = False
        render_run_config_panel()
    run_config_fingerprint = run_config.fingerprint()
    job_key_str = _job_key()

    if REPORT_SESSION_KEY in st.session_state:
        cached_gen = st.session_state.get(REPORT_GENERATION_ID_KEY)
        cached_config = st.session_state.get(REPORT_CONFIG_FINGERPRINT_KEY)
        if cached_gen == _generation_id() and cached_config == run_config_fingerprint:
            return st.session_state[REPORT_SESSION_KEY]

    job = get_job(job_key_str, session_id=_session_id())
    if job and job.error is not None:
        exc = job.error
        steps = job.live.get("steps") or []
        job.error = None
        log.exception("report generation failed")
        if steps:
            from src.viz.pipeline_progress import render_progress_steps

            st.markdown("**生成进度（失败前）**")
            render_progress_steps(steps, title="")
        st.error(f"报告生成失败: {format_generation_error(exc)}")
        st.caption("可在 `.env` 调整 `TV_FETCH_RETRIES` / `TV_FETCH_ROUND_RETRIES`；确认代理可用后点「重新配置 / 刷新报告」重试。")
        st.stop()

    start_generation(job_key_str, run_config, session_id=_session_id())
    job = get_job(job_key_str, session_id=_session_id())

    if not job or job.result is None:
        _render_waiting_ui(job_key_str, show_generation_ui=show_generation_ui)
        st.stop()

    bundle = job.result
    job.result = None
    return _store_report_bundle(job_key_str, bundle, run_config_fingerprint)


def _store_report_bundle(
    job_key_str: str,
    bundle: tuple[dict, dict, dict],
    run_config_fingerprint: str,
) -> tuple[dict, dict, dict]:
    drop_job(job_key_str, session_id=_session_id())
    st.session_state[REPORT_SESSION_KEY] = bundle
    st.session_state[REPORT_GENERATION_ID_KEY] = _generation_id()
    st.session_state[REPORT_CONFIG_FINGERPRINT_KEY] = run_config_fingerprint
    return bundle
