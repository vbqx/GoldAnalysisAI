"""Human-readable summaries for LLM stage outputs (Advice V2 advisor + generic JSON)."""

from __future__ import annotations

import json
from html import escape
from typing import Any


def _try_parse_json(raw: str) -> dict[str, Any] | None:
    text = (raw or "").strip()
    if not text:
        return None
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return None
    return data if isinstance(data, dict) else None


def _bullet_list(items: list[Any], *, limit: int = 8) -> str:
    rows = [f"<li>{escape(str(item))}</li>" for item in items[:limit] if str(item).strip()]
    return f"<ul>{''.join(rows)}</ul>" if rows else ""


def _fmt_advisor_wording(data: dict[str, Any]) -> str:
    parts = [f"<p><b>摘要</b> {escape(str(data.get('summary') or '—'))}</p>"]
    for key, title in (
        ("market_context", "市场背景"),
        ("rationale", "理由"),
        ("confirmation_checklist", "人工确认清单"),
        ("risks", "风险"),
        ("uncertainties", "不确定性"),
    ):
        block = _bullet_list(list(data.get(key) or []))
        if block:
            parts.append(f"<p><b>{title}</b></p>{block}")
    return "\n".join(parts)


def _fmt_generic(data: dict[str, Any]) -> str:
    preview = escape(json.dumps(data, ensure_ascii=False, indent=2)[:2400])
    return f"<pre>{preview}</pre>"


def format_llm_narrative(stage: str, raw: str) -> str:
    """Return HTML for the human-readable summary box under each I/O record."""
    if not (raw or "").strip():
        return "<p><i>等待模型输出…</i></p>"

    data = _try_parse_json(raw)
    if data is None:
        preview = escape(raw[:800])
        suffix = "…" if len(raw) > 800 else ""
        return f"<p><i>输出尚未形成完整 JSON，当前片段：</i></p><p>{preview}{suffix}</p>"

    if stage == "advisor":
        body = _fmt_advisor_wording(data)
    else:
        body = _fmt_generic(data)

    return f'<div class="llm-narrative-box">{body}</div>'
