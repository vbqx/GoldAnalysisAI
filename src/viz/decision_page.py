"""Full-page LLM decision chain + I/O history."""

from __future__ import annotations

import streamlit as st

from src.viz.agent_trace_view import render_agent_trace_panel
from src.viz.llm_view import render_llm_panel
from src.viz.llm_meta import merge_llm_io_with_stage_sources
from src.viz.pipeline_progress import (
    partition_llm_records_for_live,
    render_live_llm_streams,
    render_llm_io_history,
    render_progress_steps,
)
from src.viz.source_labels import render_agent_source_banner
from src.viz.streamlit_common import render_page_hero


def _render_generation_and_llm_io(
    *,
    steps: list[dict],
    records: list[dict],
    stage_sources: dict | None = None,
    expand_last: bool = False,
    empty_steps_msg: str = "暂无生成步骤记录",
    empty_io_msg: str = "暂无 LLM 调用记录",
    live_streaming: bool = False,
) -> None:
    """Single panel: pipeline steps on top, LLM I/O below."""
    if steps:
        render_progress_steps(steps, title="生成步骤")
    else:
        st.info(empty_steps_msg)

    st.divider()

    if records:
        merged = (
            merge_llm_io_with_stage_sources(records, stage_sources)
            if stage_sources
            else records
        )
        if live_streaming:
            active, completed = partition_llm_records_for_live(merged)
            if active:
                render_live_llm_streams(active)
                if completed:
                    st.divider()
            render_llm_io_history(
                completed,
                title="已完成 I/O" if active else "智能体 I/O（Analyst Team + LLM）",
                expand_last=expand_last and not active,
            )
        else:
            render_llm_io_history(
                merged,
                title="智能体 I/O（Analyst Team + LLM）",
                expand_last=expand_last,
            )
    else:
        st.info(empty_io_msg)


def render_live_generation_panel(live: dict) -> None:
    """Same tab layout as the decision page, fed by in-flight pipeline snapshots."""
    steps = live.get("steps") or []
    records = live.get("llm_io") or []

    tab_gen, tab_trace, tab_llm = st.tabs(
        ["生成与 LLM I/O", "智能体决策", "LLM 文案"]
    )

    with tab_gen:
        _render_generation_and_llm_io(
            steps=steps,
            records=records,
            expand_last=True,
            live_streaming=True,
            empty_steps_msg="流水线启动中，即将显示各阶段进度…",
            empty_io_msg="数据拉取与 Analyst Team 完成后，将在此展示各阶段输入/输出与 LLM 整理摘要。",
        )

    with tab_trace:
        st.info("Analyst Team 与智能体决策链将在四位分析师与多空辩论完成后自动出现。")

    with tab_llm:
        st.info("报告文案层将在流水线末尾生成。")


def render_llm_decision_page(report: dict) -> None:
    render_page_hero(
        "LLM 决策链",
        "智能体来源、辩论过程、报告文案与完整 Prompt / 响应记录",
    )
    st.markdown(render_agent_source_banner(report), unsafe_allow_html=True)

    tab_trace, tab_llm, tab_gen = st.tabs(
        ["智能体决策", "LLM 文案", "生成与 LLM I/O"]
    )

    with tab_trace:
        render_agent_trace_panel(report)

    with tab_llm:
        render_llm_panel(report)

    with tab_gen:
        meta = report.get("meta", {})
        _render_generation_and_llm_io(
            steps=meta.get("generation_steps", []),
            records=meta.get("llm_io", []),
            stage_sources=meta.get("stage_sources", {}),
            empty_io_msg="暂无智能体 I/O 记录。请确认已刷新报告；Analyst Team 为规则输出，LLM 需启用 `LLM_STAGE_*` 或 `LLM_ENABLED`。",
        )
