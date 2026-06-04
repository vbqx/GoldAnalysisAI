"""Streamlit view renderers for institutional report and strategy map."""



from __future__ import annotations



import streamlit as st



from src.config import TV_EXCHANGE, TV_SYMBOL, WATERMARK_TEXT

from src.viz.charts import build_projection_chart, build_sentiment_donut

from src.viz.dashboard_components import (

    render_calendar,

    render_footer,

    render_header,

    render_key_levels,

    render_liquidity,

    render_path_cards,

    render_strategy_sections,

    render_tf_panel,

    render_top_overview_row,

    render_trading_plans,

)

from src.viz.lightweight_chart import build_lightweight_chart_html, chart_iframe_height





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

):

    if show_title:

        st.markdown(

            f'<p class="chart-box-title">{ {"15m": "15m 结构判断", "5m": "5m 执行区域", "4h": "4H 结构", "1h": "1H 结构"}.get(tf, tf) }</p>',

            unsafe_allow_html=True,

        )

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

        ),

        height=chart_iframe_height(variant),
        width="stretch",
    )





def render_institutional_report(report, data, analyses) -> None:

    meta = report["meta"]

    conclusion = report["conclusion"]



    st.markdown(f'<p class="report-title">{meta["title"]}</p>', unsafe_allow_html=True)

    st.markdown(

        f'<p class="report-meta">更新时间: {meta["updated_at"]} &nbsp;|&nbsp; '

        f'数据源: {report["meta"].get("data_source", "TradingView")} &nbsp;|&nbsp; {meta["methodology"]}</p>',

        unsafe_allow_html=True,

    )

    st.markdown(render_header(report), unsafe_allow_html=True)

    st.markdown(render_top_overview_row(report), unsafe_allow_html=True)



    left, center, right = st.columns([1.05, 2.35, 1.0])



    with left:

        st.markdown('<p class="section-h">多周期结构</p>', unsafe_allow_html=True)

        for tf in ("4h", "1h", "15m"):

            _embed_chart(data, analyses[tf], report, analyses.get("1h"), tf, variant="mini", projections=False)

            st.markdown(render_tf_panel(tf, report["timeframes"][tf]), unsafe_allow_html=True)

        st.markdown(render_calendar(report.get("calendar_events", [])), unsafe_allow_html=True)



    with center:

        st.markdown('<p class="section-h">5min 周期 (执行主图)</p>', unsafe_allow_html=True)

        _embed_chart(

            data,

            analyses["5m"],

            report,

            analyses["15m"],

            "5m",

            variant="main",

            watermark=WATERMARK_TEXT,

            projections=True,

            show_title=False,

        )



    with right:

        st.markdown('<p class="section-h">统计与策略</p>', unsafe_allow_html=True)

        st.plotly_chart(build_sentiment_donut(report["sentiment"]), width="stretch")

        st.markdown(render_path_cards(report.get("path_summary", [])), unsafe_allow_html=True)

        st.markdown('<p class="section-h">关键流动性</p>', unsafe_allow_html=True)

        st.markdown(render_liquidity(report["liquidity"]), unsafe_allow_html=True)

        st.markdown('<p class="section-h">交易计划</p>', unsafe_allow_html=True)

        st.markdown(render_trading_plans(report["signals"]), unsafe_allow_html=True)



    b1, b2, b3, b4 = st.columns(4)

    fib = report["fibonacci"]

    with b1:

        st.markdown("**Fibonacci 回调参考**")

        st.table({"比例": [f"{f['ratio']:.3f}" for f in fib], "价位": [f["price"] for f in fib], "含义": [f["significance"] for f in fib]})

    with b2:

        st.plotly_chart(build_projection_chart(report["projections"]), width="stretch")

    with b3:

        st.markdown("**风控与失效**")

        for r in report.get("risk_control", []):

            st.markdown(f"- {r}")

        for r in report["invalidation"]:

            st.markdown(f"- {r}")

    with b4:

        st.markdown("**最终结论**")

        st.markdown("<ul class='star-list'>" + "".join(f"<li>{s}</li>" for s in conclusion.get("starred", [])) + "</ul>", unsafe_allow_html=True)



    st.markdown(render_footer(report), unsafe_allow_html=True)





def render_strategy_map(report, data, analyses) -> None:

    meta = report["meta"]

    st.markdown(f'<p class="report-title center">{meta["strategy_title"]}</p>', unsafe_allow_html=True)

    st.markdown(f'<p class="report-subtitle">{meta["strategy_subtitle"]}</p>', unsafe_allow_html=True)

    st.markdown(f'<p class="report-meta" style="text-align:right;">生成时间: {meta["updated_at"]}</p>', unsafe_allow_html=True)



    chart_col, levels_col, strategy_col = st.columns([2.05, 0.52, 1.0])



    with chart_col:

        _embed_chart(data, analyses["15m"], report, analyses["1h"], "15m", variant="strategy", projections=False)

        _embed_chart(data, analyses["5m"], report, analyses["15m"], "5m", variant="strategy", projections=False)



    with levels_col:

        st.markdown('<p class="section-h">关键价位</p>', unsafe_allow_html=True)

        st.markdown(render_key_levels(report.get("key_levels", [])), unsafe_allow_html=True)

        boundary = report.get("resistance_levels", [""])[0] if report.get("resistance_levels") else ""

        st.markdown(f'<p style="font-size:11px;color:#64748b;text-align:center;">多空分界参考<br>{boundary}</p>', unsafe_allow_html=True)



    with strategy_col:

        st.markdown(render_strategy_sections(report), unsafe_allow_html=True)



    st.markdown(render_footer(report), unsafe_allow_html=True)

