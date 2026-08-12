"""Advice V2 LLM thinking process page — pipeline steps and I/O audit."""

from __future__ import annotations

import json

import streamlit as st

from src.viz.pipeline_progress import render_llm_io_history, render_progress_steps
from src.viz.streamlit_common import render_page_hero


def _meta(report: dict) -> dict:
    return report.get("meta") or {}


def _llm_records(meta: dict) -> list[dict]:
    return list(meta.get("llm_io") or [])


def _rule_stage_records(records: list[dict]) -> list[dict]:
    return [row for row in records if row.get("kind") == "rule" or row.get("model") == "规则引擎"]


def _llm_stage_records(records: list[dict]) -> list[dict]:
    return [row for row in records if row.get("kind") != "rule" and row.get("model") != "规则引擎"]


def _render_advisor_trace(trace: dict | None) -> None:
    if not trace:
        st.caption("未调用 LLM 解释增强，或调用未产生审计记录。")
        return
    cols = st.columns(4)
    cols[0].metric("阶段", trace.get("stage") or "advisor")
    cols[1].metric("模型", trace.get("model") or "—")
    cols[2].metric("耗时", f"{int(trace.get('latency_ms') or 0)} ms")
    cols[3].metric("尝试次数", int(trace.get("attempts") or 0))
    if trace.get("error"):
        st.error(str(trace["error"]))
    if trace.get("budget_action") and trace.get("budget_action") != "none":
        st.warning(f"输入预算动作：{trace['budget_action']}")
    usage = trace.get("usage")
    if isinstance(usage, dict) and usage:
        st.json(usage)
    attempt_log = trace.get("attempt_log") or []
    if attempt_log:
        with st.expander("重试与降级记录", expanded=False):
            st.json(attempt_log)


def render_llm_process_page(report: dict) -> None:
    """Show Advice V2 generation steps and LLM/rule I/O from report meta."""
    meta = _meta(report)
    advice = report.get("advice") or {}
    advice_source = str(meta.get("advice_source") or "rule")
    records = _llm_records(meta)

    render_page_hero(
        "LLM 思考过程",
        "查看本次生成的流水线步骤、确定性建议输入/输出，以及可选的 LLM 文案增强 Prompt 与响应",
    )

    if advice_source == "llm_explanation":
        st.success(
            f"本次主建议使用 **LLM 解释增强**（决策 {advice.get('decision', '—')}）。"
            "模型只能修改文字字段，方向与数值仍由确定性引擎约束。"
        )
    elif meta.get("advisor_trace", {}).get("error"):
        st.warning("LLM 解释增强失败，已回退到确定性文案。详见下方「审计与追踪」。")
    else:
        st.info(
            "本次为 **确定性建议**。"
            "若需查看 LLM Prompt/响应，请在生成配置中选择「LLM 解释增强」后重新生成。"
        )

    tab_steps, tab_llm, tab_rule, tab_audit = st.tabs(
        ["生成步骤", "LLM 调用", "确定性建议 I/O", "审计与追踪"]
    )

    with tab_steps:
        steps = meta.get("generation_steps") or []
        if steps:
            render_progress_steps(steps, title="流水线阶段")
        else:
            st.caption("暂无步骤记录。请重新生成报告，或使用含完整 meta 的历史归档。")

    with tab_llm:
        llm_rows = _llm_stage_records(records)
        if llm_rows:
            render_llm_io_history(
                llm_rows,
                title="LLM 解释增强（advisor）",
                expand_last=True,
            )
        else:
            st.caption("暂无 LLM 调用记录。")

    with tab_rule:
        rule_rows = _rule_stage_records(records)
        if rule_rows:
            render_llm_io_history(
                rule_rows,
                title="确定性建议引擎（规则输入 → 建议输出）",
                expand_last=True,
            )
        else:
            st.caption("暂无规则阶段 I/O。归档过旧或生成中断时可能缺失。")

    with tab_audit:
        st.markdown("#### 建议来源")
        st.code(
            json.dumps(
                {
                    "advice_source": advice_source,
                    "decision": advice.get("decision"),
                    "confidence": advice.get("confidence"),
                    "run_config_fingerprint": meta.get("run_config_fingerprint"),
                },
                ensure_ascii=False,
                indent=2,
            ),
            language="json",
        )
        st.markdown("#### LLM 阶段追踪（advisor_trace）")
        _render_advisor_trace(meta.get("advisor_trace"))
        routing = meta.get("llm_routing")
        if routing:
            with st.expander("LLM 路由策略", expanded=False):
                st.json(routing)
