"""Model routing for agent stages."""

from __future__ import annotations

from src.config import (
    LLM_API_KEY,
    LLM_BASE_URL,
    LLM_CONNECT_TIMEOUT,
    LLM_DEBATE_USE_FAST,
    LLM_MODEL_FAST,
    LLM_MODEL_STRONG,
    LLM_READ_TIMEOUT,
)
from src.llm.client import LLMClient


def client_for_model(model: str) -> LLMClient:
    """Build an OpenAI-compatible client using app timeout settings."""
    return LLMClient(
        api_key=LLM_API_KEY,
        base_url=LLM_BASE_URL,
        model=model,
        connect_timeout=LLM_CONNECT_TIMEOUT,
        read_timeout=LLM_READ_TIMEOUT,
    )


def get_fast_client() -> LLMClient:
    return client_for_model(LLM_MODEL_FAST)


def get_strong_client() -> LLMClient:
    return client_for_model(LLM_MODEL_STRONG)


def get_debate_client() -> LLMClient:
    """Debate moderator: STRONG by default; FAST when LLM_DEBATE_USE_FAST=true."""
    if LLM_DEBATE_USE_FAST:
        return get_fast_client()
    return get_strong_client()


def llm_configured() -> bool:
    return bool(LLM_API_KEY)
