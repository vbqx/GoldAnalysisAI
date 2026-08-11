"""Runtime configuration for the single Advice V2 pipeline."""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, fields
from typing import Any, Literal

GenerationMode = Literal["rule", "llm"]


@dataclass(frozen=True)
class RunConfig:
    """Choose deterministic advice or one constrained LLM wording pass."""

    generation_mode: GenerationMode = "rule"
    llm_enabled: bool = False
    replay_mode: bool = False
    replay_run_id: str = ""

    def normalized(self) -> "RunConfig":
        replay_run_id = str(self.replay_run_id or "").strip()
        if self.replay_mode and replay_run_id:
            return RunConfig(replay_mode=True, replay_run_id=replay_run_id)
        mode: GenerationMode = "llm" if self.generation_mode == "llm" else "rule"
        return RunConfig(
            generation_mode=mode,
            llm_enabled=bool(self.llm_enabled and mode == "llm"),
            replay_mode=False,
            replay_run_id="",
        )

    def to_dict(self) -> dict[str, object]:
        return asdict(self.normalized())

    def fingerprint(self) -> str:
        raw = json.dumps(self.to_dict(), ensure_ascii=False, sort_keys=True)
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> "RunConfig":
        if not data:
            return cls()
        migrated = dict(data)
        if "generation_mode" not in migrated and "agent_mode" in migrated:
            migrated["generation_mode"] = migrated["agent_mode"]
        known = {item.name for item in fields(cls)}
        filtered = {key: value for key, value in migrated.items() if key in known}
        # Old hybrid archives map to the only remaining LLM-assisted mode.
        if filtered.get("generation_mode") == "hybrid":
            filtered["generation_mode"] = "llm"
            filtered["llm_enabled"] = True
        return cls(**filtered).normalized()


def coerce_run_config(value: object) -> RunConfig | None:
    if isinstance(value, RunConfig):
        return value.normalized()
    if isinstance(value, dict):
        return RunConfig.from_dict(value)
    return None


def run_config_widget_state(config: RunConfig) -> dict[str, object]:
    cfg = config.normalized()
    return {
        "run_config_mode_label": "LLM 解释增强" if cfg.generation_mode == "llm" else "确定性建议",
        "run_config_replay_mode": cfg.replay_mode,
        "run_config_replay_run_id": cfg.replay_run_id,
    }


def is_advanced_run_config(config: RunConfig) -> bool:
    return False


def default_panel_run_config() -> RunConfig:
    return RunConfig()


def run_config_from_env() -> RunConfig:
    from src import config as app_config

    enabled = bool(app_config.LLM_ENABLED)
    return RunConfig(generation_mode="llm" if enabled else "rule", llm_enabled=enabled).normalized()


def run_config_for_mode(
    mode: str,
    *,
    llm_enabled: bool = True,
    llm_analyst_only: str = "",
) -> RunConfig:
    del llm_analyst_only
    resolved = "llm" if mode in ("llm", "hybrid") else "rule"
    return RunConfig(generation_mode=resolved, llm_enabled=llm_enabled and resolved == "llm").normalized()


def apply_run_config(run_config: RunConfig) -> None:
    from src.run.context import set_run_config

    set_run_config(run_config.normalized())
