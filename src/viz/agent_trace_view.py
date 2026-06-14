"""Agent decision chain panel (main content area)."""

from __future__ import annotations

import json

import streamlit as st

from src.viz.llm_meta import format_latency_ms, stage_llm_caption
from src.viz.source_labels import STAGE_LABELS, llm_was_invoked, stage_meta_label


def _badge_md(meta: dict) -> str:
    label = stage_meta_label(meta)
    if llm_was_invoked(meta):
        return f":violet-badge[{label}]"
    return f":gray-badge[{label}]"


def render_agent_trace_panel(report: dict) -> None:
    trace = report.get("agent_trace")
    if not trace:
        st.caption("暂无 agent_trace 数据")
        return

    stage_meta = trace.get("stage_meta") or {}
    analyst_team = trace.get("analyst_team") or {}
    decision = trace.get("decision", {})
    debate = trace.get("debate", {})
    proposal = trace.get("proposal", {})
    risk_reviews = trace.get("risk_reviews", [])

    c1, c2, c3 = st.columns(3)
    mgr_meta = stage_meta.get("manager") or {}
    with c1:
        st.metric("经理决策", decision.get("action", "—"))
        st.caption(f"{_badge_md(mgr_meta)} · 置信 {decision.get('confidence', 0):.0%}")
    debate_meta = stage_meta.get("debate") or {}
    with c2:
        st.metric("辩论共识", debate.get("consensus_bias", "—"))
        st.caption(f"{_badge_md(debate_meta)} · 强度 {debate.get('consensus_strength', 0):.0%}")
    trader_meta = stage_meta.get("trader") or {}
    with c3:
        st.metric("交易员", proposal.get("primary_direction", "—"))
        st.caption(f"{_badge_md(trader_meta)} · 信号 {proposal.get('signal_indices', [])}")

    st.markdown("**经理摘要**")
    st.write(decision.get("summary", "—"))

    if analyst_team:
        team_meta = stage_meta.get("analyst_team") or {}
        st.markdown(f"**Analyst Team** {_badge_md(team_meta)}")
        cols = st.columns(4)
        labels = {
            "technical": "技术",
            "fundamentals": "基本面",
            "news": "新闻",
            "sentiment": "情绪",
        }
        for col, (key, title) in zip(cols, labels.items()):
            report = analyst_team.get(key) or {}
            with col:
                st.markdown(f"**{title}**")
                st.caption(report.get("bias", "—"))
                st.caption(report.get("summary", "—")[:120])
                st.caption(f"{len(report.get('items', []))} 条证据")

    st.markdown("**辩论要点**")
    for note in debate.get("discussion_notes", [])[:6]:
        st.markdown(f"- {note}")

    bull = debate.get("bullish", {})
    bear = debate.get("bearish", {})
    bull_meta = stage_meta.get("bullish") or {}
    bear_meta = stage_meta.get("bearish") or {}
    r1, r2 = st.columns(2)
    with r1:
        st.markdown(f"**看多研究** {_badge_md(bull_meta)}")
        if bull_meta.get("llm"):
            st.caption(stage_llm_caption(stage_meta, "bullish"))
        st.caption(bull.get("summary", "—"))
        st.caption(f"{len(bull.get('items', []))} 条证据")
    with r2:
        st.markdown(f"**看空研究** {_badge_md(bear_meta)}")
        if bear_meta.get("llm"):
            st.caption(stage_llm_caption(stage_meta, "bearish"))
        st.caption(bear.get("summary", "—"))
        st.caption(f"{len(bear.get('items', []))} 条证据")

    if proposal.get("rationale"):
        st.markdown("**交易员理由**")
        for line in proposal.get("rationale", [])[:4]:
            st.markdown(f"- {line}")

    risk_meta = stage_meta.get("risk") or {}
    st.markdown(f"**风控** {_badge_md(risk_meta)}")
    if risk_reviews:
        st.dataframe(
            [
                {
                    "风格": r.get("profile", "—"),
                    "通过": "✓" if r.get("approved") else "✗",
                    "仓位": f"{r.get('position_scale', 0):.0%}",
                    "信号": str(r.get("allowed_signal_indices", [])),
                }
                for r in risk_reviews
            ],
            # Fix #6 [Improvement] Streamlit use_container_width 弃用警告
            # 原因：use_container_width 将于 2025-12-31 移除，改用 width="stretch"。
            width="stretch",
            hide_index=True,
        )

    if stage_meta:
        st.markdown("**阶段来源一览**")
        for name, meta in stage_meta.items():
            label = STAGE_LABELS.get(name, name)
            extra = ""
            if meta.get("fallback_reason"):
                extra = f" · {meta['fallback_reason'][:80]}"
            llm = meta.get("llm") or {}
            if llm.get("model"):
                extra += f" · `{llm['model']}`"
            if llm.get("latency_ms"):
                extra += f" · {format_latency_ms(llm['latency_ms'])}"
            st.markdown(f"- **{label}** {_badge_md(meta)}{extra}")

    llm = report.get("llm_analysis") or {}
    if llm.get("enabled") and not llm.get("error"):
        st.markdown(f"**报告文案层** {_badge_md('llm')}")

    with st.expander("完整 agent_trace JSON", expanded=False):
        st.code(json.dumps(trace, ensure_ascii=False, indent=2), language="json")


def render_agent_trace_sidebar(report: dict) -> None:
    """Legacy sidebar entry — delegates to panel."""
    render_agent_trace_panel(report)
