"""Agent decision chain panel (main content area)."""

from __future__ import annotations

import json

import streamlit as st

from src.viz.llm_meta import format_latency_ms, stage_llm_caption
from src.viz.source_labels import STAGE_LABELS, source_label


def _badge_md(source: str | None) -> str:
    label = source_label(source)
    if source in ("llm", "hybrid"):
        return f":violet-badge[{label}]"
    return f":gray-badge[{label}]"


def render_agent_trace_panel(report: dict) -> None:
    trace = report.get("agent_trace")
    if not trace:
        st.caption("暂无 agent_trace 数据")
        return

    stage_meta = trace.get("stage_meta") or {}
    decision = trace.get("decision", {})
    debate = trace.get("debate", {})
    proposal = trace.get("proposal", {})
    risk_reviews = trace.get("risk_reviews", [])

    c1, c2, c3 = st.columns(3)
    mgr_src = (stage_meta.get("manager") or {}).get("source", "rule")
    with c1:
        st.metric("经理决策", decision.get("action", "—"))
        st.caption(f"{_badge_md(mgr_src)} · 置信 {decision.get('confidence', 0):.0%}")
    debate_src = (stage_meta.get("debate") or {}).get("source", "rule")
    with c2:
        st.metric("辩论共识", debate.get("consensus_bias", "—"))
        st.caption(f"{_badge_md(debate_src)} · 强度 {debate.get('consensus_strength', 0):.0%}")
    trader_src = (stage_meta.get("trader") or {}).get("source", "rule")
    with c3:
        st.metric("交易员", proposal.get("primary_direction", "—"))
        st.caption(f"{_badge_md(trader_src)} · 信号 {proposal.get('signal_indices', [])}")

    st.markdown("**经理摘要**")
    st.write(decision.get("summary", "—"))

    st.markdown("**辩论要点**")
    for note in debate.get("discussion_notes", [])[:6]:
        st.markdown(f"- {note}")

    bull = debate.get("bullish", {})
    bear = debate.get("bearish", {})
    bull_src = (stage_meta.get("bullish") or {}).get("source", "rule")
    bear_src = (stage_meta.get("bearish") or {}).get("source", "rule")
    bull_llm = (stage_meta.get("bullish") or {}).get("llm") or {}
    bear_llm = (stage_meta.get("bearish") or {}).get("llm") or {}
    r1, r2 = st.columns(2)
    with r1:
        st.markdown(f"**看多研究** {_badge_md(bull_src)}")
        if bull_llm:
            st.caption(stage_llm_caption(stage_meta, "bullish"))
        st.caption(bull.get("summary", "—"))
        st.caption(f"{len(bull.get('items', []))} 条证据")
    with r2:
        st.markdown(f"**看空研究** {_badge_md(bear_src)}")
        if bear_llm:
            st.caption(stage_llm_caption(stage_meta, "bearish"))
        st.caption(bear.get("summary", "—"))
        st.caption(f"{len(bear.get('items', []))} 条证据")

    if proposal.get("rationale"):
        st.markdown("**交易员理由**")
        for line in proposal.get("rationale", [])[:4]:
            st.markdown(f"- {line}")

    risk_src = (stage_meta.get("risk") or {}).get("source", "rule")
    st.markdown(f"**风控** {_badge_md(risk_src)}")
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
            use_container_width=True,
            hide_index=True,
        )

    if stage_meta:
        st.markdown("**阶段来源一览**")
        for name, meta in stage_meta.items():
            src = meta.get("source", "rule")
            label = STAGE_LABELS.get(name, name)
            extra = ""
            if meta.get("fallback_reason"):
                extra = f" · 回退：{meta['fallback_reason'][:60]}"
            llm = meta.get("llm") or {}
            if llm.get("model"):
                extra += f" · `{llm['model']}`"
            if llm.get("latency_ms"):
                extra += f" · {format_latency_ms(llm['latency_ms'])}"
            st.markdown(f"- **{label}** {_badge_md(src)}{extra}")

    llm = report.get("llm_analysis") or {}
    if llm.get("enabled") and not llm.get("error"):
        st.markdown(f"**报告文案层** {_badge_md('llm')}")

    with st.expander("完整 agent_trace JSON", expanded=False):
        st.code(json.dumps(trace, ensure_ascii=False, indent=2), language="json")


def render_agent_trace_sidebar(report: dict) -> None:
    """Legacy sidebar entry — delegates to panel."""
    render_agent_trace_panel(report)
