"""Issue #37 — stage policy, unified retry budget, and telemetry."""

from __future__ import annotations

import json
from unittest.mock import MagicMock

import pytest

from src.agents.llm.base import run_llm_stage, stream_llm_json
from src.core.progress import ProgressReporter, reset_progress, set_progress
from src.llm.client import LLMClient, LLMClientError
from src.llm.stage_policy import (
    apply_input_budget,
    build_routing_strategy,
    get_stage_policy,
)


def test_routing_strategy_records_same_model(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("src.llm.stage_policy.LLM_MODEL_FAST", "m1")
    monkeypatch.setattr("src.llm.stage_policy.LLM_MODEL_STRONG", "m1")
    monkeypatch.setattr("src.llm.stage_policy.LLM_MODEL", "m1")
    meta = build_routing_strategy()
    assert meta["same_model_strategy"] is True
    assert "identical" in meta["same_model_reason"].lower() or "同" in meta["same_model_reason"] or "identical" in meta["same_model_reason"]
    assert meta["policy_version"] == "llm-stage-v1"
    assert "llm_levels" in meta["stages"]
    assert meta["stages"]["risk"]["upgrade_enabled"] is False


def test_input_budget_hard_degrade_is_visible() -> None:
    policy = get_stage_policy("llm_narrative")
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
    """Transport + JSON failures share one budget — never nested 3×3."""
    monkeypatch.setattr("src.config.LLM_MAX_RETRIES", 2)
    monkeypatch.setattr("src.llm.stage_policy.LLM_MAX_RETRIES", 2)
    policy = get_stage_policy("bullish")
    assert policy.max_attempts == 3

    client = LLMClient(api_key="k", base_url="https://api.example.com/v1", model="m", timeout=5)
    calls = {"n": 0}

    def fake_stream(*_a, **_k):
        calls["n"] += 1
        if calls["n"] == 1:
            raise LLMClientError("transport down")
        if calls["n"] == 2:
            return "not-json{{{"
        return '{"items": [], "confidence": 0.5, "summary": "ok"}'

    monkeypatch.setattr("src.agents.llm.base._stream_once", lambda *a, **k: fake_stream())
    monkeypatch.setattr("src.agents.llm.base.time.sleep", lambda _s: None)

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
    assert calls["n"] == 3  # exactly policy.max_attempts, not 9
    assert trace.attempts == 3
    assert [a["reason"] for a in trace.attempt_log] == ["transport", "json_schema"]
    io = reporter.llm_io_snapshot()
    assert len([r for r in io if r["stage"] == "bullish"]) == 1
    rec = io[-1]
    assert rec["attempt"] == 3
    assert len(rec["attempts"]) == 2
    assert rec["attempts"][0]["reason"] == "transport"
    assert rec["attempts"][1]["reason"] == "json_schema"
    assert rec["input_chars"] is not None
    assert rec["input_tokens_est"] is not None
    assert rec["tier"] == "fast"
    assert rec["policy_version"] == "llm-stage-v1"


def test_exhausted_unified_budget_records_reasons(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("src.config.LLM_MAX_RETRIES", 1)
    monkeypatch.setattr("src.llm.stage_policy.LLM_MAX_RETRIES", 1)
    client = LLMClient(api_key="k", base_url="https://api.example.com/v1", model="m", timeout=5)
    calls = {"n": 0}

    def always_fail(*_a, **_k):
        calls["n"] += 1
        raise LLMClientError("down")

    monkeypatch.setattr("src.agents.llm.base._stream_once", always_fail)
    monkeypatch.setattr("src.agents.llm.base.time.sleep", lambda _s: None)

    reporter = ProgressReporter()
    token = set_progress(reporter)
    try:
        result, trace = run_llm_stage(
            stage="llm_levels",
            model="m",
            client=client,
            messages=[{"role": "user", "content": "levels"}],
            parse=lambda d: d,
        )
    finally:
        reset_progress(token)

    assert result is None
    assert calls["n"] == 2  # 1 + LLM_MAX_RETRIES
    assert trace.error
    assert len(trace.attempt_log) == 2
    assert all(a["reason"] == "transport" for a in trace.attempt_log)
    rec = reporter.llm_io_snapshot()[-1]
    assert rec["error"]
    assert rec["tier"] == "strong"


def test_stream_llm_json_respects_explicit_max_attempts(monkeypatch: pytest.MonkeyPatch) -> None:
    client = LLMClient(api_key="k", base_url="https://api.example.com/v1", model="m", timeout=5)
    calls = {"n": 0}

    def fail(*_a, **_k):
        calls["n"] += 1
        raise LLMClientError("down")

    monkeypatch.setattr("src.agents.llm.base._stream_once", fail)
    monkeypatch.setattr("src.agents.llm.base.time.sleep", lambda _s: None)

    with pytest.raises(LLMClientError):
        stream_llm_json(
            client,
            [{"role": "user", "content": "x"}],
            stage="bearish",
            max_attempts=2,
        )
    assert calls["n"] == 2


def test_audit_summary_includes_llm_usage(monkeypatch: pytest.MonkeyPatch) -> None:
    from src.analysis.audit_summary import build_audit_summary

    report = {
        "meta": {
            "llm_io": [
                {
                    "stage": "bullish",
                    "kind": "llm",
                    "latency_ms": 70_000,
                    "input_chars": 1000,
                    "output_chars": 200,
                    "attempt": 2,
                    "attempts": [{"attempt": 1, "reason": "transport"}],
                    "budget_action": "soft_warn",
                    "usage": None,
                }
            ],
            "llm_routing": {"same_model_strategy": True, "policy_version": "llm-stage-v1"},
        },
        "signals": [],
    }
    summary = build_audit_summary(report)
    assert summary["llm_routing"]["same_model_strategy"] is True
    assert summary["llm_usage_summary"]["input_chars"] == 1000
    assert summary["llm_usage_summary"]["total_attempts"] == 2
    assert summary["llm_usage_summary"]["budget_actions"]["bullish"] == "soft_warn"
    assert summary["llm_usage_summary"]["provider_usage_available"] is False
