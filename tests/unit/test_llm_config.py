"""LLM default provider configuration."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

from src.config import llm_provider_extra_payload
from src.llm.client import LLMClient


def test_llm_provider_extra_payload_auto_disables_deepseek_v4_thinking(
    monkeypatch,
) -> None:
    monkeypatch.delenv("LLM_THINKING", raising=False)
    assert llm_provider_extra_payload(model="deepseek-v4-flash") == {
        "thinking": {"type": "disabled"}
    }
    assert llm_provider_extra_payload(model="gpt-4o-mini") == {}


def test_llm_provider_extra_payload_respects_explicit_thinking(monkeypatch) -> None:
    monkeypatch.setenv("LLM_THINKING", "enabled")
    assert llm_provider_extra_payload(model="gpt-4o-mini") == {
        "thinking": {"type": "enabled"}
    }


def test_chat_stream_includes_deepseek_thinking_payload(monkeypatch) -> None:
    monkeypatch.delenv("LLM_THINKING", raising=False)
    client = LLMClient(
        api_key="k",
        base_url="https://api.deepseek.com",
        model="deepseek-v4-flash",
        timeout=5,
    )
    resp = MagicMock()
    resp.status_code = 200
    resp.iter_lines.return_value = iter([])

    with patch("src.llm.client.requests.post", return_value=resp) as post:
        list(client.chat_stream([{"role": "user", "content": "hi"}]))

    payload = post.call_args.kwargs["json"]
    assert payload["model"] == "deepseek-v4-flash"
    assert payload["thinking"] == {"type": "disabled"}
