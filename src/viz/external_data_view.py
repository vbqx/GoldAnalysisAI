"""External data page — news, calendar, DXY, social; available right after fetch."""

from __future__ import annotations

import html
from typing import Any

import streamlit as st

from src.analysis.report_engine import parse_risk_events_calendar
from src.data.fetch_pipeline import DataFetchResult
from src.viz.dashboard_components import _source_tags
from src.viz.streamlit_common import render_page_hero


def external_snapshot_from_fetch(fetched: DataFetchResult) -> dict[str, Any]:
    ext = fetched.external
    calendar = parse_risk_events_calendar(ext.risk_events) if ext.risk_events != "—" else []
    return {
        "dxy_impact": ext.dxy_impact,
        "risk_events": ext.risk_events,
        "news_headlines": list(ext.news_headlines[:20]),
        "headlines": [h.to_dict() for h in ext.headline_items],
        "flash_headlines": [h.to_dict() for h in ext.headline_items if h.source == "jin10_flash"],
        "article_headlines": [h.to_dict() for h in ext.headline_items if h.source == "jin10_news"],
        "calendar_events": calendar,
        "macro_quotes": [m.to_dict() for m in ext.macro_quotes],
        "social_sentiment": ext.social_sentiment,
        "social_posts": list(ext.social_posts[:10]),
        "sources": list(ext.sources),
        "fetch_errors": list(ext.fetch_errors[:5]),
        "bars": fetched.bars_summary,
        "data_source": fetched.source_label,
        "phase": "fetch",
    }


def external_payload_from_report(report: dict, data: dict | None = None) -> dict[str, Any]:
    ext = dict(report.get("external") or {})
    cal = report.get("calendar_events", None)
    if cal is not None:
        # Preserve confirmed-empty [] from the report; do not fall back to stale rows.
        ext["calendar_events"] = list(cal)
    else:
        ext["calendar_events"] = list(ext.get("calendar_events") or [])
    if data:
        ext["bars"] = {tf: len(df) for tf, df in data.items()}
    ext.setdefault("bars", {})
    ext["data_source"] = report.get("meta", {}).get("data_source", ext.get("data_source", ""))
    ext["phase"] = "report"
    return ext


def _render_headline_list(items: list[dict], *, empty: str) -> str:
    if not items:
        return f"<li>{html.escape(empty)}</li>"
    rows = []
    for h in items[:20]:
        title = html.escape(str(h.get("title") or h.get("text") or "—"))
        source = html.escape(str(h.get("source") or ""))
        when = html.escape(str(h.get("time") or ""))
        prefix = f"{when} " if when else ""
        tag = f' <span class="ext-kind">{source}</span>' if source else ""
        rows.append(f"<li>{prefix}{title}{tag}</li>")
    return "".join(rows)


def _render_calendar_rows(payload: dict[str, Any]) -> str:
    events = payload.get("calendar_events")
    if events is None:
        events = []
    if events:
        return "".join(
            f'<div class="cal-item">{html.escape(str(e.get("time", "")))} '
            f'{e.get("flag", "")} {html.escape(str(e.get("event", "")))}</div>'
            for e in events[:24]
        )
    risk = str(payload.get("risk_events") or "—")
    if risk != "—":
        parsed = parse_risk_events_calendar(risk)
        if parsed:
            return "".join(
                f'<div class="cal-item">{html.escape(str(e.get("time", "")))} '
                f'{e.get("flag", "")} {html.escape(str(e.get("event", "")))}</div>'
                for e in parsed[:24]
            )
        return f'<div class="cal-item">{html.escape(risk)}</div>'
    count = payload.get("calendar_count")
    if count == 0 or risk in ("—", "", "-"):
        return '<div class="cal-item">今日暂无已确认宏观日历事件</div>'
    return '<div class="cal-item">—</div>'


def render_external_data_content(payload: dict[str, Any]) -> None:
    """Render external feed panels from fetch snapshot or full report payload."""
    sources = payload.get("sources") or []
    src_html = _source_tags(sources if isinstance(sources, list) else [])

    headlines = payload.get("headlines") or []
    flash = payload.get("flash_headlines") or []
    articles = payload.get("article_headlines") or []
    legacy_headlines = payload.get("news_headlines") or []

    if headlines:
        flash_html = _render_headline_list(flash, empty="暂无快讯")
        article_html = _render_headline_list(articles, empty="暂无资讯")
    else:
        legacy_li = "".join(f"<li>{html.escape(str(h))}</li>" for h in legacy_headlines[:20]) or "<li>暂无匹配头条</li>"
        flash_html = legacy_li
        article_html = "<li>暂无结构化资讯</li>"

    cal_rows = _render_calendar_rows(payload)
    social = html.escape(str(payload.get("social_sentiment") or "—"))
    posts = payload.get("social_posts") or []
    social_html = "".join(
        f'<li><span class="ext-kind">{html.escape(str(p.get("kind", "ideas")))}</span> '
        f'{html.escape(str(p.get("author") or "—"))}: '
        f'{html.escape(str(p.get("title") or "")[:120])}'
        f'{" · 👍" + str(p.get("likes")) if p.get("likes") else ""}</li>'
        for p in posts[:8]
    ) or "<li>暂无 TV 社区样本</li>"

    dxy = html.escape(str(payload.get("dxy_impact") or "—"))
    bars = payload.get("bars") or {}
    bars_txt = " · ".join(f"{tf} {n}根" for tf, n in sorted(bars.items(), key=lambda x: x[0])) or "—"
    data_source = html.escape(str(payload.get("data_source") or "—"))

    macro = payload.get("macro_quotes") or []
    macro_html = ""
    if macro:
        macro_rows = "".join(
            f"<li><b>{html.escape(str(m.get('symbol', m.get('name', '—'))))}</b> "
            f"{m.get('close', '—')} ({m.get('change_pct', '—')}%) · {html.escape(str(m.get('impact', '')))}</li>"
            for m in macro
        )
        macro_html = f'<div class="panel-box"><h4>宏观报价</h4><ul class="bullet-list">{macro_rows}</ul></div>'

    derived_bits = []
    if payload.get("spot_cross_check"):
        derived_bits.append(
            f"<p><b>Spot 交叉校验</b>：{html.escape(str(payload['spot_cross_check']))}</p>"
        )
    if payload.get("jin10_kline_summary"):
        derived_bits.append(
            f"<p><b>金十 K 线摘要</b>：{html.escape(str(payload['jin10_kline_summary']))}</p>"
        )
    if payload.get("news_topics"):
        topics = payload["news_topics"]
        if isinstance(topics, list) and topics:
            derived_bits.append(
                "<p><b>新闻主题</b>：" + " · ".join(html.escape(str(t)) for t in topics[:8]) + "</p>"
            )
    derived_html = ""
    if derived_bits:
        derived_html = f'<div class="panel-box span-2"><h4>二次加工摘要</h4>{"".join(derived_bits)}</div>'

    errors = payload.get("fetch_errors") or []
    err_html = ""
    if isinstance(errors, list) and errors:
        err_html = (
            '<p class="lbl" style="color:#b45309;margin-top:8px">拉取提示：'
            + html.escape("；".join(str(e) for e in errors[:3]))
            + "</p>"
        )

    phase = payload.get("phase", "fetch")
    phase_note = "数据拉取完成" if phase == "fetch" else "完整报告已生成（含二次加工摘要）"

    st.markdown(
        f"""
<div class="section-card external-feed">
  <h3>外部数据 · {phase_note} {src_html}</h3>
  <p class="report-meta">数据源：{data_source} · K 线：{bars_txt}</p>
  <div class="ext-grid">
    <div class="panel-box"><h4>美元指数 DXY</h4><p>{dxy}</p></div>
    <div class="panel-box"><h4>TV 社区情绪</h4><p>{social}</p><ul class="bullet-list">{social_html}</ul></div>
    {macro_html}
    <div class="panel-box span-2"><h4>金十快讯</h4><ul class="bullet-list">{flash_html}</ul></div>
    <div class="panel-box span-2"><h4>金十资讯</h4><ul class="bullet-list">{article_html}</ul></div>
    <div class="panel-box span-2"><h4>经济日历 / 事件风险</h4>{cal_rows}</div>
    {derived_html}
  </div>
  {err_html}
</div>
""",
        unsafe_allow_html=True,
    )


def render_external_data_page(payload: dict[str, Any]) -> None:
    phase = payload.get("phase", "fetch")
    subtitle = (
        "新闻 · 日历 · DXY · 社媒 — 数据拉取完成后即可查看，无需等待报告生成"
        if phase == "fetch"
        else "新闻 · 日历 · DXY · 社媒 — 含二次加工摘要（校验 / 主题 / K线）"
    )
    render_page_hero("外部数据", subtitle)
    render_external_data_content(payload)
