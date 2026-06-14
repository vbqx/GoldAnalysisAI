"""Stage source label tests — hybrid research display."""
from __future__ import annotations

from src.viz.source_labels import llm_was_invoked, stage_meta_label


def test_hybrid_rule_fallback_shows_mixed_label() -> None:
    meta = {
        "source": "hybrid",
        "fallback_reason": "采用规则输出：confidence 0.55 < 0.65",
        "llm": {"model": "deepseek-ai/DeepSeek-V4-Pro", "latency_ms": 12000},
    }
    assert stage_meta_label(meta) == "混合·规则"
    assert llm_was_invoked(meta)


def test_hybrid_llm_output_label() -> None:
    meta = {"source": "hybrid", "llm": {"model": "gpt-4o", "latency_ms": 800}}
    assert stage_meta_label(meta) == "混合·LLM"


def test_pure_rule_no_llm() -> None:
    meta = {"source": "rule"}
    assert stage_meta_label(meta) == "规则"
    assert not llm_was_invoked(meta)


def test_llm_mode_failure_fallback() -> None:
    meta = {"source": "rule", "fallback_reason": "timeout", "llm": {"error": "timeout"}}
    assert stage_meta_label(meta) == "规则·LLM失败回退"
    assert llm_was_invoked(meta)
