"""Streamlit run-config panel and replay controls."""

from __future__ import annotations

import streamlit as st

from src.core.run_config import RunConfig, default_panel_run_config, run_config_for_mode, run_config_widget_state
from src.log import get_logger
from src.viz.session_keys import (
    FORCE_REFRESH_KEY,
    RUN_CONFIG_KEY,
    RUN_CONFIG_READY_KEY,
    RUN_CONFIG_REFRESH_UI_KEY,
    RUN_CONFIG_WIDGETS_SEEDED_KEY,
    invalidate_report_cache,
)
from src.viz.page_layout import render_page_hero

log = get_logger(__name__)

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


def mode_label_to_value(label: str) -> str:
    return _MODE_LABEL_TO_VALUE.get(label, "rule")


def mode_value_to_label(value: str) -> str:
    return _MODE_VALUE_TO_LABEL.get(value, value)


def _apply_widget_state_from_run_config(config: RunConfig) -> None:
    for key, value in run_config_widget_state(config).items():
        st.session_state[key] = value


def _seed_run_config_widgets_if_needed(seed: RunConfig, *, force: bool = False) -> None:
    if not (force or not st.session_state.get(RUN_CONFIG_WIDGETS_SEEDED_KEY)):
        return
    preserve_replay = bool(st.session_state.get("run_config_replay_mode"))
    state = run_config_widget_state(seed)
    if preserve_replay:
        state.pop("run_config_replay_mode", None)
        state.pop("run_config_replay_run_id", None)
    for key, value in state.items():
        st.session_state[key] = value
    if preserve_replay:
        _ensure_default_replay_run_id()
    st.session_state[RUN_CONFIG_WIDGETS_SEEDED_KEY] = True


def _ensure_default_replay_run_id() -> None:
    """Pick first archive when replay is on but run_id missing — call before replay widgets."""
    from src.run import list_archives

    archives = list_archives()
    if not archives:
        return
    valid_ids = {str(row.get("run_id") or "") for row in archives}
    current = str(st.session_state.get("run_config_replay_run_id") or "")
    if current not in valid_ids:
        st.session_state["run_config_replay_run_id"] = archives[0]["run_id"]


def _set_all_agent_llm_widgets(select: bool) -> None:
    st.session_state["run_config_stage_analysts"] = select
    for key, _, _ in _PIPELINE_STAGE_WIDGETS:
        st.session_state[key] = select
    for key, _, _ in _ANALYST_LLM_WIDGETS:
        st.session_state[key] = select


def _analyst_checkbox_state() -> tuple[str, int]:
    checked = [stage for key, stage, _ in _ANALYST_LLM_WIDGETS if st.session_state.get(key, True)]
    n = len(checked)
    if n in (0, 4):
        return "", n
    if n == 1:
        return checked[0], 1
    return "__multi__", n


_MODE_SYNC_KEY = "_run_config_applied_mode"
_CORE_STAGE_WIDGET_KEYS = (
    "run_config_stage_analysts",
    "run_config_stage_bullish",
    "run_config_stage_bearish",
    "run_config_stage_debate",
    "run_config_stage_levels",
)


def _sync_stage_widgets_from_mode_preset() -> None:
    """When advanced controls open, align stage/analyst widgets with the mode preset."""
    mode_label = st.session_state.get("run_config_mode_label", "规则引擎")
    mode = _MODE_LABEL_TO_VALUE.get(mode_label, "rule")
    if mode == "rule":
        return
    narrative = bool(st.session_state.get("run_config_llm_narrative", True))
    preset = run_config_for_mode(mode, llm_enabled=narrative)  # type: ignore[arg-type]
    for key, value in run_config_widget_state(preset).items():
        if key.startswith(("run_config_stage_", "run_config_llm_")):
            st.session_state[key] = value


def _on_advanced_toggle() -> None:
    if st.session_state.get("run_config_advanced"):
        _sync_stage_widgets_from_mode_preset()


def _apply_mode_preset_to_widgets(mode: str) -> None:
    """When mode radio changes, re-seed LLM stage widgets from the mode preset."""
    preserve_replay = bool(st.session_state.get("run_config_replay_mode"))
    narrative = bool(st.session_state.get("run_config_llm_narrative", True))
    preset = run_config_for_mode(mode, llm_enabled=narrative)  # type: ignore[arg-type]
    skip = {"run_config_mode_label", "run_config_replay_mode", "run_config_replay_run_id"}
    if preserve_replay:
        skip |= {"run_config_replay_mode", "run_config_replay_run_id"}
    for key, value in run_config_widget_state(preset).items():
        if key in skip:
            continue
        st.session_state[key] = value


def _advanced_core_stages_all_off() -> bool:
    return not any(st.session_state.get(key, False) for key in _CORE_STAGE_WIDGET_KEYS)


def selected_run_config() -> RunConfig:
    if st.session_state.get("run_config_replay_mode") and st.session_state.get("run_config_replay_run_id"):
        return RunConfig(
            replay_mode=True,
            replay_run_id=str(st.session_state["run_config_replay_run_id"]),
        ).normalized()

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

    narrative = bool(st.session_state.get("run_config_llm_narrative", True))
    preset = run_config_for_mode(mode, llm_enabled=narrative)  # type: ignore[arg-type]
    if mode != "rule" and _advanced_core_stages_all_off():
        analyst_only, _ = _analyst_checkbox_state()
        return RunConfig(
            agent_mode=mode,  # type: ignore[arg-type]
            llm_enabled=narrative,
            llm_stage_analysts=preset.llm_stage_analysts,
            llm_stage_bullish=preset.llm_stage_bullish,
            llm_stage_bearish=preset.llm_stage_bearish,
            llm_stage_debate=preset.llm_stage_debate,
            llm_stage_levels=preset.llm_stage_levels,
            llm_stage_trader=preset.llm_stage_trader,
            llm_stage_risk=preset.llm_stage_risk,
            llm_stage_manager=preset.llm_stage_manager,
            llm_analyst_only="" if analyst_only == "__multi__" else analyst_only,
            replay_mode=bool(st.session_state.get("run_config_replay_mode", False)),
            replay_run_id=str(st.session_state.get("run_config_replay_run_id") or "").strip(),
        ).normalized()

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
        replay_mode=bool(st.session_state.get("run_config_replay_mode", False)),
        replay_run_id=str(st.session_state.get("run_config_replay_run_id") or "").strip(),
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


def _on_open_replay_config() -> None:
    """Sidebar — jump to config panel with replay mode pre-selected."""
    st.session_state[FORCE_REFRESH_KEY] = True
    st.session_state[RUN_CONFIG_READY_KEY] = False
    st.session_state[RUN_CONFIG_REFRESH_UI_KEY] = True
    st.session_state.pop(RUN_CONFIG_KEY, None)
    st.session_state.pop(RUN_CONFIG_WIDGETS_SEEDED_KEY, None)
    st.session_state["run_config_replay_mode"] = True


def render_sidebar_replay() -> None:
    """Always visible in sidebar — entry point for historical replay."""
    from src.run import list_archives

    st.sidebar.markdown("---")
    st.sidebar.markdown("**历史回放**")
    archives = list_archives(limit=1)
    if not archives:
        st.sidebar.caption(
            "暂无记录。先完成一次「开始生成报告」，结果会保存到 `.cache/run_archives/`。"
        )
        return
    count = len(list_archives(limit=500))
    st.sidebar.caption(f"已保存 {count} 条 · 0 token · 不重跑 LLM")
    st.sidebar.button(
        "选择历史记录并回放…",
        on_click=_on_open_replay_config,
        key="sidebar_open_replay_config",
    )


def _render_replay_controls() -> None:
    from src.run import archive_label, list_archives

    archives = list_archives()
    st.markdown("#### 历史回放")
    if not archives:
        st.info(
            "暂无历史记录。请先点击下方 **「开始生成报告」** 完成一次生成；"
            "成功后报告会自动保存，届时可勾选回放模式 **0 token** 查看，无需重新调用 LLM。"
        )
        return

    if st.session_state.get("run_config_replay_mode"):
        _ensure_default_replay_run_id()

    st.checkbox(
        "回放模式（0 token · 不重跑 LLM · 即时加载已保存报告）",
        key="run_config_replay_mode",
        help="不拉数据、不调用 LLM，即时加载所选历史记录中的完整报告与文案。",
    )
    if st.session_state.get("run_config_replay_mode"):
        options = {meta["run_id"]: archive_label(meta) for meta in archives}
        run_ids = list(options.keys())
        st.selectbox(
            "选择历史记录",
            options=run_ids,
            format_func=lambda rid: options.get(rid, rid),
            key="run_config_replay_run_id",
        )
        selected_id = str(st.session_state.get("run_config_replay_run_id") or "")
        selected = next((row for row in archives if row.get("run_id") == selected_id), None)
        if selected and not selected.get("replayable", True):
            st.warning(
                "所选记录为中断/失败快照，将加载**问题现场**（步骤、I/O、配置），"
                "完整报告页可能不完整；请优先查看「LLM 决策链」。"
            )
        else:
            st.info("回放展示当时的完整报告（流水线已全部跑完），不会重新拉数或调用 LLM。")
        st.caption(f"共 {len(archives)} 条 · `.cache/run_archives/` · 可导出 zip 移植到其他机器")
        _render_archive_transfer_controls(selected_id)
    else:
        st.caption(f"已有 {len(archives)} 条历史记录可选（0 token 回放）。")
        _render_archive_import_only()


def _render_archive_import_only() -> None:
    uploaded = st.file_uploader(
        "导入历史 zip 包（移植报告）",
        type=["zip"],
        key="run_config_import_archive_zip_idle",
        help="从其他机器导出的 `.cache/run_archives/<run_id>/` zip 包。",
    )
    if uploaded is not None and st.button("导入 zip 到本地归档", key="run_config_import_archive_btn_idle"):
        from src.run.archive.transfer import import_archive_zip

        try:
            run_id = import_archive_zip(uploaded.getvalue())
            st.success(f"已导入 `{run_id}`，可勾选回放模式查看。")
            st.rerun()
        except Exception as exc:
            st.error(str(exc))


def _render_archive_transfer_controls(selected_id: str) -> None:
    from src.run.archive.transfer import export_archive_zip, import_archive_zip

    exp_col, imp_col = st.columns(2)
    with exp_col:
        if selected_id:
            try:
                payload = export_archive_zip(selected_id)
                st.download_button(
                    "导出所选 zip 包",
                    data=payload,
                    file_name=f"{selected_id}.zip",
                    mime="application/zip",
                    key=f"run_config_export_{selected_id}",
                )
            except FileNotFoundError:
                st.caption("导出不可用：归档目录缺失")
        else:
            st.caption("选择记录后可导出 zip")
    with imp_col:
        uploaded = st.file_uploader(
            "导入 zip 包",
            type=["zip"],
            key="run_config_import_archive_zip",
            label_visibility="collapsed",
        )
        if uploaded is not None and st.button("导入 zip", key="run_config_import_archive_btn"):
            try:
                run_id = import_archive_zip(uploaded.getvalue())
                st.session_state["run_config_replay_run_id"] = run_id
                st.success(f"已导入 `{run_id}`")
                st.rerun()
            except Exception as exc:
                st.error(str(exc))


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


def render_run_config_panel() -> None:
    from src.llm.router import llm_configured

    seed = default_panel_run_config()
    is_refresh = bool(st.session_state.pop(RUN_CONFIG_REFRESH_UI_KEY, False))
    _seed_run_config_widgets_if_needed(seed, force=is_refresh)
    hero_title = "重新生成配置" if is_refresh else "生成前配置"
    hero_sub = (
        "默认选择规则引擎，可调整后点击「开始生成报告」"
        if is_refresh
        else "默认选择规则引擎模式，可调整后点击「开始生成报告」"
    )
    render_page_hero(hero_title, hero_sub)

    _render_replay_controls()
    st.markdown("#### 运行模式")
    _render_run_mode_guide()
    replay_active = bool(st.session_state.get("run_config_replay_mode"))
    mode_label = st.radio(
        "选择本次报告使用的智能体模式",
        list(_MODE_LABEL_TO_VALUE),
        horizontal=True,
        key="run_config_mode_label",
        disabled=replay_active,
    )
    mode = _MODE_LABEL_TO_VALUE.get(mode_label, "rule")
    if st.session_state.get(_MODE_SYNC_KEY) != mode_label:
        _apply_mode_preset_to_widgets(mode)
        st.session_state[_MODE_SYNC_KEY] = mode_label
    needs_llm = mode != "rule" and not replay_active
    llm_ready = llm_configured()

    if replay_active:
        st.info("当前为回放模式：将直接加载历史报告（0 token · 不重跑 LLM）。")
    elif mode == "rule":
        st.info("规则引擎模式不会调用 LLM，适合快速生成与排查数据/指标问题。")
    elif mode == "llm":
        st.info("LLM 智能体模式会启用分析师团队、看多/看空研究、辩论与可选报告文案。")
    else:
        st.info("混合模式会先跑规则基线，LLM 置信度达标时覆盖对应阶段。")

    if needs_llm and not llm_ready:
        st.warning("当前未配置 `LLM_API_KEY`，请先配置密钥，或选择规则引擎模式。")

    st.checkbox(
        "启用 LLM 报告文案",
        disabled=not needs_llm or replay_active,
        key="run_config_llm_narrative",
        help="这是流水线末尾的报告叙述层，独立于智能体链。规则模式下固定关闭。",
    )

    st.checkbox(
        "高级调试",
        disabled=not needs_llm or replay_active,
        key="run_config_advanced",
        on_change=_on_advanced_toggle,
        help="勾选后可分阶段、分 Analyst 控制 LLM 调用范围。",
    )

    if needs_llm and st.session_state.get("run_config_advanced") and not replay_active:
        with st.expander("高级调试：阶段与 Analyst 控制", expanded=False):
            _render_run_config_advanced_controls()

    config = selected_run_config()
    st.caption(f"预填配置指纹: `{seed.fingerprint()}` · 本次配置指纹: `{config.fingerprint()}`")

    _analyst_only, _ = _analyst_checkbox_state()
    analyst_invalid = (
        needs_llm
        and st.session_state.get("run_config_advanced")
        and _analyst_only == "__multi__"
    )
    replay_invalid = replay_active and not str(st.session_state.get("run_config_replay_run_id") or "").strip()
    start_disabled = ((needs_llm and not llm_ready) and not replay_active) or analyst_invalid or replay_invalid
    start_label = "开始生成报告"
    if replay_active:
        from src.run import inspect_run_archive

        rid = str(st.session_state.get("run_config_replay_run_id") or "").strip()
        if rid:
            try:
                replayable = inspect_run_archive(rid).replayable
            except Exception:
                replayable = True
            start_label = "加载历史回放" if replayable else "加载问题现场"
        else:
            start_label = "加载历史回放"
    if st.button(start_label, type="primary", disabled=start_disabled):
        st.session_state[RUN_CONFIG_KEY] = config
        st.session_state[RUN_CONFIG_READY_KEY] = True
        st.session_state.pop(RUN_CONFIG_WIDGETS_SEEDED_KEY, None)
        invalidate_report_cache()
        log.info("user started report generation config=%s", config.to_dict())
        st.rerun()

    st.stop()
