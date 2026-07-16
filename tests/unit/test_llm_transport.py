"""LLM transport retry and stream error wrapping."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest
from requests.exceptions import ChunkedEncodingError

from src.agents.llm.base import stream_llm_json
from src.core.progress import ProgressReporter, reset_progress, set_progress
from src.llm.client import LLMClient, LLMClientError


def test_chat_stream_wraps_chunked_encoding() -> None:
    client = LLMClient(api_key="k", base_url="https://api.example.com/v1", model="m", timeout=5)
    resp = MagicMock()
    resp.status_code = 200
    resp.iter_lines.side_effect = ChunkedEncodingError("Response ended prematurely")

    with patch("src.llm.client.requests.post", return_value=resp):
        with pytest.raises(LLMClientError, match="流式读取失败"):
            list(client.chat_stream([{"role": "user", "content": "hi"}]))


def test_stream_llm_json_retries_transport(monkeypatch: pytest.MonkeyPatch) -> None:
    client = LLMClient(api_key="k", base_url="https://api.example.com/v1", model="m", timeout=5)
    calls = {"n": 0}

    def fake_stream(*_args, **_kwargs):
        calls["n"] += 1
        if calls["n"] < 3:
            raise LLMClientError("LLM 流式读取失败: broken")
        return '{"items": [], "confidence": 0.5, "summary": "ok"}'

    sleeps: list[float] = []
    monkeypatch.setattr("src.agents.llm.base._stream_once", lambda *a, **k: fake_stream())
    monkeypatch.setattr("src.agents.llm.base.time.sleep", lambda s: sleeps.append(s))

    reporter = ProgressReporter()
    token = set_progress(reporter)
    try:
        raw = stream_llm_json(
            client,
            [{"role": "user", "content": "x"}],
            stage="bullish",
            temperature=0.2,
            max_attempts=3,
        )
    finally:
        reset_progress(token)

    assert calls["n"] == 3
    assert sleeps == [1.0, 2.0]
    assert "confidence" in raw


def test_stream_llm_json_raises_after_exhausted_retries(monkeypatch: pytest.MonkeyPatch) -> None:
    client = LLMClient(api_key="k", base_url="https://api.example.com/v1", model="m", timeout=5)

    def always_fail(*_args, **_kwargs):
        raise LLMClientError("LLM 流式读取失败: down")

    monkeypatch.setattr("src.agents.llm.base._stream_once", always_fail)
    monkeypatch.setattr("src.agents.llm.base.time.sleep", lambda _s: None)

    reporter = ProgressReporter()
    token = set_progress(reporter)
    try:
        with pytest.raises(LLMClientError, match="down"):
            stream_llm_json(
                client,
                [{"role": "user", "content": "x"}],
                stage="bearish",
                max_attempts=3,
            )
    finally:
        reset_progress(token)
