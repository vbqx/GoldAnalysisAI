"""LLM client connect/read timeout configuration."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest
from requests.exceptions import Timeout

from src.llm.client import LLMClient, LLMClientError


def test_explicit_connect_and_read_timeouts() -> None:
    client = LLMClient(
        api_key="k",
        base_url="https://api.example.com/v1",
        model="m",
        connect_timeout=7.5,
        read_timeout=99.0,
    )
    assert client.connect_timeout == 7.5
    assert client.read_timeout == 99.0
    assert client.timeout == 99.0
    assert client._request_timeout() == (7.5, 99.0)


def test_legacy_timeout_sets_both() -> None:
    client = LLMClient(api_key="k", base_url="https://api.example.com/v1", model="m", timeout=45)
    assert client.connect_timeout == 30.0
    assert client.read_timeout == 45.0


def test_post_uses_connect_read_tuple() -> None:
    client = LLMClient(
        api_key="k",
        base_url="https://api.example.com/v1",
        model="m",
        connect_timeout=5.0,
        read_timeout=15.0,
    )
    resp = MagicMock()
    resp.status_code = 200
    resp.iter_lines.return_value = iter([])

    with patch("src.llm.client.requests.post", return_value=resp) as post:
        list(client.chat_stream([{"role": "user", "content": "hi"}]))

    _, kwargs = post.call_args
    assert kwargs["timeout"] == (5.0, 15.0)


def test_connect_timeout_error_message() -> None:
    client = LLMClient(
        api_key="k",
        base_url="https://api.example.com/v1",
        model="m",
        connect_timeout=3.0,
        read_timeout=10.0,
    )
    with patch("src.llm.client.requests.post", side_effect=Timeout("connect")):
        with pytest.raises(LLMClientError, match="connect=3.0s.*read_idle=10.0s"):
            list(client.chat_stream([{"role": "user", "content": "hi"}]))


def test_max_retries_from_config(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("src.config.LLM_MAX_RETRIES", 4)
    monkeypatch.setattr("src.llm.stage_policy.LLM_MAX_RETRIES", 4)
    from src.llm.stage_policy import get_stage_policy

    assert get_stage_policy("bullish").max_attempts == 5  # 1 + LLM_MAX_RETRIES
