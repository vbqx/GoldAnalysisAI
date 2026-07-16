"""Auditable per-stage LLM routing, attempt budget, and input size policy (Issue #37).

Risk/Manager remain subject to deterministic gates; a stronger model never bypasses them.
Upgrade-to-strong mid-run is disabled by default — compare strategies on weekly samples first.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Literal

from src.config import (
    LLM_MAX_RETRIES,
    LLM_MODEL,
    LLM_MODEL_FAST,
    LLM_MODEL_STRONG,
    LLM_STAGE_WARN_MS,
)

Tier = Literal["disabled", "fast", "strong", "report"]
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
        "technical": StagePolicy("technical", "fast", attempts, 45_000, 80_000, soft_lat),
        "fundamentals": StagePolicy("fundamentals", "fast", attempts, 35_000, 60_000, soft_lat),
        "news": StagePolicy("news", "fast", attempts, 40_000, 70_000, soft_lat),
        "sentiment": StagePolicy("sentiment", "fast", attempts, 30_000, 55_000, soft_lat),
        "bullish": StagePolicy("bullish", "fast", attempts, 40_000, 70_000, soft_lat),
        "bearish": StagePolicy("bearish", "fast", attempts, 40_000, 70_000, soft_lat),
        "debate": StagePolicy(
            "debate",
            "strong",
            attempts,
            35_000,
            60_000,
            soft_lat,
            notes="LLM_DEBATE_USE_FAST may route to FAST without changing tier label in archive",
        ),
        "llm_levels": StagePolicy("llm_levels", "strong", attempts, 60_000, 100_000, soft_lat),
        "trader": StagePolicy("trader", "strong", attempts, 40_000, 70_000, soft_lat),
        "risk": StagePolicy(
            "risk",
            "strong",
            attempts,
            35_000,
            65_000,
            soft_lat,
            notes="Deterministic risk gates remain authoritative; LLM is advisory",
        ),
        "manager": StagePolicy(
            "manager",
            "strong",
            attempts,
            30_000,
            55_000,
            soft_lat,
            notes="ManagerDecision still gated by trigger/claim/invariant layers",
        ),
        "llm_narrative": StagePolicy("llm_narrative", "report", attempts, 70_000, 110_000, soft_lat),
    }


def get_stage_policy(stage: str) -> StagePolicy:
    table = _policies()
    if stage in table:
        return table[stage]
    attempts = _default_attempts()
    return StagePolicy(
        stage=stage,
        tier="strong",
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
    """Explicit FAST/STRONG/REPORT layering status for archive / Runtime Ledger."""
    fast = LLM_MODEL_FAST
    strong = LLM_MODEL_STRONG
    report = LLM_MODEL
    same = fast == strong == report
    return {
        "policy_version": "llm-stage-v1",
        "fast_model": fast,
        "strong_model": strong,
        "report_model": report,
        "same_model_strategy": same,
        "same_model_reason": (
            "FAST/STRONG/REPORT are identical; cost/latency tiering is not active. "
            "Keep this explicit until a weekly controlled sample justifies splitting models."
            if same
            else "Distinct FAST/STRONG/REPORT models configured."
        ),
        "upgrade_default": False,
        "stages": {name: p.to_dict() for name, p in _policies().items()},
    }
