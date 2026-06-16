"""Shared Streamlit bootstrap, report session cache, sidebar."""

from __future__ import annotations

import os
import threading
from datetime import timedelta
from pathlib import Path

import streamlit as st

from src.core.progress import ProgressReporter, reset_progress, set_progress
from src.core.run_config import RunConfig, run_config_for_mode, run_config_from_env, apply_run_config
from src.indicators.verify import indicator_snapshot, indicator_table_rows
from src.log import get_logger
from src.pipeline import run_analysis
from src.viz.dashboard_components import DASHBOARD_CSS

log = get_logger(__name__)

REPORT_SESSION_KEY = "report_bundle"
FORCE_REFRESH_KEY = "force_refresh_report"
REFRESH_COUNTER_KEY = "report_refresh_counter"
RUN_CONFIG_KEY = "report_run_config"
RUN_CONFIG_READY_KEY = "report_run_config_ready"
REPORT_CONFIG_FINGERPRINT_KEY = f"{REPORT_SESSION_KEY}_run_config_fingerprint"

_MODE_LABEL_TO_VALUE = {
    "规则引擎": "rule",
    "LLM 智能体": "llm",
    "混合模式": "hybrid",
}
_MODE_VALUE_TO_LABEL = {v: k for k, v in _MODE_LABEL_TO_VALUE.items()}
_ANALYST_ONLY_OPTIONS = {
    "全部": "",
    "technical": "technical",
    "fundamentals": "fundamentals",
    "news": "news",
    "sentiment": "sentiment",
}

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
    st.sidebar.caption("先选择运行模式再生成；切换页面不重新生成")


def render_sidebar_footer(data: dict) -> None:
    active_config = st.session_state.get(RUN_CONFIG_KEY)
    if isinstance(active_config, RunConfig):
        st.sidebar.caption(f"当前模式: {_MODE_VALUE_TO_LABEL.get(active_config.agent_mode, active_config.agent_mode)}")
    with st.sidebar.expander("指标校验", expanded=False):
        st.table(indicator_table_rows([
            indicator_snapshot(data["5m"], "5m"),
            indicator_snapshot(data["15m"], "15m"),
        ]))
    if st.sidebar.button("重新配置 / 刷新报告", type="primary"):
        log.info("user requested report reconfiguration")
        st.session_state[FORCE_REFRESH_KEY] = True
        st.session_state[RUN_CONFIG_READY_KEY] = False
        st.rerun()


def _next_refresh_counter() -> int:
    if REFRESH_COUNTER_KEY not in st.session_state:
        st.session_state[REFRESH_COUNTER_KEY] = 0
    return int(st.session_state[REFRESH_COUNTER_KEY])


def _invalidate_report_cache() -> None:
    old = _next_refresh_counter()
    st.session_state[REFRESH_COUNTER_KEY] = old + 1
    st.session_state.pop(REPORT_SESSION_KEY, None)
    st.session_state.pop(f"{REPORT_SESSION_KEY}_counter", None)
    st.session_state.pop(REPORT_CONFIG_FINGERPRINT_KEY, None)
    _clear_generation_state(old)


def _init_run_config_widgets() -> None:
    env_config = run_config_from_env()
    st.session_state.setdefault("run_config_mode_label", _MODE_VALUE_TO_LABEL.get(env_config.agent_mode, "规则引擎"))
    st.session_state.setdefault("run_config_llm_narrative", env_config.llm_enabled)
    analyst_label = next((label for label, value in _ANALYST_ONLY_OPTIONS.items() if value == env_config.llm_analyst_only), "全部")
    st.session_state.setdefault("run_config_analyst_only", analyst_label)


def _selected_run_config() -> RunConfig:
    mode_label = st.session_state.get("run_config_mode_label", "规则引擎")
    mode = _MODE_LABEL_TO_VALUE.get(mode_label, "rule")
    analyst_label = st.session_state.get("run_config_analyst_only", "全部")
    analyst_only = _ANALYST_ONLY_OPTIONS.get(analyst_label, "")
    return run_config_for_mode(
        mode,  # type: ignore[arg-type]
        llm_enabled=bool(st.session_state.get("run_config_llm_narrative", mode != "rule")),
        llm_analyst_only=analyst_only,
    )


def _render_run_config_panel() -> None:
    from src.llm.router import llm_configured

    _init_run_config_widgets()
    render_page_hero("生成前配置", "选择规则或 LLM 后再开始拉取数据，避免启动即更新报告")

    st.markdown("#### 运行模式")
    mode_label = st.radio(
        "选择本次报告使用的智能体模式",
        list(_MODE_LABEL_TO_VALUE),
        horizontal=True,
        key="run_config_mode_label",
    )
    mode = _MODE_LABEL_TO_VALUE.get(mode_label, "rule")
    needs_llm = mode != "rule"
    llm_ready = llm_configured()

    if mode == "rule":
        st.info("规则引擎模式不会调用 LLM，适合快速生成与排查数据/指标问题。")
    elif mode == "llm":
        st.info("LLM 智能体模式会启用分析师团队、看多/看空研究、辩论与可选报告文案。")
    else:
        st.info("混合模式会先跑规则基线，LLM 置信度达标时覆盖对应阶段。")

    if needs_llm and not llm_ready:
        st.warning("当前未配置 `LLM_API_KEY`，请先配置密钥，或选择规则引擎模式。")

    st.checkbox(
        "启用 LLM 报告文案",
        value=needs_llm,
        disabled=not needs_llm,
        key="run_config_llm_narrative",
        help="这是流水线末尾的报告叙述层，独立于智能体链。规则模式下固定关闭。",
    )

    with st.expander("高级调试", expanded=False):
        st.selectbox(
            "仅运行单个 Analyst LLM",
            list(_ANALYST_ONLY_OPTIONS),
            disabled=not needs_llm,
            key="run_config_analyst_only",
            help="用于调试单个分析师；未选中的分析师使用规则输出补齐。",
        )

    config = _selected_run_config()
    st.caption(f"本次配置指纹: `{config.fingerprint()}`")

    start_disabled = needs_llm and not llm_ready
    if st.button("开始生成报告", type="primary", disabled=start_disabled):
        st.session_state[RUN_CONFIG_KEY] = config
        st.session_state[RUN_CONFIG_READY_KEY] = True
        _invalidate_report_cache()
        log.info("user started report generation config=%s", config.to_dict())
        st.rerun()

    st.stop()


def _clear_generation_state(counter: int) -> None:
    _GEN_RESULTS.pop(counter, None)
    _GEN_ERRORS.pop(counter, None)
    _LIVE_GEN_STATE.pop(counter, None)
    thread = _GEN_THREADS.pop(counter, None)
    if thread and thread.is_alive():
        log.info("refresh requested while generation running counter=%s", counter)


def _start_generation(counter: int, run_config: RunConfig) -> None:
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
                apply_run_config(run_config)
                clear_cache()
                bundle = run_analysis()
                bundle[0].setdefault("meta", {})["run_config"] = run_config.to_dict()
                bundle[0]["meta"]["run_config_fingerprint"] = run_config.fingerprint()
                _GEN_RESULTS[counter] = bundle
                log.info(
                    "report ready price=%.2f counter=%s config=%s",
                    bundle[0]["metrics"]["current_price"],
                    counter,
                    run_config.to_dict(),
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
    Return cached (report, data, analyses). Generate only after run config is confirmed.

    Generation runs in a background thread so widget clicks do not restart the pipeline.
    While waiting, live decision-chain tabs are shown on the current page.
    """
    if st.session_state.pop(FORCE_REFRESH_KEY, False):
        _invalidate_report_cache()
        st.session_state[RUN_CONFIG_READY_KEY] = False

    if not st.session_state.get(RUN_CONFIG_READY_KEY):
        _render_run_config_panel()

    run_config = st.session_state.get(RUN_CONFIG_KEY)
    if not isinstance(run_config, RunConfig):
        run_config = run_config_from_env()
        st.session_state[RUN_CONFIG_KEY] = run_config
    run_config_fingerprint = run_config.fingerprint()
    counter = _next_refresh_counter()

    if REPORT_SESSION_KEY in st.session_state:
        cached_counter = st.session_state.get(f"{REPORT_SESSION_KEY}_counter")
        cached_config = st.session_state.get(REPORT_CONFIG_FINGERPRINT_KEY)
        if cached_counter == counter and cached_config == run_config_fingerprint:
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
        st.caption("可在 `.env` 调整 `TV_FETCH_RETRIES` / `TV_FETCH_ROUND_RETRIES`；确认代理可用后点「重新配置 / 刷新报告」重试。")
        st.stop()

    _start_generation(counter, run_config)

    if counter not in _GEN_RESULTS:
        _render_waiting_ui(counter, show_generation_ui=show_generation_ui)
        st.stop()

    bundle = _GEN_RESULTS.pop(counter)
    _LIVE_GEN_STATE.pop(counter, None)
    _GEN_THREADS.pop(counter, None)

    st.session_state[REPORT_SESSION_KEY] = bundle
    st.session_state[f"{REPORT_SESSION_KEY}_counter"] = counter
    st.session_state[REPORT_CONFIG_FINGERPRINT_KEY] = run_config_fingerprint

    # Fix #3 [Bug] 子页面残留「报告尚未生成」提示
    # 原因：show_generation_ui=False 时未 rerun，waiting fragment 与 st.info 残留在子页面。
    # 生成完成后统一 rerun 一次，下次从 session 缓存返回，页面不再显示等待 UI。
    st.rerun()
