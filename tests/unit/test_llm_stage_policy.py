"""Advice V2 LLM budget, retry and telemetry tests."""

from __future__ import annotations

import pytest

from src.llm.stage import run_llm_stage, stream_llm_json
from src.core.progress import ProgressReporter, reset_progress, set_progress
from src.llm.client import LLMClient, LLMClientError
from src.llm.stage_policy import apply_input_budget, build_routing_strategy, get_stage_policy


def test_routing_strategy_records_single_advisor_model(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("src.llm.stage_policy.LLM_MODEL", "m1")
    meta = build_routing_strategy()
    assert meta["model"] == "m1"
    assert meta["same_model_strategy"] is True
    assert "one optional" in meta["same_model_reason"]
    assert meta["policy_version"] == "advice-llm-v2"
    assert set(meta["stages"]) == {"advisor"}
    assert meta["stages"]["advisor"]["upgrade_enabled"] is False


def test_input_budget_hard_degrade_is_visible() -> None:
    policy = get_stage_policy("advisor")
    huge = "AUTH_KEEP_HEAD " + ("x" * (policy.input_chars_hard + 5_000)) + " AUTH_KEEP_TAIL"
    messages = [
        {"role": "system", "content": "system mandate"},
        {"role": "user", "content": huge},
    ]
    out, action, meta = apply_input_budget(messages, policy)
    assert action == "hard_degrade"
    assert "[BUDGET_TRUNCATED" in out[1]["content"]
    assert "AUTH_KEEP_HEAD" in out[1]["content"]
    assert "AUTH_KEEP_TAIL" in out[1]["content"]
    assert out[0]["content"] == "system mandate"
    assert meta["original_input_chars"] > policy.input_chars_hard
    assert meta["input_chars"] <= policy.input_chars_hard + 500


def test_unified_budget_caps_transport_and_json_retries(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("src.config.LLM_MAX_RETRIES", 2)
    monkeypatch.setattr("src.llm.stage_policy.LLM_MAX_RETRIES", 2)
    policy = get_stage_policy("advisor")
    assert policy.max_attempts == 3

    client = LLMClient(api_key="k", base_url="https://api.example.com/v1", model="m", timeout=5)
    calls = {"n": 0}

    def fake_stream(*_args, **_kwargs):
        calls["n"] += 1
        if calls["n"] == 1:
            raise LLMClientError("transport down")
        if calls["n"] == 2:
            return "not-json{{{"
        return '{"items": [], "confidence": 0.5, "summary": "ok"}'

    monkeypatch.setattr("src.llm.stage._stream_once", fake_stream)
    monkeypatch.setattr("src.llm.stage.time.sleep", lambda _seconds: None)

    reporter = ProgressReporter()
    token = set_progress(reporter)
    try:
        result, trace = run_llm_stage(
            stage="advisor",
            model="m",
            client=client,
            messages=[{"role": "user", "content": "x"}],
            parse=lambda data: data,
        )
    finally:
        reset_progress(token)

    assert result is not None
    assert calls["n"] == 3
    assert trace.attempts == 3
    assert [row["reason"] for row in trace.attempt_log] == ["transport", "json_schema"]
    record = reporter.llm_io_snapshot()[-1]
    assert record["attempt"] == 3
    assert record["tier"] == "advisor"
    assert record["policy_version"] == "advice-llm-v2"


def test_exhausted_unified_budget_records_reasons(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("src.config.LLM_MAX_RETRIES", 1)
    monkeypatch.setattr("src.llm.stage_policy.LLM_MAX_RETRIES", 1)
    client = LLMClient(api_key="k", base_url="https://api.example.com/v1", model="m", timeout=5)
    calls = {"n": 0}

    def always_fail(*_args, **_kwargs):
        calls["n"] += 1
        raise LLMClientError("down")

    monkeypatch.setattr("src.llm.stage._stream_once", always_fail)
    monkeypatch.setattr("src.llm.stage.time.sleep", lambda _seconds: None)
    reporter = ProgressReporter()
    token = set_progress(reporter)
    try:
        result, trace = run_llm_stage(
            stage="advisor",
            model="m",
            client=client,
            messages=[{"role": "user", "content": "levels"}],
            parse=lambda data: data,
        )
    finally:
        reset_progress(token)

    assert result is None
    assert calls["n"] == 2
    assert trace.error
    assert all(row["reason"] == "transport" for row in trace.attempt_log)
    assert reporter.llm_io_snapshot()[-1]["tier"] == "advisor"


def test_stream_llm_json_respects_explicit_max_attempts(monkeypatch: pytest.MonkeyPatch) -> None:
    client = LLMClient(api_key="k", base_url="https://api.example.com/v1", model="m", timeout=5)
    calls = {"n": 0}

    def fail(*_args, **_kwargs):
        calls["n"] += 1
        raise LLMClientError("down")

    monkeypatch.setattr("src.llm.stage._stream_once", fail)
    monkeypatch.setattr("src.llm.stage.time.sleep", lambda _seconds: None)
    with pytest.raises(LLMClientError):
        stream_llm_json(
            client,
            [{"role": "user", "content": "x"}],
            stage="advisor",
            max_attempts=2,
        )
    assert calls["n"] == 2
