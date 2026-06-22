"""Live LLM streaming panel helpers."""

from __future__ import annotations

from src.viz.pipeline_progress import is_streaming_llm_record, partition_llm_records_for_live


def test_is_streaming_llm_record() -> None:
    assert is_streaming_llm_record(
        {"stage": "bullish", "model": "qwen", "latency_ms": None, "kind": "llm"}
    )
    assert not is_streaming_llm_record(
        {"stage": "bullish", "model": "qwen", "latency_ms": 120, "kind": "llm"}
    )
    assert not is_streaming_llm_record(
        {"stage": "analyst_team", "model": "规则引擎", "latency_ms": None, "kind": "rule"}
    )
    assert not is_streaming_llm_record(
        {"stage": "debate", "model": "qwen", "latency_ms": None, "error": "timeout", "kind": "llm"}
    )


def test_partition_llm_records_for_live() -> None:
    records = [
        {"stage": "analyst_team", "model": "规则引擎", "kind": "rule", "latency_ms": 10},
        {"stage": "technical", "model": "fast", "kind": "llm", "latency_ms": None, "output": "{"},
        {"stage": "fundamentals", "model": "fast", "kind": "llm", "latency_ms": 50, "output": "{}"},
        {"stage": "news", "model": "fast", "kind": "llm", "latency_ms": None, "output": ""},
    ]
    active, completed = partition_llm_records_for_live(records)
    assert {r["stage"] for r in active} == {"technical", "news"}
    # analyst_team rule row is hidden when parallel analyst LLM rows exist
    assert {r["stage"] for r in completed} == {"fundamentals"}
