"""LLM narrative panel."""

from __future__ import annotations

import streamlit as st

from src.config import LLM_ENABLED


def render_llm_panel(report: dict) -> None:
    llm = report.get("llm_analysis")
    if not llm:
        if LLM_ENABLED:
            st.caption("LLM 已启用，但本次未生成分析结果")
        else:
            st.caption("LLM 未启用。在 `.env` 中设置 `LLM_ENABLED=true` 并配置 API Key")
        return

    if not llm.get("enabled"):
        st.caption(llm.get("error") or "LLM 未启用")
        return

    if llm.get("error"):
        st.error(f"LLM 调用失败：{llm['error']}")
        return

    meta = report.get("meta") or {}
    execution_authorized = bool(meta.get("execution_authorized"))
    observation_mode = bool(meta.get("observation_mode"))
    top_audit = (meta.get("stage_sources") or {}).get("narrative_top_level") or {}
    action_plan = str(llm.get("action_plan") or "").strip()

    model = llm.get("model") or ""
    reliability = (report.get("meta") or {}).get("report_reliability") or {}
    overall = reliability.get("overall_reliability")
    if overall is not None:
        st.caption(
            f"模型 `{model}` · 报告质量分 {overall:.0%}（启发式，非胜率）"
            f"；模型自报 {llm.get('confidence', 0):.0%}"
        )
    else:
        st.caption(f"模型 `{model}` · 模型自报置信 {llm.get('confidence', 0):.0%}（非胜率）")

    if not execution_authorized or observation_mode:
        st.info("经理未授权执行：以下内容仅为市场观察，不含可执行交易指令。")

    if llm.get("market_summary"):
        st.markdown("**市场总览**")
        st.write(llm["market_summary"])

    if llm.get("trade_thesis"):
        st.markdown("**交易逻辑**")
        st.write(llm["trade_thesis"])

    if action_plan and execution_authorized and not observation_mode:
        st.markdown("**操作建议**")
        for line in action_plan.split("\n"):
            line = line.strip()
            if line:
                st.markdown(f"- {line}")
    elif action_plan and not top_audit.get("accepted", True):
        st.caption("操作建议已因未授权执行或含可执行措辞而被系统抑制。")

    col_a, col_b = st.columns(2)
    with col_a:
        if llm.get("watch_levels"):
            label = "**观察价位**" if not execution_authorized else "**关注价位**"
            st.markdown(label)
            for level in llm["watch_levels"]:
                st.markdown(f"- {level}")
    with col_b:
        if llm.get("risks"):
            st.markdown("**风险提示**")
            for risk in llm["risks"]:
                st.markdown(f"- {risk}")


def render_llm_sidebar(report: dict) -> None:
    render_llm_panel(report)
