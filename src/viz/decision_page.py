"""Full-page LLM decision chain + I/O history."""

from __future__ import annotations

import streamlit as st

from src.viz.agent_trace_view import render_agent_trace_panel
from src.viz.llm_view import render_llm_panel
from src.viz.llm_meta import merge_llm_io_with_stage_sources
from src.viz.pipeline_progress import render_llm_io_history, render_progress_steps
from src.viz.source_labels import render_agent_source_banner
from src.viz.streamlit_common import render_page_hero


def render_live_generation_panel(live: dict) -> None:
    """Same tab layout as the decision page, fed by in-flight pipeline snapshots."""
    steps = live.get("steps") or []
    records = live.get("llm_io") or []

    tab_steps, tab_io, tab_trace, tab_llm = st.tabs(
        ["生成步骤", "LLM 输入/输出", "智能体决策", "LLM 文案"]
    )

    with tab_steps:
        if steps:
            render_progress_steps(steps, title="生成步骤")
        else:
            st.info("流水线启动中，即将显示各阶段进度…")

    with tab_io:
        if records:
            render_llm_io_history(records, title="LLM 调用记录", expand_last=True)
        else:
            st.info("数据拉取与规则分析完成后，将在此展示 LLM Prompt 与流式输出。")

    with tab_trace:
        st.info("智能体决策链将在多空研究、辩论阶段完成后自动出现。")

    with tab_llm:
        st.info("报告文案层将在流水线末尾生成。")


def render_llm_decision_page(report: dict) -> None:
    render_page_hero(
        "LLM 决策链",
        "智能体来源、辩论过程、报告文案与完整 Prompt / 响应记录",
    )
    st.markdown(render_agent_source_banner(report), unsafe_allow_html=True)

    tab_trace, tab_llm, tab_steps, tab_io = st.tabs(
        ["智能体决策", "LLM 文案", "生成步骤", "LLM 输入/输出"]
    )

    with tab_trace:
        render_agent_trace_panel(report)

    with tab_llm:
        render_llm_panel(report)

    with tab_steps:
        steps = report.get("meta", {}).get("generation_steps", [])
        if steps:
            render_progress_steps(steps, title="生成步骤")
        else:
            st.info("暂无生成步骤记录")

    with tab_io:
        records = report.get("meta", {}).get("llm_io", [])
        stage_sources = report.get("meta", {}).get("stage_sources", {})
        if not records:
            st.info("暂无 LLM 调用记录。请确认 `.env` 中已启用 `LLM_STAGE_*` 或 `LLM_ENABLED`。")
        else:
            render_llm_io_history(
                merge_llm_io_with_stage_sources(records, stage_sources),
                title="LLM 调用记录",
            )
