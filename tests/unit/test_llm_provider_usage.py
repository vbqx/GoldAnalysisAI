"""Issue #37 — persist provider usage from SSE when available; never invent zeros."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from src.agents.llm.base import run_llm_stage
from src.analysis.audit_summary import build_audit_summary
from src.core.progress import ProgressReporter, reset_progress, set_progress
from src.llm.client import LLMClient, normalize_provider_usage


def test_normalize_provider_usage_openai_shape() -> None:
    assert normalize_provider_usage(
        {"prompt_tokens": 10, "completion_tokens": 4, "total_tokens": 14}
    ) == {"prompt_tokens": 10, "completion_tokens": 4, "total_tokens": 14}


def test_normalize_provider_usage_input_output_aliases() -> None:
    assert normalize_provider_usage({"input_tokens": 8, "output_tokens": 2}) == {
        "prompt_tokens": 8,
        "completion_tokens": 2,
        "total_tokens": 10,
    }


def test_normalize_provider_usage_rejects_empty() -> None:
    assert normalize_provider_usage(None) is None
    assert normalize_provider_usage({}) is None
    assert normalize_provider_usage("x") is None


def test_chat_stream_captures_usage_from_final_chunk() -> None:
    client = LLMClient(api_key="k", base_url="https://api.example.com/v1", model="m", timeout=5)
    lines = [
        b'data: {"choices":[{"delta":{"content":"hello"}}]}',
        b'data: {"choices":[],"usage":{"prompt_tokens":100,"completion_tokens":20,"total_tokens":120}}',
        b"data: [DONE]",
    ]
    resp = MagicMock()
    resp.status_code = 200
    resp.iter_lines.return_value = iter(lines)

    with patch("src.llm.client.requests.post", return_value=resp) as post:
        text = "".join(client.chat_stream([{"role": "user", "content": "hi"}]))

    assert text == "hello"
    assert client.last_usage == {
        "prompt_tokens": 100,
        "completion_tokens": 20,
        "total_tokens": 120,
    }
    payload = post.call_args.kwargs["json"]
    assert payload["stream"] is True
    assert payload["stream_options"] == {"include_usage": True}


def test_chat_stream_usage_stays_none_when_provider_omits(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr("src.config.LLM_STREAM_INCLUDE_USAGE", False)
    client = LLMClient(api_key="k", base_url="https://api.example.com/v1", model="m", timeout=5)
    resp = MagicMock()
    resp.status_code = 200
    resp.iter_lines.return_value = iter(
        [b'data: {"choices":[{"delta":{"content":"hi"}}]}', b"data: [DONE]"]
    )

    with patch("src.llm.client.requests.post", return_value=resp) as post:
        assert "".join(client.chat_stream([{"role": "user", "content": "x"}])) == "hi"

    assert client.last_usage is None
    assert "stream_options" not in post.call_args.kwargs["json"]


def test_run_llm_stage_persists_provider_usage(monkeypatch: pytest.MonkeyPatch) -> None:
    client = LLMClient(api_key="k", base_url="https://api.example.com/v1", model="m", timeout=5)

    def fake_stream(*_a, **_k):
        client.last_usage = {
            "prompt_tokens": 50,
            "completion_tokens": 10,
            "total_tokens": 60,
        }
        return '{"items": [], "confidence": 0.5, "summary": "ok"}'

    monkeypatch.setattr("src.agents.llm.base._stream_once", fake_stream)

    reporter = ProgressReporter()
    token = set_progress(reporter)
    try:
        result, trace = run_llm_stage(
            stage="bullish",
            model="m",
            client=client,
            messages=[{"role": "user", "content": "x"}],
            parse=lambda d: d,
        )
    finally:
        reset_progress(token)

    assert result is not None
    assert trace.usage == {"prompt_tokens": 50, "completion_tokens": 10, "total_tokens": 60}
    rec = reporter.llm_io_snapshot()[-1]
    assert rec["usage"] == trace.usage
    assert rec["attempts"] == []  # auditable empty retry log on first-pass success


def test_json_retry_then_success_keeps_attempt_reasons_and_final_usage(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr("src.config.LLM_MAX_RETRIES", 2)
    monkeypatch.setattr("src.llm.stage_policy.LLM_MAX_RETRIES", 2)
    client = LLMClient(api_key="k", base_url="https://api.example.com/v1", model="m", timeout=5)
    calls = {"n": 0}

    def fake_stream(*_a, **_k):
        calls["n"] += 1
        if calls["n"] == 1:
            client.last_usage = {"prompt_tokens": 11, "completion_tokens": 1, "total_tokens": 12}
            return "not-json"
        client.last_usage = {"prompt_tokens": 22, "completion_tokens": 3, "total_tokens": 25}
        return '{"summary": "ok", "confidence": 0.4}'

    monkeypatch.setattr("src.agents.llm.base._stream_once", fake_stream)
    monkeypatch.setattr("src.agents.llm.base.time.sleep", lambda _s: None)

    reporter = ProgressReporter()
    token = set_progress(reporter)
    try:
        result, trace = run_llm_stage(
            stage="news",
            model="m",
            client=client,
            messages=[{"role": "user", "content": "x"}],
            parse=lambda d: d,
        )
    finally:
        reset_progress(token)

    assert result is not None
    assert calls["n"] == 2
    assert [a["reason"] for a in trace.attempt_log] == ["json_schema"]
    assert trace.usage == {"prompt_tokens": 22, "completion_tokens": 3, "total_tokens": 25}
    rec = reporter.llm_io_snapshot()[-1]
    assert rec["attempts"][0]["reason"] == "json_schema"
    assert rec["usage"] == trace.usage


def test_audit_summary_aggregates_provider_tokens() -> None:
    report = {
        "meta": {
            "llm_io": [
                {
                    "stage": "technical",
                    "kind": "llm",
                    "attempt": 1,
                    "attempts": [],
                    "input_chars": 100,
                    "output_chars": 20,
                    "usage": {
                        "prompt_tokens": 40,
                        "completion_tokens": 5,
                        "total_tokens": 45,
                    },
                },
                {
                    "stage": "news",
                    "kind": "llm",
                    "attempt": 2,
                    "attempts": [{"attempt": 1, "reason": "transport"}],
                    "input_chars": 200,
                    "output_chars": 30,
                    "usage": {
                        "prompt_tokens": 80,
                        "completion_tokens": 10,
                        "total_tokens": 90,
                    },
                },
            ],
            "llm_routing": {"policy_version": "llm-stage-v1"},
        },
        "signals": [],
    }
    summary = build_audit_summary(report)
    usage = summary["llm_usage_summary"]
    assert usage["provider_usage_available"] is True
    assert usage["provider_usage_stage_count"] == 2
    assert usage["provider_prompt_tokens"] == 120
    assert usage["provider_completion_tokens"] == 15
    assert usage["provider_total_tokens"] == 135
    assert usage["retry_reasons"] == [
        {"stage": "news", "attempt": 1, "reason": "transport"}
    ]
