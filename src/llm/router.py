"""Model routing for agent stages."""

from __future__ import annotations

from src.config import (
    LLM_API_KEY,
    LLM_BASE_URL,
    LLM_DEBATE_USE_FAST,
    LLM_MODEL_FAST,
    LLM_MODEL_STRONG,
    LLM_TIMEOUT,
)
from src.llm.client import LLMClient


def get_fast_client() -> LLMClient:
    return LLMClient(
        api_key=LLM_API_KEY,
        base_url=LLM_BASE_URL,
        model=LLM_MODEL_FAST,
        timeout=LLM_TIMEOUT,
    )


def get_strong_client() -> LLMClient:
    return LLMClient(
        api_key=LLM_API_KEY,
        base_url=LLM_BASE_URL,
        model=LLM_MODEL_STRONG,
        timeout=LLM_TIMEOUT,
    )


def get_debate_client() -> LLMClient:
    """Debate moderator: STRONG by default; FAST when LLM_DEBATE_USE_FAST=true."""
    if LLM_DEBATE_USE_FAST:
        return get_fast_client()
    return get_strong_client()


def llm_configured() -> bool:
    return bool(LLM_API_KEY)
