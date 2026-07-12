"""Unit tests for lightweight live progress UI during report generation."""

from __future__ import annotations

from src.viz.generation_worker import compact_llm_io_for_live


def test_compact_llm_io_strips_streaming_payload() -> None:
    huge = "x" * 50_000
    records = [
        {
            "stage": "bearish",
            "label": "看空研究",
            "model": "deepseek-fast",
            "latency_ms": None,
            "output": huge,
            "messages": [{"role": "user", "content": "prompt " * 5000}],
        },
        {
            "stage": "bullish",
            "label": "看多研究",
            "model": "deepseek-fast",
            "latency_ms": 1200,
            "output": "done",
            "messages": [],
        },
    ]

    compact = compact_llm_io_for_live(records)

    assert compact[0]["output"] == ""
    assert compact[0]["messages"] == []
    assert compact[0]["stream_chars"] == 50_000
    assert compact[1]["output"] == "done"
    assert "stream_chars" not in compact[1]


def test_compact_llm_io_truncates_completed_output() -> None:
    records = [
        {
            "stage": "debate",
            "label": "辩论",
            "model": "deepseek-strong",
            "latency_ms": 8000,
            "output": "z" * 10_000,
            "messages": [],
        }
    ]

    compact = compact_llm_io_for_live(records)

    assert len(compact[0]["output"]) <= 6001
    assert compact[0]["output"].startswith("…")
