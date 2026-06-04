"""Sidebar debug panel for agent decision chain."""

from __future__ import annotations

import json

import streamlit as st


def render_agent_trace_sidebar(report: dict) -> None:
    trace = report.get("agent_trace")
    if not trace:
        st.caption("暂无 agent_trace 数据")
        return

    decision = trace.get("decision", {})
    debate = trace.get("debate", {})
    proposal = trace.get("proposal", {})
    risk_reviews = trace.get("risk_reviews", [])

    st.markdown(
        f"**经理决策** · `{decision.get('action', '—')}` "
        f"· 置信度 {decision.get('confidence', 0):.0%}"
    )
    st.caption(decision.get("summary", "—"))

    st.markdown(
        f"**辩论共识** · `{debate.get('consensus_bias', '—')}` "
        f"· 强度 {debate.get('consensus_strength', 0):.0%}"
    )
    for note in debate.get("discussion_notes", [])[:4]:
        st.markdown(f"- {note}")

    bull = debate.get("bullish", {})
    bear = debate.get("bearish", {})
    st.markdown(
        f"**研究员** · 多 {len(bull.get('items', []))} 条 / "
        f"空 {len(bear.get('items', []))} 条"
    )
    st.caption(f"多：{bull.get('summary', '—')}")
    st.caption(f"空：{bear.get('summary', '—')}")

    st.markdown(
        f"**交易员** · `{proposal.get('primary_direction', '—')}` "
        f"· 信号 {proposal.get('signal_indices', [])}"
    )
    for line in proposal.get("rationale", [])[:3]:
        st.markdown(f"- {line}")

    if risk_reviews:
        rows = [
            {
                "风格": r.get("profile", "—"),
                "通过": "✓" if r.get("approved") else "✗",
                "仓位": f"{r.get('position_scale', 0):.0%}",
                "信号": str(r.get("allowed_signal_indices", [])),
            }
            for r in risk_reviews
        ]
        st.table(rows)

    with st.expander("完整 JSON", expanded=False):
        st.code(json.dumps(trace, ensure_ascii=False, indent=2), language="json")
