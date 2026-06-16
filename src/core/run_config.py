"""Runtime report-generation configuration.

The Streamlit UI lets users choose rule/LLM modes after the app starts. Some
pipeline modules import config values as module globals, so this helper applies
the selected values to those imported copies before the background worker runs.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, fields
from typing import Any, Literal

AgentMode = Literal["rule", "llm", "hybrid"]

ANALYST_ONLY_ALIASES = {
    "": "",
    "all": "",
    "technical": "technical",
    "technical_analyst": "technical",
    "fundamentals": "fundamentals",
    "fundamentals_analyst": "fundamentals",
    "news": "news",
    "news_analyst": "news",
    "sentiment": "sentiment",
    "sentiment_analyst": "sentiment",
}


@dataclass(frozen=True)
class RunConfig:
    """Configuration selected before a report generation run."""

    agent_mode: AgentMode = "rule"
    llm_enabled: bool = False
    llm_stage_analysts: bool = False
    llm_stage_bullish: bool = False
    llm_stage_bearish: bool = False
    llm_stage_debate: bool = False
    llm_stage_trader: bool = False
    llm_stage_risk: bool = False
    llm_stage_manager: bool = False
    llm_analyst_only: str = ""

    def normalized(self) -> "RunConfig":
        mode = self.agent_mode if self.agent_mode in ("rule", "llm", "hybrid") else "rule"
        analyst_only = ANALYST_ONLY_ALIASES.get((self.llm_analyst_only or "").strip().lower(), "")
        if mode == "rule":
            return RunConfig(
                agent_mode="rule",
                llm_enabled=False,
                llm_stage_analysts=False,
                llm_stage_bullish=False,
                llm_stage_bearish=False,
                llm_stage_debate=False,
                llm_stage_trader=False,
                llm_stage_risk=False,
                llm_stage_manager=False,
                llm_analyst_only="",
            )
        return RunConfig(
            agent_mode=mode,
            llm_enabled=bool(self.llm_enabled),
            llm_stage_analysts=bool(self.llm_stage_analysts),
            llm_stage_bullish=bool(self.llm_stage_bullish),
            llm_stage_bearish=bool(self.llm_stage_bearish),
            llm_stage_debate=bool(self.llm_stage_debate),
            llm_stage_trader=bool(self.llm_stage_trader),
            llm_stage_risk=bool(self.llm_stage_risk),
            llm_stage_manager=bool(self.llm_stage_manager),
            llm_analyst_only=analyst_only,
        )

    def to_dict(self) -> dict[str, object]:
        return asdict(self.normalized())

    def fingerprint(self) -> str:
        raw = json.dumps(self.to_dict(), ensure_ascii=False, sort_keys=True)
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> "RunConfig":
        if not data:
            return RunConfig()
        known = {f.name for f in fields(cls)}
        filtered = {k: v for k, v in data.items() if k in known}
        return cls(**filtered).normalized()


def coerce_run_config(value: object) -> RunConfig | None:
    """Accept RunConfig instances or dict snapshots from session / report meta."""
    if isinstance(value, RunConfig):
        return value.normalized()
    if isinstance(value, dict):
        return RunConfig.from_dict(value)
    return None


_MODE_UI_LABELS = {
    "rule": "规则引擎",
    "llm": "LLM 智能体",
    "hybrid": "混合模式",
}


def run_config_widget_state(config: RunConfig) -> dict[str, object]:
    """Pure mapping from RunConfig to Streamlit widget session keys."""
    cfg = config.normalized()
    preset = run_config_for_mode(
        cfg.agent_mode,
        llm_enabled=cfg.llm_enabled,
        llm_analyst_only=cfg.llm_analyst_only,
    )
    advanced = cfg.fingerprint() != preset.fingerprint()
    only = cfg.llm_analyst_only
    analyst_checks: dict[str, bool] = {}
    for stage in ("technical", "fundamentals", "news", "sentiment"):
        key = f"run_config_llm_{stage}"
        if only:
            analyst_checks[key] = stage == only
        else:
            analyst_checks[key] = bool(cfg.llm_stage_analysts)

    return {
        "run_config_mode_label": _MODE_UI_LABELS.get(cfg.agent_mode, "规则引擎"),
        "run_config_llm_narrative": cfg.llm_enabled,
        "run_config_advanced": advanced,
        "run_config_stage_analysts": cfg.llm_stage_analysts,
        "run_config_stage_bullish": cfg.llm_stage_bullish,
        "run_config_stage_bearish": cfg.llm_stage_bearish,
        "run_config_stage_debate": cfg.llm_stage_debate,
        "run_config_stage_trader": cfg.llm_stage_trader,
        "run_config_stage_risk": cfg.llm_stage_risk,
        "run_config_stage_manager": cfg.llm_stage_manager,
        **analyst_checks,
    }


def is_advanced_run_config(config: RunConfig) -> bool:
    cfg = config.normalized()
    preset = run_config_for_mode(cfg.agent_mode, llm_enabled=cfg.llm_enabled, llm_analyst_only=cfg.llm_analyst_only)
    return cfg.fingerprint() != preset.fingerprint()


def run_config_from_env() -> RunConfig:
    """Build defaults from imported environment configuration."""
    from src import config as app_config

    return RunConfig(
        agent_mode=app_config.AGENT_MODE,
        llm_enabled=app_config.LLM_ENABLED,
        llm_stage_analysts=app_config.LLM_STAGE_ANALYSTS,
        llm_stage_bullish=app_config.LLM_STAGE_BULLISH,
        llm_stage_bearish=app_config.LLM_STAGE_BEARISH,
        llm_stage_debate=app_config.LLM_STAGE_DEBATE,
        llm_stage_trader=app_config.LLM_STAGE_TRADER,
        llm_stage_risk=app_config.LLM_STAGE_RISK,
        llm_stage_manager=app_config.LLM_STAGE_MANAGER,
        llm_analyst_only=app_config.LLM_ANALYST_ONLY,
    ).normalized()


def run_config_for_mode(mode: AgentMode, *, llm_enabled: bool = True, llm_analyst_only: str = "") -> RunConfig:
    """Create the simple UI presets: rule, llm, or hybrid."""
    if mode == "rule":
        return RunConfig().normalized()
    return RunConfig(
        agent_mode=mode,
        llm_enabled=llm_enabled,
        llm_stage_analysts=True,
        llm_stage_bullish=True,
        llm_stage_bearish=True,
        llm_stage_debate=True,
        llm_stage_trader=False,
        llm_stage_risk=False,
        llm_stage_manager=False,
        llm_analyst_only=llm_analyst_only,
    ).normalized()


def apply_run_config(run_config: RunConfig) -> None:
    """Apply runtime config to modules that imported config globals."""
    cfg = run_config.normalized()

    from src import config as app_config
    from src.agents import factory as agent_factory
    from src.core import orchestrator
    from src.llm import analyst as llm_analyst

    app_config.AGENT_MODE = cfg.agent_mode
    app_config.LLM_ENABLED = cfg.llm_enabled
    app_config.LLM_STAGE_ANALYSTS = cfg.llm_stage_analysts
    app_config.LLM_STAGE_BULLISH = cfg.llm_stage_bullish
    app_config.LLM_STAGE_BEARISH = cfg.llm_stage_bearish
    app_config.LLM_STAGE_DEBATE = cfg.llm_stage_debate
    app_config.LLM_STAGE_TRADER = cfg.llm_stage_trader
    app_config.LLM_STAGE_RISK = cfg.llm_stage_risk
    app_config.LLM_STAGE_MANAGER = cfg.llm_stage_manager
    app_config.LLM_STAGE_RESEARCH = cfg.llm_stage_bullish or cfg.llm_stage_bearish
    app_config.LLM_ANALYST_ONLY = cfg.llm_analyst_only

    agent_factory.AGENT_MODE = cfg.agent_mode
    agent_factory.LLM_STAGE_ANALYSTS = cfg.llm_stage_analysts
    agent_factory.LLM_STAGE_BULLISH = cfg.llm_stage_bullish
    agent_factory.LLM_STAGE_BEARISH = cfg.llm_stage_bearish
    agent_factory.LLM_STAGE_DEBATE = cfg.llm_stage_debate
    agent_factory.LLM_STAGE_TRADER = cfg.llm_stage_trader
    agent_factory.LLM_STAGE_RISK = cfg.llm_stage_risk
    agent_factory.LLM_STAGE_MANAGER = cfg.llm_stage_manager
    agent_factory.LLM_STAGE_RESEARCH = cfg.llm_stage_bullish or cfg.llm_stage_bearish
    agent_factory.LLM_ANALYST_ONLY = cfg.llm_analyst_only

    orchestrator.AGENT_MODE = cfg.agent_mode
    orchestrator.LLM_ENABLED = cfg.llm_enabled

    llm_analyst.LLM_ENABLED = cfg.llm_enabled
