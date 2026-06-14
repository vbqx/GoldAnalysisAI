"""Source badge helpers — label rule vs LLM outputs."""

from __future__ import annotations

from src.config import short_model_name

STAGE_LABELS = {
    "bullish": "看多研究",
    "bearish": "看空研究",
    "debate": "辩论共识",
    "trader": "交易员",
    "risk": "风控",
    "manager": "经理",
}

SOURCE_LABELS = {
    "rule": "规则",
    "llm": "LLM",
    "hybrid": "LLM",
}

MODE_LABELS = {
    "rule": "规则",
    "llm": "LLM",
    "hybrid": "混合",
}


def is_llm_source(source: str | None) -> bool:
    return source in ("llm", "hybrid")


def llm_was_invoked(meta: dict) -> bool:
    """True if an LLM call was made for this stage (even when rule output was chosen)."""
    source = meta.get("source") or "rule"
    if source in ("llm", "hybrid"):
        return True
    llm = meta.get("llm") or {}
    return bool(llm.get("model") or llm.get("latency_ms") or llm.get("error"))


def stage_meta_label(meta: dict) -> str:
    """Human label for a stage_sources / stage_meta entry."""
    source = meta.get("source") or "rule"
    llm = meta.get("llm") or {}
    fallback = (meta.get("fallback_reason") or "").strip()

    if source == "hybrid":
        return "混合·规则" if fallback else "混合·LLM"
    if source == "llm":
        return "LLM"
    if source == "rule" and llm_was_invoked(meta):
        return "规则·LLM失败回退" if llm.get("error") else "规则"
    return "规则"


def source_label(source: str | None) -> str:
    return SOURCE_LABELS.get(source or "rule", "规则")


def stage_source(report: dict, stage: str) -> str:
    meta = (report.get("meta") or {}).get("stage_sources") or {}
    entry = meta.get(stage) or {}
    return entry.get("source", "rule")


def render_source_badge(source: str | None, *, small: bool = False) -> str:
    label = source_label(source)
    cls = "src-badge llm" if is_llm_source(source) else "src-badge rule"
    if small:
        cls += " sm"
    return f'<span class="{cls}">{label}</span>'


def render_stage_meta_badge(meta: dict, *, small: bool = False) -> str:
    label = stage_meta_label(meta)
    cls = "src-badge llm" if llm_was_invoked(meta) else "src-badge rule"
    if small:
        cls += " sm"
    return f'<span class="{cls}">{label}</span>'


def render_agent_source_banner(report: dict) -> str:
    """Horizontal strip showing each pipeline stage source."""
    meta = report.get("meta") or {}
    sources = meta.get("stage_sources") or {}
    mode = meta.get("agent_mode", "rule")
    mode_label = MODE_LABELS.get(mode, mode)

    if not sources and mode == "rule":
        return (
            '<div class="agent-source-bar">'
            f'<span class="agent-mode-tag">模式：{mode_label}</span>'
            '<span class="src-badge rule">全流程规则引擎</span>'
            "</div>"
        )

    chips = [f'<span class="agent-mode-tag">模式：{mode_label}</span>']
    for key in ("bullish", "bearish", "debate", "trader", "risk", "manager"):
        if key not in sources:
            continue
        entry = sources[key]
        name = STAGE_LABELS.get(key, key)
        llm = entry.get("llm") or {}
        model_hint = ""
        if llm.get("model") and llm_was_invoked(entry):
            model_hint = f' <span class="stage-model">{short_model_name(llm["model"])}</span>'
        chips.append(
            f'<span class="stage-chip">'
            f"{name}{render_stage_meta_badge(entry, small=True)}{model_hint}"
            f"</span>"
        )

    llm = report.get("llm_analysis") or {}
    if llm.get("enabled") and not llm.get("error"):
        chips.append(f'<span class="stage-chip">报告文案{render_source_badge("llm", small=True)}</span>')

    return f'<div class="agent-source-bar">{"".join(chips)}</div>'
