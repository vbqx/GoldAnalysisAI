"""LLM default provider configuration."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

from src.config import llm_provider_extra_payload
from src.llm.client import LLMClient


def test_llm_provider_extra_payload_auto_disables_direct_deepseek_v4_thinking(
    monkeypatch,
) -> None:
    monkeypatch.delenv("LLM_THINKING", raising=False)
    monkeypatch.setattr("src.config.LLM_BASE_URL", "https://api.deepseek.com")
    assert llm_provider_extra_payload(model="deepseek-v4-flash") == {
        "thinking": {"type": "disabled"}
    }


def test_llm_provider_extra_payload_skips_thinking_for_siliconflow(monkeypatch) -> None:
    monkeypatch.delenv("LLM_THINKING", raising=False)
    monkeypatch.setattr("src.config.LLM_BASE_URL", "https://api.siliconflow.cn/v1")
    assert llm_provider_extra_payload(model="deepseek-ai/DeepSeek-V4-Flash") == {}


def test_llm_provider_extra_payload_respects_explicit_thinking(monkeypatch) -> None:
    monkeypatch.setenv("LLM_THINKING", "enabled")
    monkeypatch.setattr("src.config.LLM_BASE_URL", "https://api.siliconflow.cn/v1")
    assert llm_provider_extra_payload(model="deepseek-ai/DeepSeek-V4-Flash") == {
        "thinking": {"type": "enabled"}
    }


def test_chat_stream_omits_thinking_payload_on_siliconflow(monkeypatch) -> None:
    monkeypatch.delenv("LLM_THINKING", raising=False)
    monkeypatch.setattr("src.config.LLM_BASE_URL", "https://api.siliconflow.cn/v1")
    client = LLMClient(
        api_key="k",
        base_url="https://api.siliconflow.cn/v1",
        model="deepseek-ai/DeepSeek-V4-Flash",
        timeout=5,
    )
    resp = MagicMock()
    resp.status_code = 200
    resp.iter_lines.return_value = iter([])

    with patch("src.llm.client.requests.post", return_value=resp) as post:
        list(client.chat_stream([{"role": "user", "content": "hi"}]))

    payload = post.call_args.kwargs["json"]
    assert payload["model"] == "deepseek-ai/DeepSeek-V4-Flash"
    assert "thinking" not in payload
