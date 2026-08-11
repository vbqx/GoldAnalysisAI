"""Model routing for the optional Advice V2 wording pass."""

from __future__ import annotations

from src.config import (
    LLM_API_KEY,
    LLM_BASE_URL,
    LLM_CONNECT_TIMEOUT,
    LLM_MODEL,
    LLM_READ_TIMEOUT,
)
from src.llm.client import LLMClient


def client_for_stage(stage: str) -> LLMClient:
    """Return the single configured client; ``stage`` is retained for audit naming."""
    del stage
    return LLMClient(
        api_key=LLM_API_KEY,
        base_url=LLM_BASE_URL,
        model=LLM_MODEL,
        connect_timeout=LLM_CONNECT_TIMEOUT,
        read_timeout=LLM_READ_TIMEOUT,
    )


def llm_configured() -> bool:
    return bool(LLM_API_KEY)
