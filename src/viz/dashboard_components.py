"""Extended dashboard components — institutional + strategy map (white theme)."""

from __future__ import annotations

from typing import Any

from src.config import GITHUB_REPO, PROJECT_NAME
from src.viz.source_labels import render_source_badge, stage_source

DASHBOARD_CSS = """
<style>
/* ── Streamlit 全局 ── */
.block-container { padding-top: 1rem; padding-bottom: 2rem; max-width: 1320px; }
[data-testid="stSidebar"] { background: #f8fafc; }
[data-testid="stSidebar"] .block-container { padding-top: 1.25rem; }

/* ── 页面标题区 ── */
.page-hero {
  background: linear-gradient(135deg, #fff7ed 0%, #ffffff 55%);
  border: 1px solid #fed7aa;
  border-radius: 10px;
  padding: 14px 18px;
  margin-bottom: 16px;
}
.page-hero h1 { font-size: 1.45rem; font-weight: 700; color: #0f172a; margin: 0 0 4px 0; }
.page-hero p { font-size: 0.88rem; color: #64748b; margin: 0; }

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] { gap: 6px; background: transparent; border-bottom: 1px solid #e2e8f0; }
.stTabs [data-baseweb="tab"] {
  height: 38px; padding: 0 14px; border-radius: 8px 8px 0 0;
  font-size: 0.88rem; font-weight: 600; color: #64748b;
}
.stTabs [aria-selected="true"] { color: #0f172a; background: #fff7ed; border: 1px solid #fed7aa; border-bottom-color: #fff7ed; }

/* ── 卡片分区 ── */
.section-card {
  background: #fff;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  padding: 14px 16px;
  margin-bottom: 14px;
}
.section-card h3 { font-size: 1rem; font-weight: 700; color: #0f172a; margin: 0 0 10px 0; }

.report-title { font-size: 1.35rem; font-weight: 700; color: #0f172a; margin: 0 0 4px 0; }
.report-title.center { color: #0f172a; text-align: center; font-size: 1.5rem; }
.report-subtitle { text-align: center; color: #64748b; font-size: 0.85rem; margin: 0 0 12px; }
.report-meta { font-size: 0.8rem; color: #64748b; margin-bottom: 12px; }
.header-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 10px;
  margin-bottom: 12px;
}
.top-grid-4 { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 10px; margin-bottom: 12px; }
.hbox { background: #fff; border: 1px solid #e2e8f0; border-radius: 8px; padding: 10px 12px; min-height: 72px; box-shadow: 0 1px 2px rgba(15,23,42,0.04); }
.hbox.panel { border: 1px solid #e2e8f0; }
.hbox .lbl { font-size: 11px; color: #64748b; margin: 0; }
.hbox .val { font-size: 1.15rem; font-weight: 700; margin: 2px 0 0; line-height: 1.2; color: #0f172a; }
.hbox .val.sm { font-size: 0.82rem; font-weight: 600; line-height: 1.35; color: #334155; }
.hbox .bear { color: #dc2626; }
.hbox .bull { color: #16a34a; }
.panel-box { background: #fff; border: 1px solid #e2e8f0; border-radius: 8px; padding: 10px 12px; margin-bottom: 8px; font-size: 12px; color: #334155; line-height: 1.55; }
.panel-box h4 { margin: 0 0 8px; font-size: 13px; color: #0f172a; display: flex; align-items: center; gap: 8px; }
.num-badge { display: inline-flex; align-items: center; justify-content: center; width: 22px; height: 22px; background: #0f172a; color: #fff; font-weight: 700; font-size: 12px; border-radius: 4px; }
.tf-panel { background: #fff; border: 1px solid #e2e8f0; border-radius: 6px; padding: 10px 12px; margin-bottom: 8px; font-size: 12px; line-height: 1.55; color: #334155; }
.tf-panel h4 { margin: 0 0 6px; font-size: 13px; color: #0f172a; }
.tf-panel .bear { color: #dc2626; font-weight: 600; }
.tf-panel .bull { color: #16a34a; font-weight: 600; }
.level-ladder { display: flex; flex-direction: column; gap: 6px; }
.level-item { border: 1px solid #e2e8f0; border-radius: 8px; padding: 8px 10px; text-align: center; background: #fff; }
.level-item.resistance { border-color: #fca5a5; background: #fff5f5; }
.level-item.support { border-color: #86efac; background: #f0fdf4; }
.level-item .price { font-size: 1.25rem; font-weight: 700; color: #0f172a; }
.level-item .lbl { font-size: 11px; color: #64748b; margin-top: 2px; }
.plan-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; }
.plan-card { border: 1px solid #e2e8f0; border-radius: 6px; overflow: hidden; font-size: 12px; }
.plan-card .head { padding: 8px 10px; font-weight: 700; color: #fff; text-align: center; font-size: 13px; }
.plan-card.short .head { background: linear-gradient(135deg, #dc2626, #b91c1c); }
.plan-card.short.alt .head { background: linear-gradient(135deg, #991b1b, #7f1d1d); }
.plan-card.long .head { background: linear-gradient(135deg, #16a34a, #15803d); }
.plan-card .body { padding: 8px 10px; background: #fff; line-height: 1.6; }
.plan-card .body b { color: #475569; font-weight: 600; }
.llm-narrative-box {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 12px 14px;
  font-size: 13px;
  line-height: 1.65;
  color: #334155;
  margin-top: 6px;
}
.llm-narrative-box p { margin: 0 0 8px; }
.llm-narrative-box p:last-child { margin-bottom: 0; }
.llm-narrative-box ul { margin: 4px 0 8px; padding-left: 18px; }
.llm-narrative-box li { margin-bottom: 4px; }
.llm-narrative-box b { color: #0f172a; }
.path-card { border-left: 4px solid #94a3b8; padding: 6px 10px; margin-bottom: 6px; font-size: 11px; background: #fafafa; border-radius: 0 6px 6px 0; }
.section-h { font-size: 14px; font-weight: 700; color: #0f172a; margin: 8px 0 6px; border-left: 3px solid #dc2626; padding-left: 8px; }
.liq-list, .bullet-list { font-size: 12px; line-height: 1.6; color: #334155; margin: 0; padding-left: 16px; }
.cal-item { font-size: 12px; padding: 4px 0; border-bottom: 1px dashed #e2e8f0; }
.footer-bar { background: linear-gradient(90deg, #dc2626, #b91c1c); color: #fff; padding: 8px 14px; border-radius: 6px; font-size: 12px; margin-top: 10px; }
.footer-brand { text-align: center; margin-top: 10px; padding-top: 8px; border-top: 1px solid #e2e8f0; font-size: 12px; color: #64748b; font-weight: 600; }
.star-list { font-size: 12px; line-height: 1.65; color: #334155; margin: 0; padding-left: 0; list-style: none; }
.star-list li::before { content: "★ "; color: #eab308; }
.chart-box-title { font-size: 12px; font-weight: 700; color: #0f172a; margin: 0 0 4px; padding: 6px 10px; border: 1px solid #e2e8f0; border-bottom: none; border-radius: 6px 6px 0 0; background: #f8fafc; }
.chart-stack { margin-bottom: 10px; }
.agent-source-bar { display: flex; flex-wrap: wrap; gap: 8px; align-items: center; margin-bottom: 14px; padding: 10px 12px; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; font-size: 11px; }
.agent-mode-tag { color: #64748b; font-weight: 600; margin-right: 4px; }
.stage-chip { display: inline-flex; align-items: center; gap: 4px; padding: 2px 8px; background: #fff; border: 1px solid #e2e8f0; border-radius: 4px; color: #334155; }
.src-badge { display: inline-block; padding: 1px 6px; border-radius: 3px; font-size: 10px; font-weight: 700; line-height: 1.4; }
.src-badge.sm { font-size: 9px; padding: 0 5px; }
.src-badge.rule { background: #e2e8f0; color: #475569; }
.src-badge.llm { background: #ede9fe; color: #6d28d9; }
.stage-model { font-size: 10px; color: #64748b; margin-left: 4px; }
.val-with-badge { display: flex; flex-wrap: wrap; align-items: flex-start; gap: 6px; }

/* ── 决策链页 ── */
.trace-block { padding: 8px 0; border-bottom: 1px solid #f1f5f9; margin-bottom: 8px; }
.trace-block:last-child { border-bottom: none; }
.step-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 6px 16px; font-size: 0.9rem; }
</style>
"""

# Re-export helpers from original module patterns
TF_LABELS = {
    "1h": "1H周期（大结构）",
    "4h": "4H周期（大结构）",
    "15m": "15min周期（中间结构）",
}
TREND_CN = {"bearish": ("空头", "bear"), "bullish": ("多头", "bull"), "ranging": ("震荡", "")}


def _chg_class(change: float) -> str:
    return "bear" if change < 0 else "bull"


def render_header(report: dict[str, Any]) -> str:
    m = report["metrics"]
    c = report["conclusion"]
    ext = report.get("external", {})
    cls = _chg_class(m["daily_change"])

    debate_src = stage_source(report, "debate")
    debate_badge = render_source_badge(debate_src, small=True)
    conclusion_text = c.get("header_conclusion", c["action"])
    if c.get("llm_trade_thesis"):
        conclusion_badge = render_source_badge("llm", small=True)
    else:
        conclusion_badge = debate_badge

    boxes = [
        ("当前价格", f"{m['current_price']:.2f}", cls, ""),
        ("日涨跌", f"{m['daily_change']:+.2f} ({m['daily_change_pct']:+.2f}%)", cls, ""),
        ("日高/日低", f"{m['daily_high']:.2f} / {m['daily_low']:.2f}", "", ""),
        ("市场情绪", c["market_sentiment"], cls, ""),
        ("美元指数影响", ext.get("dxy_impact", "—"), "", ""),
        ("风险事件影响", ext.get("risk_events", "—"), "sm", ""),
        (
            "当前结论",
            f'<span class="val-with-badge">{conclusion_badge}<span>{conclusion_text}</span></span>',
            "sm",
            "",
        ),
    ]
    parts = ['<div class="header-grid">']
    for label, val, vcls, _extra in boxes:
        vc = f" {vcls}" if vcls in ("bear", "bull") else (" sm" if vcls == "sm" else "")
        parts.append(f'<div class="hbox"><p class="lbl">{label}</p><p class="val{vc}">{val}</p></div>')
    parts.append("</div>")
    return "".join(parts)


def render_top_overview_row(report: dict[str, Any]) -> str:
    overview = report.get("market_overview", [])
    paths = report.get("path_summary", [])
    liq = report.get("liquidity", [])[:4]

    ov_html = "".join(f"<li>{x}</li>" for x in overview)
    path_html = "".join(
        f'<div class="path-card" style="border-color:{p["color"]}">'
        f'<b>{p["id"]}</b> {p["probability"]}% — {p["name"]}<br><span style="color:#64748b">{p["summary"][:80]}…</span></div>'
        for p in paths
    )
    liq_html = "".join(f"<li>{item['price']:.0f} {item['label'][:20]}</li>" for item in liq)

    return f"""
<div class="top-grid-4">
  <div class="hbox panel"><p class="lbl">📊 顶级市场总览</p><ul class="bullet-list">{ov_html}</ul></div>
  <div class="hbox panel"><p class="lbl">🎯 高概率路径摘要</p>{path_html}</div>
  <div class="hbox panel"><p class="lbl">💧 关键流动性位置</p><ul class="bullet-list">{liq_html}</ul></div>
  <div class="hbox panel"><p class="lbl">⚡ 今日要点</p><ul class="bullet-list">
    <li>{report['conclusion']['direction_summary']}</li>
    <li>{report['conclusion']['action']}</li>
  </ul></div>
</div>
"""


def _fmt_zone(items: list[dict], direction: str | None = None) -> str:
    filtered = [i for i in items if not direction or i.get("direction") == direction]
    if not filtered:
        return "—"
    return " / ".join(f"{i['low']:.0f}-{i['high']:.0f}" for i in filtered[:2])


def render_tf_panel(tf: str, info: dict[str, Any]) -> str:
    label = TF_LABELS.get(tf, tf)
    trend_cn, trend_cls = TREND_CN.get(info["trend"], ("—", ""))
    ema = info.get("ema_relation", {})
    ema_txt = " / ".join(f"{k}{v}" for k, v in ema.items())
    pd_map = {"premium": "溢价区", "discount": "折价区", "equilibrium": "均衡", "unknown": "—"}
    pd_txt = pd_map.get(info.get("premium_discount", ""), "—")
    ob_bear = _fmt_zone(info.get("order_blocks", []), "bearish")
    ob_bull = _fmt_zone(info.get("order_blocks", []), "bullish")
    fvg_bear = _fmt_zone(info.get("fvgs", []), "bearish")
    extra = "<div><b>执行逻辑：</b>关注反弹中位与扫流动性节点</div>" if tf == "15m" else ""
    return f"""
<div class="tf-panel">
  <h4>【{label}】</h4>
  <div>方向：<span class="{trend_cls}">{trend_cn}</span></div>
  <div>BOS：{info.get('bos', '无')} | CHoCH：{info.get('choch', '无')}</div>
  <div>聪明钱：{pd_txt} | 成交量：{info.get('volume_signal', 'N/A')}</div>
  <div>看跌 OB：{ob_bear} | FVG：{fvg_bear}</div>
  {f'<div>看涨 OB：{ob_bull}</div>' if ob_bull != '—' else ''}
  {extra}
</div>
"""


def render_key_levels(levels: list[dict]) -> str:
    items = []
    for lv in levels:
        kind = lv.get("kind", "neutral")
        css = kind if kind in ("resistance", "support") else ""
        if "price_low" in lv:
            price_txt = f"{lv['price_low']:.0f}-{lv['price_high']:.0f}"
        else:
            price_txt = f"{lv['price']:.0f}"
        items.append(
            f'<div class="level-item {css}"><div class="price">{price_txt}</div>'
            f'<div class="lbl">{lv["label"]}</div></div>'
        )
    return f'<div class="level-ladder">{"".join(items)}</div>'


def render_strategy_sections(report: dict[str, Any]) -> str:
    c = report["conclusion"]
    plans = report.get("strategy_plans", [])
    sections = [
        ("1 主方向", f"<p>{c['direction_summary']}。{c['action']}</p>"),
        ("2 关键压力", "<ul class='bullet-list'>" + "".join(f"<li>{x}</li>" for x in report.get("resistance_levels", [])) + "</ul>"),
        ("3 关键支撑", "<ul class='bullet-list'>" + "".join(f"<li>{x}</li>" for x in report.get("support_levels", [])) + "</ul>"),
        ("4 交易计划", _render_plans_text(plans)),
        ("5 关键提醒", "<ul class='bullet-list'>" + "".join(f"<li>{x}</li>" for x in report.get("risk_control", [])) + "</ul>"),
    ]
    parts = []
    for title, body in sections:
        num, label = title.split(" ", 1)
        parts.append(f'<div class="panel-box"><h4><span class="num-badge">{num}</span>{label}</h4>{body}</div>')
    return "".join(parts)


def _render_plans_text(plans: list[dict]) -> str:
    if not plans:
        return "<p>暂无计划</p>"
    blocks = []
    for p in plans:
        theme = "bear" if p.get("theme") == "short" else "bull"
        blocks.append(
            f"<p><b>{p['name']}</b> — {p['logic']}<br>"
            f"入场 {p['entry']} | 止损 {p['stop_loss']} | 目标 {p['targets']}</p>"
        )
    return "".join(blocks)


def render_path_cards(paths: list[dict]) -> str:
    return "".join(
        f'<div class="path-card" style="border-color:{p["color"]}">'
        f'<b>{p["id"]} · {p["probability"]}%</b> {p["name"]}</div>'
        for p in paths
    )


def render_calendar(events: list[dict]) -> str:
    rows = "".join(
        f'<div class="cal-item">{e["time"]} {e.get("flag","")} {e["event"]}</div>'
        for e in events
    )
    return f'<div class="panel-box"><h4>📅 今日重要提醒</h4>{rows}</div>'


def render_trading_plans(signals: list[dict]) -> str:
    if not signals:
        return "<p>暂无交易计划</p>"
    cards = []
    themes = ["short", "short alt", "long"]
    for i, sig in enumerate(signals[:3]):
        theme = themes[i] if i < len(themes) else ("long" if sig.get("theme") == "long" else "short")
        css_theme = theme.replace(" alt", "")
        alt = " alt" if "alt" in theme else ""
        tps = sig.get("take_profits", [])
        tp_lines = "".join(f"<div><b>TP{n}：</b>{tps[n-1]}</div>" for n in range(1, min(4, len(tps) + 1)))
        cards.append(f"""
<div class="plan-card {css_theme}{alt}">
  <div class="head">{sig['name']}</div>
  <div class="body">
    <div><b>方向：</b>{sig.get('direction_cn', sig['direction'])}</div>
    <div><b>入场：</b>{sig['entry_low']} ~ {sig['entry_high']}</div>
    <div><b>止损：</b>{sig['stop_loss']}</div>
    {tp_lines}
    <div><b>盈亏比：</b>{sig['risk_reward']} | <b>胜率：</b>{sig.get('win_rate','—')}</div>
  </div>
</div>""")
    return f'<div class="plan-grid">{"".join(cards)}</div>'


def render_liquidity(items: list[dict]) -> str:
    label_map = {
        "Equal Highs / Sell-side Liquidity": "Equal Highs / 卖方流动性",
        "Equal Lows / Buy-side Liquidity": "Equal Lows / 买方流动性",
        "Stop Hunt Above Highs": "高点上方 Stop Hunt",
        "Stop Hunt Below Lows": "低点下方 Stop Hunt",
    }
    lines = []
    for item in items[:6]:
        lbl = label_map.get(item["label"], item["label"])
        lines.append(f"<li>[{item['timeframe']}] {lbl}: <b>{item['price']:.2f}</b></li>")
    return f'<ul class="liq-list">{"".join(lines)}</ul>'


def render_footer(report: dict[str, Any]) -> str:
    reminders = report.get("footer_reminders", [])
    txt = " | ".join(reminders) if reminders else "注意美盘流动性与数据波动"
    return f"""
<div class="footer-bar">📌 今日重要提醒：{txt}</div>
<div class="footer-brand">{PROJECT_NAME} · {GITHUB_REPO}</div>
"""
