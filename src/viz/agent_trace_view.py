"""Agent decision chain panel (main content area)."""

from __future__ import annotations

import html
import json

import streamlit as st

from src.viz.display_labels import (
    label_action,
    label_bias,
    label_position_scale,
    label_risk_profile,
    label_trade_direction,
)
from src.viz.llm_meta import format_latency_ms, stage_llm_caption
from src.viz.source_labels import (
    STAGE_LABELS,
    llm_was_invoked,
    render_stage_meta_badge,
    stage_meta_label,
)


def _badge_md(meta: dict) -> str:
    label = stage_meta_label(meta)
    if llm_was_invoked(meta):
        return f":violet-badge[{label}]"
    return f":gray-badge[{label}]"


def _stage_source_text(stage_meta: dict, stage: str) -> str:
    meta = stage_meta.get(stage) or {}
    label = stage_meta_label(meta)
    if meta.get("fallback_reason"):
        return f"{label}（{meta['fallback_reason']}）"
    return label


def _short_text(value: object, limit: int = 72) -> str:
    text = str(value or "—").strip()
    if len(text) <= limit:
        return text
    return text[: limit - 1] + "…"


def _stage_card(stage: str, meta: dict, main: str, sub: str = "") -> str:
    cls = "llm" if llm_was_invoked(meta) else "rule"
    label = STAGE_LABELS.get(stage, stage)
    return (
        f'<div class="agent-stage-card {cls}">'
        f'<div class="stage-title"><b>{html.escape(label)}</b>{render_stage_meta_badge(meta, small=True)}</div>'
        f'<p class="stage-main">{html.escape(_short_text(main, 64))}</p>'
        f'<p class="stage-sub">{html.escape(_short_text(sub, 96))}</p>'
        "</div>"
    )


def _render_stage_summary_grid(report: dict, trace: dict) -> str:
    stage_meta = trace.get("stage_meta") or {}
    analyst_team = trace.get("analyst_team") or {}
    debate = trace.get("debate") or {}
    decision = trace.get("decision") or {}
    risk_reviews = trace.get("risk_reviews") or []
    levels = trace.get("llm_levels") or []
    validated = trace.get("validated_plans") or []
    signals = report.get("signals") or []

    analyst_biases = []
    for key in ("technical", "fundamentals", "news", "sentiment"):
        row = analyst_team.get(key) or {}
        if row:
            analyst_biases.append(f"{STAGE_LABELS.get(key, key)}={label_bias(row.get('bias', '—'))}")

    accepted = sum(1 for row in validated if row.get("accepted"))
    rejected = len(validated) - accepted
    approved_risk = sum(1 for row in risk_reviews if row.get("approved"))
    primary_signal = signals[0] if signals else {}

    cards = [
        _stage_card(
            "analyst_team",
            stage_meta.get("analyst_team") or {},
            " / ".join(analyst_biases) or "暂无分析师摘要",
            f"{len(analyst_team)} 个子模块",
        ),
        _stage_card(
            "debate",
            stage_meta.get("debate") or {},
            f"共识 {label_bias(debate.get('consensus_bias', '—'))}",
            f"强度 {float(debate.get('consensus_strength') or 0):.0%}",
        ),
        _stage_card(
            "llm_levels",
            stage_meta.get("llm_levels") or {},
            f"提议 {len(levels)} 条 / 通过 {accepted} 条",
            f"拒绝 {rejected} 条；主信号 {primary_signal.get('status', '—')}",
        ),
        _stage_card(
            "manager",
            stage_meta.get("manager") or {},
            f"{label_action(decision.get('action', '—'))} · {label_trade_direction(decision.get('primary_direction', '—'))}",
            f"置信 {float(decision.get('confidence') or 0):.0%}；风控通过 {approved_risk}/{len(risk_reviews)}",
        ),
    ]
    return f'<div class="agent-stage-summary">{"".join(cards)}</div>'


def _decision_flow_markdown(report: dict, trace: dict) -> str:
    meta = report.get("meta") or {}
    stage_meta = trace.get("stage_meta") or {}
    team = trace.get("analyst_team") or {}
    debate = trace.get("debate") or {}
    proposal = trace.get("proposal") or {}
    decision = trace.get("decision") or {}
    signals = report.get("signals") or []
    sentiment = report.get("sentiment") or {}
    metrics = report.get("metrics") or {}
    conclusion = report.get("conclusion") or {}
    levels = trace.get("llm_levels") or []
    validated = trace.get("validated_plans") or []

    analyst_bits = []
    for key, label in (
        ("technical", "技术"),
        ("fundamentals", "基本面"),
        ("news", "新闻"),
        ("sentiment", "情绪"),
    ):
        row = team.get(key) or {}
        analyst_bits.append(f"{label}={label_bias(row.get('bias', '—'))}")

    signal_bits = []
    for idx, sig in enumerate(signals[:3], start=1):
        signal_bits.append(
            f"{idx}. {sig.get('name', '信号')} {sig.get('direction', '')} "
            f"{sig.get('entry_low', '—')}~{sig.get('entry_high', '—')} "
            f"状态={sig.get('status', '—')} 质量={sig.get('score_grade', '—')}/{sig.get('score_total', '—')}"
        )

    accepted = sum(1 for row in validated if row.get("accepted"))
    rejected = len(validated) - accepted
    llm_level_line = (
        f"LLM 点位提出 {len(levels)} 条，校验通过 {accepted} 条，拒绝 {rejected} 条"
        if levels or validated
        else _stage_source_text(stage_meta, "llm_levels")
    )
    debate_strength = float(debate.get("consensus_strength") or 0)
    trader_source = _stage_source_text(stage_meta, "trader")
    decision_confidence = float(decision.get("confidence") or 0)

    return "\n".join(
        [
            (
                f"- **数据**：{meta.get('data_source', '—')}，"
                f"当前价 {metrics.get('current_price', '—')}，"
                f"更新时间 {meta.get('updated_at', '—')}。"
            ),
            (
                f"- **结构**：多 {sentiment.get('bullish', '—')}% / "
                f"空 {sentiment.get('bearish', '—')}% / "
                f"震荡 {sentiment.get('ranging', '—')}%。"
            ),
            f"- **分析师团队**（{_stage_source_text(stage_meta, 'analyst_team')}）：{'; '.join(analyst_bits)}。",
            f"- **多空研究**：看多={_stage_source_text(stage_meta, 'bullish')}；看空={_stage_source_text(stage_meta, 'bearish')}。",
            (
                f"- **辩论**（{_stage_source_text(stage_meta, 'debate')}）："
                f"共识 {label_bias(debate.get('consensus_bias', '—'))}，强度 {debate_strength:.0%}。"
            ),
            f"- **点位**：{llm_level_line}。",
            (
                f"- **交易员**（{trader_source}）："
                f"主方向 {label_trade_direction(proposal.get('primary_direction', '—'))}，"
                f"信号 {proposal.get('signal_indices', [])}。"
            ),
            (
                f"- **风控/经理**：经理动作 {label_action(decision.get('action', '—'))}，"
                f"方向 {label_trade_direction(decision.get('primary_direction', '—'))}，"
                f"置信 {decision_confidence:.0%}。"
            ),
            f"- **结论**：{conclusion.get('market_sentiment', '—')}；{decision.get('summary', '')}",
            "",
            "**候选信号**",
            *(f"- {line}" for line in signal_bits),
        ]
    )


def render_agent_trace_panel(report: dict) -> None:
    trace = report.get("agent_trace")
    if not trace:
        st.caption("暂无 agent_trace 数据")
        return

    stage_meta = trace.get("stage_meta") or {}
    analyst_team = trace.get("analyst_team") or {}
    decision = trace.get("decision", {})
    debate = trace.get("debate", {})
    llm_levels = trace.get("llm_levels") or []
    validated_plans = trace.get("validated_plans") or []
    proposal = trace.get("proposal", {})
    risk_reviews = trace.get("risk_reviews", [])

    sentiment = report.get("sentiment") or {}
    debate_bias = debate.get("consensus_bias")
    if debate_bias in ("bullish", "bearish") and sentiment:
        bear = float(sentiment.get("bearish", 0))
        bull = float(sentiment.get("bullish", 0))
        struct_bias = "bearish" if bear >= bull else "bullish" if bull > bear else "neutral"
        if struct_bias in ("bullish", "bearish") and debate_bias != struct_bias:
            st.warning(
                "辩论共识与结构情绪主导方向不一致："
                f"辩论={debate_bias}，结构情绪主导={struct_bias}。"
                "请以经理决策与风控结论为准，并核对信号主/备选标签。"
            )

    st.markdown("**阶段摘要**")
    st.markdown(_render_stage_summary_grid(report, trace), unsafe_allow_html=True)

    meta_report = report.get("meta") or {}
    if not meta_report.get("execution_authorized"):
        st.info(
            "经理未授权执行：交易计划区展示的是规则候选方案；"
            "请以本页「经理决策 / 风控」为准。"
            + (
                " 当前为快照观察模式，风控因行情非可执行而全部否决。"
                if meta_report.get("observation_mode")
                else ""
            )
        )

    c1, c2, c3 = st.columns(3)
    mgr_meta = stage_meta.get("manager") or {}
    with c1:
        st.metric("经理决策", label_action(decision.get("action", "—")))
        st.caption(f"{_badge_md(mgr_meta)} · 置信 {decision.get('confidence', 0):.0%}")
    debate_meta = stage_meta.get("debate") or {}
    with c2:
        st.metric("辩论共识", label_bias(debate.get("consensus_bias", "—")))
        st.caption(f"{_badge_md(debate_meta)} · 强度 {debate.get('consensus_strength', 0):.0%}")
    trader_meta = stage_meta.get("trader") or {}
    with c3:
        st.metric("交易员", label_trade_direction(proposal.get("primary_direction", "—")))
        st.caption(f"{_badge_md(trader_meta)} · 信号 {proposal.get('signal_indices', [])}")

    st.markdown("**经理摘要**")
    st.markdown(decision.get("summary", "—"))

    st.markdown("**本次决策流程摘要**")
    st.markdown(_decision_flow_markdown(report, trace))

    if analyst_team:
        team_meta = stage_meta.get("analyst_team") or {}
        st.markdown(f"**分析师团队** {_badge_md(team_meta)}")
        labels = {
            "technical": "技术",
            "fundamentals": "基本面",
            "news": "新闻",
            "sentiment": "情绪",
        }
        row1 = st.columns(2)
        row2 = st.columns(2)
        for col, (key, title) in zip(row1 + row2, labels.items()):
            analyst_report = analyst_team.get(key) or {}
            analyst_meta = stage_meta.get(key) or {}
            with col:
                st.markdown(f"**{title}** {_badge_md(analyst_meta)}")
                if analyst_meta.get("llm"):
                    cap = stage_llm_caption(stage_meta, key)
                    if cap:
                        st.caption(cap)
                st.caption(f"倾向：{label_bias(analyst_report.get('bias', '—'))}")
                st.markdown(analyst_report.get("summary", "—"))
                st.caption(f"{len(analyst_report.get('items', []))} 条证据")

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
        st.markdown(bull.get("summary", "—"))
        st.caption(f"{len(bull.get('items', []))} 条证据")
    with r2:
        st.markdown(f"**看空研究** {_badge_md(bear_meta)}")
        if bear_meta.get("llm"):
            st.caption(stage_llm_caption(stage_meta, "bearish"))
        st.markdown(bear.get("summary", "—"))
        st.caption(f"{len(bear.get('items', []))} 条证据")

    if proposal.get("rationale"):
        st.markdown("**交易员理由**")
        for line in proposal.get("rationale", [])[:4]:
            st.markdown(f"- {line}")

    levels_meta = stage_meta.get("llm_levels") or {}
    if llm_levels or validated_plans or "llm_levels" in stage_meta:
        st.markdown(f"**LLM点位提议** {_badge_md(levels_meta)}")
        if llm_levels:
            st.dataframe(
                [
                    {
                        "方向": p.get("direction", "—"),
                        "入场": f"{p.get('entry_low', '—')} ~ {p.get('entry_high', '—')}",
                        "止损": p.get("stop_loss", "—"),
                        "止盈": " / ".join(str(x) for x in p.get("take_profits", [])),
                        "置信": f"{float(p.get('confidence', 0)):.0%}",
                        "类型": p.get("setup_type", "—"),
                    }
                    for p in llm_levels
                ],
                width="stretch",
                hide_index=True,
            )
        else:
            st.caption("本次没有 LLM 点位提议，或该阶段未启用。")

        if validated_plans:
            st.markdown("**点位校验**")
            st.dataframe(
                [
                    {
                        "序号": row.get("index", ""),
                        "结果": "通过" if row.get("accepted") else "拒绝",
                        "原因": row.get("reason", ""),
                        "方向": (row.get("proposal") or {}).get("direction", "—"),
                        "入场": (
                            f"{(row.get('proposal') or {}).get('entry_low', '—')} ~ "
                            f"{(row.get('proposal') or {}).get('entry_high', '—')}"
                        ),
                    }
                    for row in validated_plans
                ],
                width="stretch",
                hide_index=True,
            )

    risk_meta = stage_meta.get("risk") or {}
    st.markdown(f"**风控** {_badge_md(risk_meta)}")
    if risk_reviews:
        st.dataframe(
            [
                {
                    "风格": label_risk_profile(r.get("profile", "—")),
                    "通过": "✓" if r.get("approved") else "✗",
                    "仓位": label_position_scale(r.get("position_scale", 0)),
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
        st.markdown(f"**报告文案层** {_badge_md({'source': 'llm'})}")

    with st.expander("完整 agent_trace JSON", expanded=False):
        st.code(json.dumps(trace, ensure_ascii=False, indent=2), language="json")


def render_agent_trace_sidebar(report: dict) -> None:
    """Legacy sidebar entry — delegates to panel."""
    render_agent_trace_panel(report)
