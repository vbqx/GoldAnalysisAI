"""Shared Streamlit bootstrap, report session cache, sidebar."""

from __future__ import annotations

import os
import threading
from datetime import timedelta
from pathlib import Path

import streamlit as st

from src.core.progress import ProgressReporter, reset_progress, set_progress
from src.core.run_config import (
    RunConfig,
    apply_run_config,
    coerce_run_config,
    default_panel_run_config,
    run_config_for_mode,
    run_config_widget_state,
)
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
RUN_CONFIG_REFRESH_UI_KEY = "run_config_refresh_ui"
RUN_CONFIG_WIDGETS_SEEDED_KEY = "run_config_widgets_seeded"

_MODE_LABEL_TO_VALUE = {
    "规则引擎": "rule",
    "LLM 智能体": "llm",
    "混合模式": "hybrid",
}
_MODE_VALUE_TO_LABEL = {v: k for k, v in _MODE_LABEL_TO_VALUE.items()}
_ANALYST_LLM_WIDGETS: tuple[tuple[str, str, str], ...] = (
    ("run_config_llm_technical", "technical", "技术分析师"),
    ("run_config_llm_fundamentals", "fundamentals", "基本面分析师"),
    ("run_config_llm_news", "news", "新闻分析师"),
    ("run_config_llm_sentiment", "sentiment", "情绪分析师"),
)
_PIPELINE_STAGE_WIDGETS: tuple[tuple[str, str, bool], ...] = (
    ("run_config_stage_bullish", "看多研究", False),
    ("run_config_stage_bearish", "看空研究", False),
    ("run_config_stage_debate", "多空辩论", False),
    ("run_config_stage_levels", "LLM 点位提案", False),
    ("run_config_stage_trader", "交易员", False),
    ("run_config_stage_risk", "风控团队", False),
    ("run_config_stage_manager", "经理决策", False),
)
_RESERVED_STAGE_HELP = "高级 LLM 阶段开关会写入本次生成配置"

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
        with self._lock:
            prev = _LIVE_GEN_STATE.get(self._counter, {})
            external = self.external_snapshot or prev.get("external")
            snapshot = {
                "steps": self.snapshot(),
                "llm_io": self.llm_io_snapshot(),
                "external": external,
            }
        _LIVE_GEN_STATE[self._counter] = snapshot

    def _on_change(self) -> None:
        self._sync()

    def _on_llm_chunk(self, stage: str, chunk: str) -> None:
        super()._on_llm_chunk(stage, chunk)
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


def _on_request_reconfigure() -> None:
    """Sidebar callback — runs before the next script pass so ensure_* sees flags immediately."""
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


def _saved_run_config_for_panel() -> RunConfig:
    """Prefill for the config panel; always default to rule engine on each new visit."""
    return default_panel_run_config()


def _apply_widget_state_from_run_config(config: RunConfig) -> None:
    for key, value in run_config_widget_state(config).items():
        st.session_state[key] = value


def _seed_run_config_widgets_if_needed(seed: RunConfig, *, force: bool = False) -> None:
    """Prefill widgets once per config-panel visit; never overwrite user edits on rerun."""
    if force or not st.session_state.get(RUN_CONFIG_WIDGETS_SEEDED_KEY):
        _apply_widget_state_from_run_config(seed)
        st.session_state[RUN_CONFIG_WIDGETS_SEEDED_KEY] = True


def _resolve_confirmed_run_config() -> RunConfig | None:
    cfg = coerce_run_config(st.session_state.get(RUN_CONFIG_KEY))
    if cfg is not None:
        return cfg
    return None


def render_sidebar_header() -> None:
    st.sidebar.markdown("**GoldAnalysisAI**")
    from src.config import TV_EXCHANGE, TV_SYMBOL

    st.sidebar.caption(f"数据源: TradingView · {TV_EXCHANGE}:{TV_SYMBOL}")
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
    render_sidebar_refresh_button()


def render_sidebar_footer(data: dict | None = None) -> None:
    active_config = coerce_run_config(st.session_state.get(RUN_CONFIG_KEY))
    if active_config is not None:
        mode = _MODE_VALUE_TO_LABEL.get(active_config.agent_mode, active_config.agent_mode)
        st.sidebar.caption(f"当前模式: {mode} · `{active_config.fingerprint()}`")
    if data:
        with st.sidebar.expander("指标校验", expanded=False):
            st.table(indicator_table_rows([
                indicator_snapshot(data["5m"], "5m"),
                indicator_snapshot(data["15m"], "15m"),
            ]))


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



def _set_all_agent_llm_widgets(select: bool) -> None:
    """Toggle all advanced agent LLM stage widgets (Analyst Team + pipeline + sub-analysts)."""
    st.session_state["run_config_stage_analysts"] = select
    for key, _, _ in _PIPELINE_STAGE_WIDGETS:
        st.session_state[key] = select
    for key, _, _ in _ANALYST_LLM_WIDGETS:
        st.session_state[key] = select


def _analyst_checkbox_state() -> tuple[str, int]:
    """Return (llm_analyst_only, checked_count). llm_analyst_only is '__multi__' when invalid."""
    checked = [stage for key, stage, _ in _ANALYST_LLM_WIDGETS if st.session_state.get(key, True)]
    n = len(checked)
    if n in (0, 4):
        return "", n
    if n == 1:
        return checked[0], 1
    return "__multi__", n


def _selected_run_config() -> RunConfig:
    mode_label = st.session_state.get("run_config_mode_label", "规则引擎")
    mode = _MODE_LABEL_TO_VALUE.get(mode_label, "rule")
    if mode == "rule":
        return run_config_for_mode("rule")

    advanced = bool(st.session_state.get("run_config_advanced", False))
    if not advanced:
        return run_config_for_mode(
            mode,  # type: ignore[arg-type]
            llm_enabled=bool(st.session_state.get("run_config_llm_narrative", True)),
            llm_analyst_only="",
        )

    analyst_only, checked_count = _analyst_checkbox_state()
    stage_analysts = bool(st.session_state.get("run_config_stage_analysts", True))
    if checked_count == 0:
        stage_analysts = False

    return RunConfig(
        agent_mode=mode,  # type: ignore[arg-type]
        llm_enabled=bool(st.session_state.get("run_config_llm_narrative", True)),
        llm_stage_analysts=stage_analysts,
        llm_stage_bullish=bool(st.session_state.get("run_config_stage_bullish", True)),
        llm_stage_bearish=bool(st.session_state.get("run_config_stage_bearish", True)),
        llm_stage_debate=bool(st.session_state.get("run_config_stage_debate", True)),
        llm_stage_levels=bool(st.session_state.get("run_config_stage_levels", True)),
        llm_stage_trader=bool(st.session_state.get("run_config_stage_trader", False)),
        llm_stage_risk=bool(st.session_state.get("run_config_stage_risk", False)),
        llm_stage_manager=bool(st.session_state.get("run_config_stage_manager", False)),
        llm_analyst_only="" if analyst_only == "__multi__" else analyst_only,
    ).normalized()


def _render_run_mode_guide() -> None:
    st.markdown(
        """
<div class="run-mode-guide">
  <div class="run-mode-card fast">
    <p class="name">规则引擎</p>
    <p class="desc">最快路径，不调用 LLM；适合检查数据、指标和交易假设几何关系。</p>
  </div>
  <div class="run-mode-card recommended">
    <p class="name">混合模式</p>
    <p class="desc">推荐默认项；先跑规则基线，再用 LLM 增强研究、辩论和文案。</p>
  </div>
  <div class="run-mode-card deep">
    <p class="name">LLM 智能体</p>
    <p class="desc">完整智能体链路；适合深度复盘、审计决策过程和调试提示词。</p>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )


def _render_run_config_advanced_controls() -> None:
    pick_col, clear_col, _ = st.columns([1, 1, 4])
    with pick_col:
        st.button(
            "一键全选",
            on_click=_set_all_agent_llm_widgets,
            args=(True,),
            key="run_config_select_all_llm",
        )
    with clear_col:
        st.button(
            "全部取消",
            on_click=_set_all_agent_llm_widgets,
            args=(False,),
            key="run_config_clear_all_llm",
        )
    st.markdown("**分析师团队**")
    st.checkbox("启用 Analyst Team LLM", key="run_config_stage_analysts")
    st.markdown("**研究 · 辩论 · 执行链**")
    stage_cols = st.columns(3)
    for idx, (key, label, reserved) in enumerate(_PIPELINE_STAGE_WIDGETS):
        with stage_cols[idx % 3]:
            st.checkbox(
                label,
                key=key,
                help=_RESERVED_STAGE_HELP if reserved else None,
            )
    st.markdown("**Analyst 子模块**（仅勾选的走 LLM，其余用规则补齐；四者全选 = 四位均 LLM；全不选 = 分析师团队均规则）")
    col_a, col_b = st.columns(2)
    with col_a:
        for key, _stage, label in _ANALYST_LLM_WIDGETS[:2]:
            st.checkbox(label, key=key)
    with col_b:
        for key, _stage, label in _ANALYST_LLM_WIDGETS[2:]:
            st.checkbox(label, key=key)
    _analyst_only, _ = _analyst_checkbox_state()
    if _analyst_only == "__multi__":
        st.warning("单 Analyst 调试请只勾选一个，或四个全部勾选。")


def _render_run_config_panel() -> None:
    from src.llm.router import llm_configured

    seed = _saved_run_config_for_panel()
    is_refresh = bool(st.session_state.pop(RUN_CONFIG_REFRESH_UI_KEY, False))
    _seed_run_config_widgets_if_needed(seed, force=is_refresh)
    hero_title = "重新生成配置" if is_refresh else "生成前配置"
    hero_sub = (
        "默认选择规则引擎，可调整后点击「开始生成报告」"
        if is_refresh
        else "默认选择规则引擎模式，可调整后点击「开始生成报告」"
    )
    render_page_hero(hero_title, hero_sub)

    st.markdown("#### 运行模式")
    _render_run_mode_guide()
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
        st.session_state["run_config_llm_narrative"] = False
        st.session_state["run_config_advanced"] = False
        st.info("规则引擎模式不会调用 LLM，适合快速生成与排查数据/指标问题。")
    elif mode == "llm":
        st.info("LLM 智能体模式会启用分析师团队、看多/看空研究、辩论与可选报告文案。")
    else:
        st.info("混合模式会先跑规则基线，LLM 置信度达标时覆盖对应阶段。")

    if needs_llm and not llm_ready:
        st.warning("当前未配置 `LLM_API_KEY`，请先配置密钥，或选择规则引擎模式。")

    st.checkbox(
        "启用 LLM 报告文案",
        disabled=not needs_llm,
        key="run_config_llm_narrative",
        help="这是流水线末尾的报告叙述层，独立于智能体链。规则模式下固定关闭。",
    )

    st.checkbox(
        "高级调试",
        disabled=not needs_llm,
        key="run_config_advanced",
        help="勾选后可分阶段、分 Analyst 控制 LLM 调用范围。",
    )

    if needs_llm and st.session_state.get("run_config_advanced"):
        with st.expander("高级调试：阶段与 Analyst 控制", expanded=False):
            _render_run_config_advanced_controls()

    config = _selected_run_config()
    st.caption(f"预填配置指纹: `{seed.fingerprint()}` · 本次配置指纹: `{config.fingerprint()}`")

    _analyst_only, _ = _analyst_checkbox_state()
    analyst_invalid = (
        needs_llm
        and st.session_state.get("run_config_advanced")
        and _analyst_only == "__multi__"
    )
    start_disabled = (needs_llm and not llm_ready) or analyst_invalid
    if st.button("开始生成报告", type="primary", disabled=start_disabled):
        st.session_state[RUN_CONFIG_KEY] = config
        st.session_state[RUN_CONFIG_READY_KEY] = True
        st.session_state.pop(RUN_CONFIG_WIDGETS_SEEDED_KEY, None)
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


def _format_generation_error(exc: BaseException) -> str:
    raw = str(exc or type(exc).__name__).strip()
    if not raw:
        return type(exc).__name__
    network_hint = "若在国内网络，可能需要代理/VPN 才能连接 TradingView WebSocket。"
    raw = raw.replace(f"{network_hint}. {network_hint}", network_hint)
    raw = raw.replace(f"{network_hint}。 {network_hint}", network_hint)
    if "TradingView fetch failed" in raw:
        if "returned empty data" in raw:
            return f"数据拉取失败：TradingView 返回空数据。{network_hint}"
        return f"数据拉取失败：{raw}"
    return raw


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

    @st.fragment(run_every=timedelta(milliseconds=400))
    def _live_poll() -> None:
        render_live_generation_panel(_LIVE_GEN_STATE.get(counter, {}))
        if counter in _GEN_RESULTS or counter in _GEN_ERRORS:
            # Do not placeholder.empty() here — it clears the page before rerun and
            # leaves a blank screen if the next pass fails to render immediately.
            st.rerun()

    _live_poll()


def _fetch_step_status(steps: list[dict] | None) -> str | None:
    for step in reversed(steps or []):
        if step.get("id") == "fetch":
            return step.get("status")
    return None


def _render_external_waiting(counter: int) -> None:
    render_page_hero(
        "正在拉取外部数据…",
        "K 线 · 金十快讯/资讯/日历 · DXY · TV 社媒 — 完成后本页自动刷新",
    )

    @st.fragment(run_every=timedelta(seconds=1))
    def _poll() -> None:
        live = _LIVE_GEN_STATE.get(counter, {})
        if live.get("external"):
            st.rerun()
        if counter in _GEN_RESULTS or counter in _GEN_ERRORS:
            st.rerun()
        steps = live.get("steps") or []
        fetch_status = _fetch_step_status(steps)
        if fetch_status == "running":
            st.info("数据拉取进行中…")
        elif fetch_status == "error":
            st.error("数据拉取失败，请查看机构报告页或点侧边栏重试。")
        else:
            st.info("等待流水线启动…")

    _poll()


def ensure_external_data() -> dict:
    """
    Return external-data payload. Waits only until fetch completes (not full report).
    Uses cached report external when the full bundle is already in session.
    """
    if st.session_state.pop(FORCE_REFRESH_KEY, False):
        _invalidate_report_cache()
        st.session_state[RUN_CONFIG_READY_KEY] = False
        st.session_state.pop(RUN_CONFIG_KEY, None)
        st.session_state.pop(RUN_CONFIG_WIDGETS_SEEDED_KEY, None)

    if not st.session_state.get(RUN_CONFIG_READY_KEY):
        _render_run_config_panel()

    run_config = _resolve_confirmed_run_config()
    if run_config is None:
        st.session_state[RUN_CONFIG_READY_KEY] = False
        _render_run_config_panel()
    run_config_fingerprint = run_config.fingerprint()
    counter = _next_refresh_counter()

    if REPORT_SESSION_KEY in st.session_state:
        cached_counter = st.session_state.get(f"{REPORT_SESSION_KEY}_counter")
        cached_config = st.session_state.get(REPORT_CONFIG_FINGERPRINT_KEY)
        if cached_counter == counter and cached_config == run_config_fingerprint:
            from src.viz.external_data_view import external_payload_from_report

            report, data, _ = st.session_state[REPORT_SESSION_KEY]
            return external_payload_from_report(report, data)

    if counter in _GEN_ERRORS:
        exc = _GEN_ERRORS.pop(counter)
        _LIVE_GEN_STATE.pop(counter, None)
        log.exception("report generation failed during external page wait")
        st.error(f"报告生成失败: {_format_generation_error(exc)}")
        st.stop()

    if counter in _GEN_RESULTS:
        bundle = _GEN_RESULTS.get(counter)
        if bundle:
            from src.viz.external_data_view import external_payload_from_report

            return external_payload_from_report(bundle[0], bundle[1])

    live = _LIVE_GEN_STATE.get(counter, {})
    if live.get("external"):
        return live["external"]

    _start_generation(counter, run_config)

    _render_external_waiting(counter)
    st.stop()


def ensure_report(*, show_generation_ui: bool = True) -> tuple[dict, dict, dict]:
    """
    Return cached (report, data, analyses). Generate only after run config is confirmed.

    Generation runs in a background thread so widget clicks do not restart the pipeline.
    While waiting, live decision-chain tabs are shown on the current page.
    """
    if st.session_state.pop(FORCE_REFRESH_KEY, False):
        _invalidate_report_cache()
        st.session_state[RUN_CONFIG_READY_KEY] = False
        st.session_state.pop(RUN_CONFIG_KEY, None)
        st.session_state.pop(RUN_CONFIG_WIDGETS_SEEDED_KEY, None)

    if not st.session_state.get(RUN_CONFIG_READY_KEY):
        _render_run_config_panel()

    run_config = _resolve_confirmed_run_config()
    if run_config is None:
        st.session_state[RUN_CONFIG_READY_KEY] = False
        _render_run_config_panel()
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
        st.error(f"报告生成失败: {_format_generation_error(exc)}")
        st.caption("可在 `.env` 调整 `TV_FETCH_RETRIES` / `TV_FETCH_ROUND_RETRIES`；确认代理可用后点「重新配置 / 刷新报告」重试。")
        st.stop()

    _start_generation(counter, run_config)

    if counter not in _GEN_RESULTS:
        _render_waiting_ui(counter, show_generation_ui=show_generation_ui)
        st.stop()

    return _store_report_bundle(counter, _GEN_RESULTS.pop(counter), run_config_fingerprint)


def _store_report_bundle(
    counter: int,
    bundle: tuple[dict, dict, dict],
    run_config_fingerprint: str,
) -> tuple[dict, dict, dict]:
    """Persist a finished pipeline bundle and clear in-flight generation state."""
    _LIVE_GEN_STATE.pop(counter, None)
    _GEN_THREADS.pop(counter, None)

    st.session_state[REPORT_SESSION_KEY] = bundle
    st.session_state[f"{REPORT_SESSION_KEY}_counter"] = counter
    st.session_state[REPORT_CONFIG_FINGERPRINT_KEY] = run_config_fingerprint

    # Fix #3 [Bug] 全量 LLM 完成后页面空白
    # 原因：fragment 先 empty() 再 rerun，ensure_report 缓存后又 st.rerun()，中间两次 rerun
    # 都未渲染正文，用户看到白屏。改为同一次 rerun 内写入 session 并直接 return。
    return bundle
