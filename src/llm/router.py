"""Model routing for agent stages."""

from __future__ import annotations

from src.config import (
    LLM_API_KEY,
    LLM_BASE_URL,
    LLM_CONNECT_TIMEOUT,
    LLM_DEBATE_USE_FAST,
    LLM_MODEL,
    LLM_MODEL_FAST,
    LLM_MODEL_STRONG,
    LLM_READ_TIMEOUT,
)
from src.llm.client import LLMClient
from src.llm.stage_policy import build_routing_strategy, get_stage_policy


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


def client_for_stage(stage: str) -> LLMClient:
    """Resolve client from the auditable stage policy table (Issue #37)."""
    policy = get_stage_policy(stage)
    if policy.tier == "fast":
        return get_fast_client()
    if policy.tier == "report":
        return client_for_model(LLM_MODEL)
    if stage == "debate":
        return get_debate_client()
    return get_strong_client()


def routing_meta() -> dict:
    """Archive-friendly snapshot of FAST/STRONG/REPORT strategy."""
    return build_routing_strategy()


def llm_configured() -> bool:
    return bool(LLM_API_KEY)
