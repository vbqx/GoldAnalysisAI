"""Turn LLM JSON responses into readable Chinese summaries."""

from __future__ import annotations

import json
import re
from html import escape
from typing import Any

_BIAS_CN = {"bullish": "偏多", "bearish": "偏空", "neutral": "中性"}
_CATEGORY_CN = {
    "structure": "结构",
    "liquidity": "流动性",
    "external": "外部",
    "market": "行情",
}


def _try_parse_json(text: str) -> dict[str, Any] | None:
    text = text.strip()
    if not text:
        return None
    attempts = [text]
    start, end = text.find("{"), text.rfind("}")
    if start >= 0 and end > start:
        attempts.append(text[start : end + 1])
    for candidate in attempts:
        try:
            data = json.loads(candidate)
            if isinstance(data, dict):
                return data
        except json.JSONDecodeError:
            cleaned = re.sub(r",(\s*[}\]])", r"\1", candidate)
            try:
                data = json.loads(cleaned)
                if isinstance(data, dict):
                    return data
            except json.JSONDecodeError:
                continue
    return None


def _pct(v: Any) -> str:
    try:
        f = float(v)
    except (TypeError, ValueError):
        return "—"
    return f"{max(0.0, min(1.0, f)):.0%}"


def _lines_to_html(lines: list[str]) -> str:
    if not lines:
        return "<p>—</p>"
    return "".join(f"<li>{escape(line)}</li>" for line in lines)


def _fmt_evidence(direction: str, data: dict[str, Any]) -> str:
    summary = str(data.get("summary", "")).strip() or "（无总结）"
    confidence = _pct(data.get("confidence"))
    items = data.get("items") or []
    bullets: list[str] = []
    if isinstance(items, list):
        for row in items[:12]:
            if not isinstance(row, dict):
                continue
            s = str(row.get("summary", "")).strip()
            if not s:
                continue
            tf = row.get("timeframe")
            cat = _CATEGORY_CN.get(str(row.get("category", "")), str(row.get("category", "")))
            strength = _pct(row.get("strength"))
            prefix = f"[{tf}] " if tf else ""
            meta = f"（{cat} · 强度 {strength}）" if cat else f"（强度 {strength}）"
            bullets.append(f"{prefix}{s}{meta}")
    parts = [
        f"<p><b>{escape(direction)}研究总结</b>：{escape(summary)}</p>",
        f"<p><b>置信度</b>：{confidence}</p>",
    ]
    if bullets:
        parts.append(f"<p><b>主要证据</b></p><ul>{_lines_to_html(bullets)}</ul>")
    return "\n".join(parts)


def _fmt_debate(data: dict[str, Any]) -> str:
    bias = _BIAS_CN.get(str(data.get("consensus_bias", "")).lower(), "中性")
    strength = _pct(data.get("consensus_strength"))
    notes_raw = data.get("discussion_notes") or []
    notes = [str(n).strip() for n in notes_raw if str(n).strip()] if isinstance(notes_raw, list) else []
    dissent = str(data.get("dissent", "")).strip()
    parts = [
        f"<p><b>辩论共识</b>：{escape(bias)}（强度 {strength}）</p>",
    ]
    if notes:
        parts.append(f"<p><b>讨论要点</b></p><ul>{_lines_to_html(notes[:8])}</ul>")
    if dissent:
        parts.append(f"<p><b>分歧</b>：{escape(dissent)}</p>")
    return "\n".join(parts)


def _fmt_narrative(data: dict[str, Any]) -> str:
    parts: list[str] = []
    if v := str(data.get("market_summary", "")).strip():
        parts.append(f"<p><b>市场总览</b>：{escape(v)}</p>")
    if v := str(data.get("trade_thesis", "")).strip():
        parts.append(f"<p><b>交易逻辑</b>：{escape(v)}</p>")
    if v := str(data.get("action_plan", "")).strip():
        lines = [ln.strip() for ln in v.splitlines() if ln.strip()]
        parts.append(f"<p><b>操作建议</b></p><ul>{_lines_to_html(lines)}</ul>")
    watch = data.get("watch_levels") or []
    if isinstance(watch, list) and watch:
        levels = [str(w).strip() for w in watch if str(w).strip()]
        parts.append(f"<p><b>关注价位</b></p><ul>{_lines_to_html(levels)}</ul>")
    risks = data.get("risks") or []
    if isinstance(risks, list) and risks:
        risk_lines = [str(r).strip() for r in risks if str(r).strip()]
        parts.append(f"<p><b>风险提示</b></p><ul>{_lines_to_html(risk_lines)}</ul>")
    if "confidence" in data:
        parts.append(f"<p><b>置信度</b>：{_pct(data['confidence'])}</p>")
    return "\n".join(parts) if parts else "<p>（未能解析文案字段）</p>"


def _fmt_generic(data: dict[str, Any]) -> str:
    lines: list[str] = []
    for key, val in data.items():
        if isinstance(val, (dict, list)):
            continue
        text = str(val).strip()
        if text:
            lines.append(f"{key}：{text}")
    if not lines:
        return "<p>（无可用文本字段）</p>"
    return f"<ul>{_lines_to_html(lines[:10])}</ul>"


def _fmt_analyst_report(title: str, data: dict[str, Any]) -> str:
    """Single AnalystReport JSON (technical / fundamentals / news / sentiment)."""
    bias = _BIAS_CN.get(str(data.get("bias", "")).lower(), "中性")
    summary = str(data.get("summary", "")).strip() or "—"
    confidence = _pct(data.get("confidence"))
    items = data.get("items") or []
    bullets: list[str] = []
    if isinstance(items, list):
        for row in items[:8]:
            if not isinstance(row, dict):
                continue
            s = str(row.get("summary", "")).strip()
            if not s:
                continue
            tf = row.get("timeframe")
            cat = _CATEGORY_CN.get(str(row.get("category", "")), str(row.get("category", "")))
            strength = _pct(row.get("strength"))
            prefix = f"[{tf}] " if tf else ""
            meta = f"（{cat} · 强度 {strength}）" if cat else f"（强度 {strength}）"
            bullets.append(f"{prefix}{s}{meta}")
    parts = [
        f"<p><b>{escape(title)}</b>：{escape(bias)}（置信 {confidence}）</p>",
        f"<p>{escape(summary)}</p>",
    ]
    if bullets:
        parts.append(f"<p><b>主要证据</b></p><ul>{_lines_to_html(bullets)}</ul>")
    return "\n".join(parts)


_ANALYST_STAGE_TITLES = {
    "technical": "技术分析师",
    "fundamentals": "基本面分析师",
    "news": "新闻分析师",
    "sentiment": "情绪分析师",
}


def _fmt_analyst_team(data: dict[str, Any]) -> str:
    labels = {
        "technical": "技术分析师",
        "fundamentals": "基本面分析师",
        "news": "新闻分析师",
        "sentiment": "情绪分析师",
    }
    parts: list[str] = []
    for key, title in labels.items():
        report = data.get(key) or {}
        if not isinstance(report, dict):
            continue
        bias = _BIAS_CN.get(str(report.get("bias", "")).lower(), "中性")
        summary = str(report.get("summary", "")).strip() or "—"
        confidence = _pct(report.get("confidence"))
        items = report.get("items") or []
        count = len(items) if isinstance(items, list) else 0
        parts.append(
            f"<p><b>{escape(title)}</b>：{escape(bias)}（置信 {confidence}，{count} 条证据）"
            f"<br>{escape(summary)}</p>"
        )
    return "\n".join(parts) if parts else "<p>（无 Analyst Team 数据）</p>"


def _fmt_context(data: dict[str, Any]) -> str:
    price = data.get("price")
    source = str(data.get("source_label", "")).strip() or "—"
    ext = data.get("external") if isinstance(data.get("external"), dict) else {}
    headlines = ext.get("news_headlines") or []
    headline_count = len(headlines) if isinstance(headlines, list) else 0
    parts = [
        f"<p><b>现价</b> {escape(str(price))} · 来源 {escape(source)}</p>",
        f"<p><b>美元指数</b> {escape(str(ext.get('dxy_impact', '—')))}</p>",
        f"<p><b>事件风险</b> {escape(str(ext.get('risk_events', '—')))}</p>",
        f"<p><b>新闻头条</b> {headline_count} 条</p>",
        f"<p><b>社媒情绪</b> {escape(str(ext.get('social_sentiment', '—')))}</p>",
    ]
    if headline_count and isinstance(headlines, list):
        preview = headlines[:3]
        bullets = "".join(f"<li>{escape(str(h)[:120])}</li>" for h in preview)
        parts.append(f"<ul>{bullets}</ul>")
    return "\n".join(parts)


def format_llm_narrative(stage: str, raw: str) -> str:
    """Return HTML for the human-readable summary box."""
    if not raw.strip():
        return "<p><i>等待模型输出…</i></p>"

    data = _try_parse_json(raw)
    if data is None:
        preview = escape(raw[:800])
        suffix = "…" if len(raw) > 800 else ""
        return f"<p><i>输出尚未形成完整 JSON，当前片段：</i></p><p>{preview}{suffix}</p>"

    if stage == "bullish":
        body = _fmt_evidence("看多", data)
    elif stage == "bearish":
        body = _fmt_evidence("看空", data)
    elif stage == "debate":
        body = _fmt_debate(data)
    elif stage == "analyst_team":
        body = _fmt_analyst_team(data)
    elif stage == "context":
        body = _fmt_context(data)
    elif stage in _ANALYST_STAGE_TITLES:
        body = _fmt_analyst_report(_ANALYST_STAGE_TITLES[stage], data)
    elif stage in ("llm_narrative", "narrative"):
        body = _fmt_narrative(data)
    else:
        body = _fmt_generic(data)

    return f'<div class="llm-narrative-box">{body}</div>'
