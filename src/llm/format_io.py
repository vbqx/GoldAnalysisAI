"""Format LLM messages for display."""

from __future__ import annotations

import json
from typing import Any


def format_llm_output(text: str) -> str:
    """Pretty-print JSON output; preserve UTF-8 Chinese."""
    text = text.strip()
    if not text:
        return ""
    try:
        return json.dumps(json.loads(text), ensure_ascii=False, indent=2)
    except json.JSONDecodeError:
        return text


def format_messages(messages: list[dict[str, str]], *, max_chars: int = 12000) -> str:
    lines: list[str] = []
    for msg in messages:
        role = msg.get("role", "unknown")
        content = (msg.get("content") or "").strip()
        lines.append(f"[{role}]\n{content}")
    text = "\n\n".join(lines)
    if len(text) > max_chars:
        return text[:max_chars] + f"\n\n…（已截断，共 {len(text)} 字符）"
    return text


def messages_to_dict(messages: list[dict[str, str]]) -> list[dict[str, Any]]:
    return [{"role": m.get("role", ""), "content": m.get("content", "")} for m in messages]
