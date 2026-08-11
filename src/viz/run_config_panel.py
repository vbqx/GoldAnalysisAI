"""Advice V2 generation and replay controls."""

from __future__ import annotations

import streamlit as st

from src.core.run_config import RunConfig, default_panel_run_config, run_config_widget_state
from src.viz.page_layout import render_page_hero
from src.viz.session_keys import (
    FORCE_REFRESH_KEY,
    RUN_CONFIG_KEY,
    RUN_CONFIG_READY_KEY,
    RUN_CONFIG_REFRESH_UI_KEY,
    RUN_CONFIG_WIDGETS_SEEDED_KEY,
)

_LABEL_TO_MODE = {"确定性建议": "rule", "LLM 解释增强": "llm"}
_MODE_TO_LABEL = {value: key for key, value in _LABEL_TO_MODE.items()}


def mode_label_to_value(label: str) -> str:
    return _LABEL_TO_MODE.get(label, "rule")


def mode_value_to_label(value: str) -> str:
    return _MODE_TO_LABEL.get(value, "确定性建议")


def _seed() -> None:
    if st.session_state.get(RUN_CONFIG_WIDGETS_SEEDED_KEY):
        return
    replay_requested = bool(st.session_state.get("run_config_replay_mode"))
    replay_run_id = str(st.session_state.get("run_config_replay_run_id") or "")
    for key, value in run_config_widget_state(default_panel_run_config()).items():
        st.session_state[key] = value
    if replay_requested:
        st.session_state["run_config_replay_mode"] = True
        st.session_state["run_config_replay_run_id"] = replay_run_id
    st.session_state[RUN_CONFIG_WIDGETS_SEEDED_KEY] = True


def _ensure_default_replay_run_id() -> None:
    from src.run import list_archives

    archives = list_archives()
    if not archives:
        return
    valid = {str(row.get("run_id") or "") for row in archives}
    current = str(st.session_state.get("run_config_replay_run_id") or "")
    if current not in valid:
        st.session_state["run_config_replay_run_id"] = archives[0]["run_id"]


def selected_run_config() -> RunConfig:
    if st.session_state.get("run_config_replay_mode"):
        run_id = str(st.session_state.get("run_config_replay_run_id") or "").strip()
        if run_id:
            return RunConfig(replay_mode=True, replay_run_id=run_id).normalized()
    mode = mode_label_to_value(str(st.session_state.get("run_config_mode_label") or "确定性建议"))
    return RunConfig(generation_mode=mode, llm_enabled=mode == "llm").normalized()  # type: ignore[arg-type]


def _on_open_replay_config() -> None:
    st.session_state[FORCE_REFRESH_KEY] = True
    st.session_state[RUN_CONFIG_READY_KEY] = False
    st.session_state[RUN_CONFIG_REFRESH_UI_KEY] = True
    st.session_state.pop(RUN_CONFIG_KEY, None)
    st.session_state.pop(RUN_CONFIG_WIDGETS_SEEDED_KEY, None)
    st.session_state["run_config_replay_mode"] = True


def render_sidebar_replay() -> None:
    from src.run import list_archives

    st.sidebar.markdown("---")
    st.sidebar.markdown("**历史回放**")
    archives = list_archives(limit=500)
    if not archives:
        st.sidebar.caption("暂无建议归档")
        return
    st.sidebar.caption(f"已保存 {len(archives)} 条")
    st.sidebar.button("选择历史记录…", on_click=_on_open_replay_config, key="sidebar_open_replay_config")


def _render_replay_controls() -> None:
    from src.run import archive_label, list_archives

    archives = list_archives()
    st.checkbox("回放历史建议（不重新拉取数据）", key="run_config_replay_mode")
    if not st.session_state.get("run_config_replay_mode"):
        return
    if not archives:
        st.info("暂无历史记录。")
        return
    _ensure_default_replay_run_id()
    labels = {row["run_id"]: archive_label(row) for row in archives}
    st.selectbox(
        "选择历史记录",
        options=list(labels),
        format_func=lambda run_id: labels.get(run_id, run_id),
        key="run_config_replay_run_id",
    )


def render_run_config_panel() -> None:
    _seed()
    render_page_hero("生成一份人工审核建议", "系统只提出建议，不执行交易；每次最多一个首选方案。")
    st.radio(
        "生成方式",
        options=list(_LABEL_TO_MODE),
        horizontal=True,
        key="run_config_mode_label",
    )
    mode = mode_label_to_value(str(st.session_state.get("run_config_mode_label")))
    if mode == "llm":
        st.caption("确定性引擎固定方向和全部数值，LLM 只改善中文解释；校验失败时自动使用确定性文案。")
    else:
        st.caption("完全由可复现规则生成，速度快，适合检查事实和建议契约。")
    _render_replay_controls()
    if st.button("开始生成建议", type="primary", use_container_width=True):
        st.session_state[RUN_CONFIG_KEY] = selected_run_config()
        st.session_state[RUN_CONFIG_READY_KEY] = True
        st.rerun()
    st.stop()
