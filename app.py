"""Streamlit dashboard for XAUUSD PA+ICT report."""

from __future__ import annotations

import os

# Inject system proxy for TradingView WebSocket connectivity
def _inject_proxy() -> None:
    for key in ("HTTPS_PROXY", "https_proxy", "HTTP_PROXY", "http_proxy"):
        if val := os.environ.get(key):
            os.environ.setdefault("http_proxy", val)
            os.environ.setdefault("https_proxy", val)
            return
    try:
        import winreg
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Internet Settings",
        )
        enable, _ = winreg.QueryValueEx(key, "ProxyEnable")
        if enable:
            server, _ = winreg.QueryValueEx(key, "ProxyServer")
            server = server.split(";")[0].strip()
            proxy = f"http://{server}" if "://" not in server else server
            os.environ.setdefault("http_proxy", proxy)
            os.environ.setdefault("https_proxy", proxy)
        winreg.CloseKey(key)
    except Exception:
        pass

_inject_proxy()

import streamlit as st

from src.config import TV_EXCHANGE, TV_SYMBOL
from src.pipeline import run_analysis
from src.indicators.verify import indicator_snapshot, indicator_table_rows
from src.viz.charts import build_projection_chart, build_sentiment_donut
from src.viz.lightweight_chart import build_lightweight_chart_html

st.set_page_config(
    page_title="XAUUSD PA+ICT Report",
    page_icon="🥇",
    layout="wide",
)

st.sidebar.markdown(
    "数据源：TradingView (`tvDatafeed`)  —  "
    "默认 `OANDA:XAUUSD`。可在 `.env` 配置账号与交易所。"
)
st.sidebar.caption("国内网络可能需要代理/VPN 才能连接 TradingView。")

st.markdown(
    """
    <style>
    .metric-card { background:#0f172a; color:white; padding:12px 16px; border-radius:8px; }
    .metric-card h4 { margin:0; font-size:13px; opacity:0.8; }
    .metric-card p { margin:4px 0 0; font-size:22px; font-weight:700; }
    .bear { color:#f87171; }
    .bull { color:#4ade80; }
    .section-title { font-size:16px; font-weight:600; margin:12px 0 8px; }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data(ttl=300, show_spinner=False)
def load_report():
    from src.data.fetcher import clear_cache

    clear_cache()
    return run_analysis()


def metric_card(label: str, value: str, css_class: str = "") -> str:
    return f'<div class="metric-card"><h4>{label}</h4><p class="{css_class}">{value}</p></div>'


try:
    with st.spinner("正在拉取行情并计算 PA+ICT 结构..."):
        report, data, analyses = load_report()
except Exception as exc:
    st.error(f"数据获取失败: {exc}")
    st.info("请检查网络连接或 TradingView 配置后刷新。")
    st.stop()

meta = report["meta"]
metrics = report["metrics"]
conclusion = report["conclusion"]
sentiment = report["sentiment"]

st.title(meta["title"])
st.caption(
    f"更新时间: {meta['updated_at']}  |  数据源: {meta.get('data_source', 'unknown')}  |  方法论: {meta['methodology']}"
)
if meta.get("data_source_note"):
    st.warning(f"回退原因: {meta['data_source_note']}")

change_cls = "bear" if metrics["daily_change"] < 0 else "bull"
header_cols = st.columns(5)
header_cols[0].markdown(
    metric_card("Current Price", f"{metrics['current_price']:.2f}", change_cls),
    unsafe_allow_html=True,
)
header_cols[1].markdown(
    metric_card(
        "Daily Change",
        f"{metrics['daily_change']:+.2f} ({metrics['daily_change_pct']:+.2f}%)",
        change_cls,
    ),
    unsafe_allow_html=True,
)
header_cols[2].markdown(
    metric_card("Daily High/Low", f"{metrics['daily_high']:.2f} / {metrics['daily_low']:.2f}"),
    unsafe_allow_html=True,
)
header_cols[3].markdown(
    metric_card("Market Sentiment", conclusion["market_sentiment"], change_cls),
    unsafe_allow_html=True,
)
header_cols[4].markdown(
    metric_card("External", "DXY↑ → Gold↓ | US Session Vol"),
    unsafe_allow_html=True,
)

st.info(f"**结论:** {conclusion['direction_summary']}。{conclusion['action']}")

left, center, right = st.columns([1, 2.2, 1])

with left:
    st.markdown('<p class="section-title">Multi-Timeframe Analysis</p>', unsafe_allow_html=True)
    for tf, info in report["timeframes"].items():
        trend = info["trend"]
        emoji = "🔴" if trend == "bearish" else ("🟢" if trend == "bullish" else "⚪")
        with st.expander(f"{tf.upper()} {emoji} {trend}", expanded=tf == "1h"):
            st.write(f"**BOS:** {info['bos']}")
            st.write(f"**CHoCH:** {info['choch']}")
            pd_map = {"premium": "溢价区 (Premium)", "discount": "折价区 (Discount)", "equilibrium": "均衡 (EQ)"}
            st.write(f"**聪明钱区域:** {pd_map.get(info.get('premium_discount', ''), '—')}")
            if info.get("equilibrium"):
                st.write(f"**均衡价 (50%):** {info['equilibrium']:.2f}")
            st.write(f"**成交量:** {info.get('volume_signal', 'N/A')}")
            st.write("**EMA 关系:**")
            for k, v in info["ema_relation"].items():
                st.write(f"- {k}: {v}")
            if info["order_blocks"]:
                st.write("**Order Blocks (聪明钱 OB):**")
                for ob in info["order_blocks"]:
                    st.write(f"- {ob['direction']} {ob['low']:.2f} ~ {ob['high']:.2f}")
            if info["fvgs"]:
                st.write(f"**活跃 FVG ({info.get('active_fvg_count', len(info['fvgs']))}):**")
                for fvg in info["fvgs"]:
                    st.write(f"- {fvg['direction']} {fvg['low']:.2f} ~ {fvg['high']:.2f}")

with center:
    st.components.v1.html(
        build_lightweight_chart_html(
            data["5m"],
            analysis=analyses["5m"],
            report=report,
            macro_analysis=analyses["15m"],
            timeframe="5m",
            symbol=TV_SYMBOL,
            symbol_name="黄金/美元",
            exchange=TV_EXCHANGE,
            height=520,
            bars=120,
        ),
        height=560,
        scrolling=False,
    )

with st.expander("指标校验 (对照 TradingView)", expanded=True):
    snaps = [
        indicator_snapshot(data["5m"], "5m"),
        indicator_snapshot(data["15m"], "15m"),
        indicator_snapshot(data["1h"], "1h"),
        indicator_snapshot(data["4h"], "4h"),
    ]
    st.table(indicator_table_rows(snaps))
    for s in snaps:
        if s.get("notes"):
            st.caption(f"**{s['timeframe']}**: " + "；".join(s["notes"]))
    st.caption(
        "EMA 公式: pandas ewm(span=N, adjust=False)，与 TradingView 默认 EMA 一致。"
        "VWAP 为按 UTC 日历日重置的锚定 VWAP。"
    )

with right:
    st.markdown('<p class="section-title">Statistics & Strategy</p>', unsafe_allow_html=True)
    st.plotly_chart(build_sentiment_donut(sentiment), use_container_width=True)

    st.markdown("**Key Liquidity Positions**")
    for item in report["liquidity"][:6]:
        st.write(f"- [{item['timeframe']}] {item['label']}: **{item['price']:.2f}**")

    st.markdown("**Trading Plan (PA + ICT)**")
    for sig in report["signals"]:
        with st.container(border=True):
            st.markdown(f"**{sig['name']}** ({sig['direction']})")
            st.write(f"Entry: {sig['entry_low']} ~ {sig['entry_high']}")
            st.write(f"SL: {sig['stop_loss']}  |  RR: {sig['risk_reward']}")
            st.write(f"TP: {', '.join(str(tp) for tp in sig['take_profits'])}")
            st.caption(sig["note"])

bottom1, bottom2, bottom3, bottom4 = st.columns(4)

with bottom1:
    st.markdown("**Fibonacci Retracement**")
    st.table(
        {
            "Ratio": [f"{f['ratio']:.3f}" for f in report["fibonacci"]],
            "Price": [f["price"] for f in report["fibonacci"]],
            "Significance": [f["significance"] for f in report["fibonacci"]],
            "Prob": [f"{f['probability']*100:.0f}%" for f in report["fibonacci"]],
        }
    )

with bottom2:
    st.plotly_chart(build_projection_chart(report["projections"]), use_container_width=True)

with bottom3:
    st.markdown("**Risk Control & Invalidation**")
    for rule in report["invalidation"]:
        st.write(f"- {rule}")

with bottom4:
    st.markdown("**Final Conclusion**")
    for item in conclusion["must_do"]:
        st.write(f"- {item}")
    if report["signals"]:
        st.success(f"优先关注: {report['signals'][0]['entry_low']} ~ {report['signals'][0]['entry_high']}")

if st.button("刷新报告"):
    load_report.clear()
    st.rerun()
