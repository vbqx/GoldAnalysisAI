"""Auditable budget and retry policy for the single Advice V2 LLM pass."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Literal

from src.config import LLM_MAX_RETRIES, LLM_MODEL, LLM_STAGE_WARN_MS

Tier = Literal["disabled", "advisor"]
BudgetAction = Literal["none", "soft_warn", "hard_degrade"]

# Chars ≈ tokens * 1.8 (same heuristic as llm/context.estimate_payload_size).
_CHARS_PER_TOKEN_EST = 1.8


@dataclass(frozen=True)
class StagePolicy:
    stage: str
    tier: Tier
    max_attempts: int
    input_chars_soft: int
    input_chars_hard: int
    soft_latency_ms: int
    # Mid-run auto-upgrade is off until weekly controlled samples justify it.
    upgrade_enabled: bool = False
    notes: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _default_attempts() -> int:
    """Unified upstream budget: 1 + LLM_MAX_RETRIES (capped 1..6)."""
    return max(1, min(6, int(LLM_MAX_RETRIES) + 1))


def _policies() -> dict[str, StagePolicy]:
    attempts = _default_attempts()
    soft_lat = int(LLM_STAGE_WARN_MS)
    return {
        "advisor": StagePolicy(
            "advisor",
            "advisor",
            attempts,
            18_000,
            30_000,
            soft_lat,
            notes="Advice V2 single wording pass; deterministic numbers and direction remain immutable",
        ),
    }


def get_stage_policy(stage: str) -> StagePolicy:
    table = _policies()
    if stage in table:
        return table[stage]
    attempts = _default_attempts()
    return StagePolicy(
        stage=stage,
        tier="advisor",
        max_attempts=attempts,
        input_chars_soft=50_000,
        input_chars_hard=90_000,
        soft_latency_ms=int(LLM_STAGE_WARN_MS),
        notes="unknown stage — default strong tier",
    )


def estimate_messages_size(messages: list[dict[str, str]]) -> dict[str, int]:
    chars = sum(len(str(m.get("content") or "")) for m in messages)
    return {
        "input_chars": chars,
        "input_tokens_est": int(round(chars / _CHARS_PER_TOKEN_EST)),
    }


def estimate_text_size(text: str) -> dict[str, int]:
    chars = len(text or "")
    return {
        "output_chars": chars,
        "output_tokens_est": int(round(chars / _CHARS_PER_TOKEN_EST)),
    }


def apply_input_budget(
    messages: list[dict[str, str]],
    policy: StagePolicy,
) -> tuple[list[dict[str, str]], BudgetAction, dict[str, Any]]:
    """Enforce soft/hard input budgets without silently dropping auth facts.

    Soft: proceed with ``soft_warn``.
    Hard: keep system prompts intact; truncate the largest user message with an
    explicit ``[BUDGET_TRUNCATED]`` marker (visible degrade, not silent clip).
    """
    size = estimate_messages_size(messages)
    chars = size["input_chars"]
    meta: dict[str, Any] = {
        **size,
        "input_chars_soft": policy.input_chars_soft,
        "input_chars_hard": policy.input_chars_hard,
        "max_attempts": policy.max_attempts,
    }
    if chars <= policy.input_chars_soft:
        return messages, "none", meta
    if chars <= policy.input_chars_hard:
        meta["budget_note"] = (
            f"input {chars} chars exceeds soft budget {policy.input_chars_soft}"
        )
        return messages, "soft_warn", meta

    # Hard: truncate largest user content; leave system messages untouched.
    out = [dict(m) for m in messages]
    user_idxs = [i for i, m in enumerate(out) if (m.get("role") or "") == "user"]
    if not user_idxs:
        user_idxs = list(range(len(out)))
    target = max(user_idxs, key=lambda i: len(str(out[i].get("content") or "")))
    content = str(out[target].get("content") or "")
    # Reserve room for marker + keep head (mandate) and tail (recent facts).
    marker = (
        f"\n\n[BUDGET_TRUNCATED stage={policy.stage} "
        f"chars={chars}>{policy.input_chars_hard} "
        f"auth/trigger/claim fields must not be inferred from omitted text]\n\n"
    )
    keep = max(2_000, policy.input_chars_hard - 500)
    head = keep // 3
    tail = keep - head - len(marker)
    if tail < 500:
        tail = 500
        head = max(500, keep - tail - len(marker))
    if len(content) > keep:
        out[target]["content"] = content[:head] + marker + content[-tail:]
    new_size = estimate_messages_size(out)
    meta.update(new_size)
    meta["budget_note"] = (
        f"hard degrade: truncated user message from {chars} to {new_size['input_chars']} chars"
    )
    meta["original_input_chars"] = chars
    return out, "hard_degrade", meta


def build_routing_strategy() -> dict[str, Any]:
    """Archive-friendly snapshot of the single-model Advice V2 policy."""
    return {
        "policy_version": "advice-llm-v2",
        "model": LLM_MODEL,
        "same_model_strategy": True,
        "same_model_reason": "Advice V2 has exactly one optional LLM wording stage.",
        "upgrade_default": False,
        "stages": {name: p.to_dict() for name, p in _policies().items()},
    }
