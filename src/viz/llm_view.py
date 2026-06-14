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

    model = llm.get("model") or ""
    st.caption(f"模型 `{model}` · 置信度 {llm.get('confidence', 0):.0%}")

    if llm.get("market_summary"):
        st.markdown("**市场总览**")
        st.write(llm["market_summary"])

    if llm.get("trade_thesis"):
        st.markdown("**交易逻辑**")
        st.write(llm["trade_thesis"])

    if llm.get("action_plan"):
        st.markdown("**操作建议**")
        for line in str(llm["action_plan"]).split("\n"):
            line = line.strip()
            if line:
                st.markdown(f"- {line}")

    col_a, col_b = st.columns(2)
    with col_a:
        if llm.get("watch_levels"):
            st.markdown("**关注价位**")
            for level in llm["watch_levels"]:
                st.markdown(f"- {level}")
    with col_b:
        if llm.get("risks"):
            st.markdown("**风险提示**")
            for risk in llm["risks"]:
                st.markdown(f"- {risk}")


def render_llm_sidebar(report: dict) -> None:
    render_llm_panel(report)
