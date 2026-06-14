"""LLM display helpers — model names, latency, record dedupe."""

from __future__ import annotations

from src.config import short_model_name


def format_latency_ms(ms: int | None) -> str:
    if not ms:
        return "—"
    if ms >= 1000:
        return f"{ms / 1000:.1f}s"
    return f"{ms}ms"


def dedupe_llm_io_records(records: list[dict]) -> list[dict]:
    """Keep the latest record per stage (JSON retries append duplicates)."""
    order: list[str] = []
    by_stage: dict[str, dict] = {}
    for rec in records:
        stage = rec.get("stage") or ""
        if stage not in by_stage:
            order.append(stage)
        by_stage[stage] = rec
    return [by_stage[s] for s in order if s in by_stage]


def merge_llm_io_with_stage_sources(records: list[dict], stage_sources: dict) -> list[dict]:
    """Prefer orchestrator trace model/latency (total wall time) over per-attempt stream timing."""
    merged: list[dict] = []
    for rec in dedupe_llm_io_records(records):
        stage = rec.get("stage")
        trace = (stage_sources.get(stage) or {}).get("llm") or {}
        item = dict(rec)
        if trace.get("model"):
            item["model"] = trace["model"]
        if trace.get("latency_ms"):
            item["latency_ms"] = trace["latency_ms"]
        merged.append(item)
    return merged


def stage_llm_caption(stage_sources: dict, stage: str) -> str:
    trace = (stage_sources.get(stage) or {}).get("llm") or {}
    if not trace:
        return ""
    model = short_model_name(trace.get("model", ""))
    latency = format_latency_ms(trace.get("latency_ms"))
    return f"模型 `{model}` · {latency}"
