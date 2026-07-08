"""Streamlit view renderers for institutional report and strategy map."""

from __future__ import annotations

import streamlit as st

from src.config import TV_EXCHANGE, TV_SYMBOL, WATERMARK_TEXT
from src.viz.charts import build_sentiment_donut
from src.viz.dashboard_components import (
    render_bottom_row,
    render_decision_summary,
    render_footer,
    render_key_levels,
    render_primary_plan_focus,
    render_strategy_sections,
    render_tf_panel,
    render_trading_plans,
)
from src.viz.lightweight_chart import build_lightweight_chart_html, chart_iframe_height

_TOP_DONUT_HEIGHT = 165
_TF_STRIP_LABELS = {"4h": "4H", "1h": "1H", "15m": "15M"}


def _embed_chart(
    data,
    analysis,
    report,
    macro,
    tf,
    *,
    variant: str = "main",
    watermark=None,
    projections=True,
    show_title: bool = True,
    iframe_height: int | None = None,
    chart_height: int | None = None,
):
    if show_title:
        st.markdown(
            f'<p class="chart-box-title">{ {"15m": "15m 结构", "5m": "5m 执行", "4h": "4H", "1h": "1H", "1d": "日线主图"}.get(tf, tf) }</p>',
            unsafe_allow_html=True,
        )
    iframe_h = iframe_height if iframe_height is not None else chart_iframe_height(variant)
    internal_h = chart_height
    if internal_h is None and iframe_height is not None and variant in ("mini", "strip"):
        internal_h = max(48, iframe_height - 4)
    st.iframe(
        build_lightweight_chart_html(
            data[tf],
            analysis=analysis,
            report=report,
            macro_analysis=macro,
            timeframe=tf,
            symbol=TV_SYMBOL,
            symbol_name="黄金/美元",
            exchange=TV_EXCHANGE,
            variant=variant,
            watermark=watermark,
            show_projections=projections,
            height=internal_h,
        ),
        height=iframe_h,
        width="stretch",
    )


def _top_text_panel(title: str, body_html: str) -> None:
    st.markdown(
        f'<div class="hbox panel top-cell"><p class="lbl">{title}</p>{body_html}</div>',
        unsafe_allow_html=True,
    )


def render_institutional_report(report, data, analyses, *, hide_title: bool = False) -> None:
    """One-page dashboard layout (reference: 4 top panels + 3-col body + 4 bottom panels)."""
    meta = report["meta"]
    conclusion = report["conclusion"]

    if not hide_title:
        st.markdown(f'<p class="report-title">{meta["title"]}</p>', unsafe_allow_html=True)
        st.markdown(
            f'<p class="report-meta">更新时间: {meta["updated_at"]} &nbsp;|&nbsp; '
            f'数据源: {meta.get("data_source", "TradingView")} &nbsp;|&nbsp; {meta["methodology"]}</p>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f'<p class="report-meta">数据源: {meta.get("data_source", "TradingView")} · '
            f'外部数据见导航 <b>外部数据</b></p>',
            unsafe_allow_html=True,
        )

    st.markdown(render_decision_summary(report), unsafe_allow_html=True)
    st.markdown('<div class="report-top-row-anchor"></div>', unsafe_allow_html=True)

    top1, top2, top3, top4 = st.columns(4)
    with top1:
        overview = report.get("market_overview", [])
        ov_html = "".join(f"<li>{x}</li>" for x in overview[:5])
        _top_text_panel("📊 市场总览", f'<ul class="bullet-list">{ov_html or "<li>—</li>"}</ul>')
    with top2:
        liq = report.get("liquidity", [])[:5]
        liq_html = "".join(
            f"<li>[{item['timeframe']}] <b>{item['price']:.0f}</b> {item['label'][:16]}</li>" for item in liq
        )
        _top_text_panel("💧 关键流动性", f'<ul class="bullet-list">{liq_html or "<li>—</li>"}</ul>')
    with top3:
        _top_text_panel(
            "⚡ 结论要点",
            f'<ul class="bullet-list">'
            f'<li>{conclusion.get("header_conclusion", conclusion["action"])}</li>'
            f'<li>{conclusion["direction_summary"]}</li></ul>',
        )
    with top4:
        with st.container(border=True):
            fig = build_sentiment_donut(report["sentiment"])
            fig.update_layout(
                height=_TOP_DONUT_HEIGHT,
                margin=dict(t=36, b=12, l=8, r=8),
                title=dict(font=dict(size=13)),
            )
            st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})

    st.markdown('<p class="section-h tight tf-multi-section-h">多周期结构</p>', unsafe_allow_html=True)
    st.markdown('<div class="tf-multi-row-anchor"></div>', unsafe_allow_html=True)
    tf4, tf1, tf15 = st.columns(3, gap="small")
    for col, tf in zip((tf4, tf1, tf15), ("4h", "1h", "15m")):
        with col:
            with st.container(border=True):
                st.markdown(
                    f'<p class="tf-col-label">{_TF_STRIP_LABELS[tf]}</p>',
                    unsafe_allow_html=True,
                )
                _embed_chart(
                    data,
                    analyses[tf],
                    report,
                    analyses.get("1h"),
                    tf,
                    variant="strip",
                    projections=False,
                    show_title=False,
                    iframe_height=chart_iframe_height("strip"),
                )
                st.markdown(
                    render_tf_panel(tf, report["timeframes"][tf], compact=True),
                    unsafe_allow_html=True,
                )

    st.markdown('<div class="tf-main-row-anchor"></div>', unsafe_allow_html=True)
    chart_col, plan_col = st.columns([2.55, 0.95], gap="small")
    with chart_col:
        st.markdown('<p class="section-h tight">5分钟主图</p>', unsafe_allow_html=True)
        _embed_chart(
            data,
            analyses["5m"],
            report,
            analyses["15m"],
            "5m",
            variant="main",
            watermark=WATERMARK_TEXT,
            projections=False,
            show_title=False,
            iframe_height=chart_iframe_height("main"),
        )
    with plan_col:
        st.markdown('<p class="section-h tight">交易计划</p>', unsafe_allow_html=True)
        st.markdown(render_primary_plan_focus(report), unsafe_allow_html=True)
        st.markdown(render_trading_plans(report["signals"], include_primary=False), unsafe_allow_html=True)

    st.markdown(render_bottom_row(report, conclusion), unsafe_allow_html=True)
    st.markdown(render_footer(report), unsafe_allow_html=True)


def render_strategy_map(report, data, analyses) -> None:
    meta = report["meta"]
    st.markdown(f'<p class="report-title center">{meta["strategy_title"]}</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="report-subtitle">{meta["strategy_subtitle"]}</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="report-meta" style="text-align:right;">生成时间: {meta["updated_at"]}</p>', unsafe_allow_html=True)
    st.markdown(render_decision_summary(report), unsafe_allow_html=True)
    st.markdown(render_primary_plan_focus(report), unsafe_allow_html=True)

    st.markdown('<div class="strategy-layout-anchor"></div>', unsafe_allow_html=True)
    chart_col, levels_col, strategy_col = st.columns([2.2, 0.65, 1.15])
    with chart_col:
        _embed_chart(data, analyses["15m"], report, analyses["1h"], "15m", variant="strategy", projections=False)
        _embed_chart(data, analyses["5m"], report, analyses["15m"], "5m", variant="strategy", projections=False)
    with levels_col:
        st.markdown('<p class="section-h">关键价位</p>', unsafe_allow_html=True)
        st.markdown(render_key_levels(report.get("key_levels", [])), unsafe_allow_html=True)
        boundary = report.get("resistance_levels", [""])[0] if report.get("resistance_levels") else ""
        st.markdown(f'<p style="font-size:11px;color:#64748b;text-align:center;">多空分界<br>{boundary}</p>', unsafe_allow_html=True)
    with strategy_col:
        st.markdown(render_strategy_sections(report), unsafe_allow_html=True)
    st.markdown(render_footer(report), unsafe_allow_html=True)
