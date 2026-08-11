"""Compact Streamlit renderer for Advice V2."""

from __future__ import annotations

import html
from typing import Any

import streamlit as st

ADVICE_CSS = """
<style>
.block-container{max-width:1320px;padding-top:1.4rem}
.page-hero{padding:1.15rem 1.35rem;margin-bottom:1rem;border:1px solid #dbe3ee;border-radius:14px;background:linear-gradient(135deg,#fff,#f7fafc)}
.page-hero h1{margin:0;color:#172033;font-size:1.75rem}.page-hero p{margin:.35rem 0 0;color:#64748b}
.advice-banner{padding:1.15rem 1.25rem;border-radius:14px;border:1px solid #cbd5e1;background:#fff;margin-bottom:1rem}
.advice-banner.long{border-left:6px solid #16a34a}.advice-banner.short{border-left:6px solid #dc2626}
.advice-banner.wait{border-left:6px solid #64748b}.advice-banner.avoid{border-left:6px solid #d97706}
.advice-kicker{font-size:.78rem;color:#64748b;letter-spacing:.08em}.advice-title{font-size:1.35rem;font-weight:750;color:#172033;margin:.2rem 0}.advice-summary{color:#334155;margin:0}
.section-card,.panel-box{border:1px solid #dbe3ee;border-radius:12px;background:#fff;padding:1rem 1.1rem;margin-bottom:1rem}
.section-card h3,.panel-box h4{margin:.05rem 0 .65rem;color:#172033}.report-meta,.lbl{color:#64748b;font-size:.86rem}
.zone-price{font-size:1.55rem;font-weight:750;color:#172033}.status-pill{display:inline-block;padding:.2rem .55rem;border-radius:999px;background:#eef2ff;color:#3730a3;font-size:.8rem}
.bullet-list{margin:.35rem 0 .2rem;padding-left:1.2rem}.bullet-list li{margin:.32rem 0;color:#334155}
.check-list{counter-reset:item;list-style:none;padding:0}.check-list li{padding:.55rem .7rem .55rem 2.4rem;margin:.4rem 0;background:#f8fafc;border-radius:8px;position:relative}.check-list li:before{counter-increment:item;content:counter(item);position:absolute;left:.7rem;top:.48rem;width:1.25rem;height:1.25rem;border-radius:50%;background:#334155;color:#fff;text-align:center;font-size:.78rem;line-height:1.25rem}
.ext-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:.75rem}.span-2{grid-column:span 2}.cal-item{padding:.35rem 0;border-bottom:1px solid #eef2f7}.ext-kind{font-size:.72rem;color:#475569;background:#f1f5f9;border-radius:4px;padding:.1rem .3rem}.source-tag{font-size:.72rem;color:#475569;margin-left:.3rem}
@media(max-width:800px){.ext-grid{grid-template-columns:1fr}.span-2{grid-column:span 1}}
</style>
"""

_DECISION_CN = {
    "WATCH_LONG": "关注做多机会",
    "WATCH_SHORT": "关注做空机会",
    "WAIT": "观望",
    "AVOID": "暂不形成建议",
}
_BIAS_CN = {"bullish": "偏多", "bearish": "偏空", "mixed": "分歧", "neutral": "中性"}
_CONFIDENCE_CN = {"high": "较清晰", "medium": "中等", "low": "较低"}


def _list(items: list[Any], *, css: str = "bullet-list") -> str:
    return f'<ul class="{css}">' + "".join(f"<li>{html.escape(str(item))}</li>" for item in items) + "</ul>"


def render_advice_report(report: dict[str, Any], data: dict, analyses: dict) -> None:
    advice = report.get("advice") or {}
    decision = str(advice.get("decision") or "AVOID")
    theme = {"WATCH_LONG": "long", "WATCH_SHORT": "short", "WAIT": "wait"}.get(decision, "avoid")
    bias = _BIAS_CN.get(str(advice.get("bias")), str(advice.get("bias") or "—"))
    confidence = _CONFIDENCE_CN.get(str(advice.get("confidence")), str(advice.get("confidence") or "—"))
    title = _DECISION_CN.get(decision, decision)
    summary = html.escape(str(advice.get("summary") or "—"))
    horizon = html.escape(str(advice.get("horizon") or "—"))
    price = float(advice.get("current_price") or report.get("metrics", {}).get("current_price") or 0.0)
    st.markdown(
        f"""
<div class="advice-banner {theme}">
  <div class="advice-kicker">当前建议 · {horizon}</div>
  <div class="advice-title">{title} · 市场背景{bias}</div>
  <p class="advice-summary">{summary}</p>
  <p class="report-meta">当前价格 {price:.2f} · 判断清晰度 {confidence} · 最终执行由用户人工确认</p>
</div>
""",
        unsafe_allow_html=True,
    )

    setup = advice.get("primary_setup")
    if isinstance(setup, dict):
        zone = setup.get("attention_zone") or {}
        low, high = float(zone.get("low") or 0), float(zone.get("high") or 0)
        left, right = st.columns([1.25, 1])
        with left:
            st.markdown(
                f"""
<div class="section-card">
  <h3>首选关注方案</h3>
  <div class="zone-price">{low:.2f}–{high:.2f}</div>
  <p class="report-meta">{html.escape(str(zone.get('label') or '结构关注区'))}</p>
  <span class="status-pill">{html.escape(str(setup.get('current_state') or '—'))}</span>
  <h4>为什么关注</h4>{_list(list(setup.get('rationale') or []))}
</div>
""",
                unsafe_allow_html=True,
            )
        with right:
            targets = " / ".join(f"{float(value):.2f}" for value in setup.get("targets") or []) or "—"
            rr = " / ".join(f"{float(value):.2f}R" for value in setup.get("reward_risk_to_targets") or []) or "—"
            st.markdown(
                f"""
<div class="section-card">
  <h3>失效与参考空间</h3>
  <p><b>失效：</b>{html.escape(str(setup.get('invalidation') or '—'))}</p>
  <p><b>参考目标：</b>{targets}</p>
  <p><b>几何空间：</b>{rr}</p>
  <p class="report-meta">仅用于人工评估，不构成自动下单或仓位授权。</p>
</div>
""",
                unsafe_allow_html=True,
            )
        st.markdown(
            '<div class="section-card"><h3>人工确认清单</h3>'
            + _list(list(setup.get("confirmation_checklist") or []), css="check-list")
            + "</div>",
            unsafe_allow_html=True,
        )
    else:
        st.info("本次没有达到建议门槛的首选方案。观望本身是有效结论，不强行补齐多空计划。")

    alt = advice.get("alternative_scenario")
    risks = list(advice.get("risks") or [])
    uncertainties = list(advice.get("uncertainties") or [])
    left, right = st.columns(2)
    with left:
        if isinstance(alt, dict):
            st.markdown(
                '<div class="section-card"><h3>反向条件预案</h3>'
                f'<p><b>条件：</b>{html.escape(str(alt.get("condition") or "—"))}</p>'
                f'<p><b>响应：</b>{html.escape(str(alt.get("response") or "—"))}</p></div>',
                unsafe_allow_html=True,
            )
    with right:
        st.markdown(
            '<div class="section-card"><h3>风险与不确定性</h3>'
            + _list(risks + uncertainties or ["暂无额外风险说明"])
            + "</div>",
            unsafe_allow_html=True,
        )

    with st.expander("查看分析依据与一致性审计", expanded=False):
        st.markdown("#### 多周期背景")
        for item in advice.get("market_context") or []:
            st.write("-", item)
        st.markdown("#### 建议引用事实")
        st.dataframe(advice.get("evidence") or [], use_container_width=True, hide_index=True)
        audit = advice.get("audit") or {}
        if audit.get("passed"):
            st.success(f"一致性审计通过 · {audit.get('policy_version', 'human-advice-v2')}")
        else:
            st.error("一致性审计未通过：" + "；".join(audit.get("violations") or []))
