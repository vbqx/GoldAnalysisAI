"""Runtime report-generation configuration.

The Streamlit UI lets users choose rule/LLM modes after the app starts. Some
pipeline modules import config values as module globals, so this helper applies
the selected values to those imported copies before the background worker runs.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from typing import Literal

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
    llm_stage_research: bool = False
    llm_stage_debate: bool = False
    llm_analyst_only: str = ""

    def normalized(self) -> "RunConfig":
        mode = self.agent_mode if self.agent_mode in ("rule", "llm", "hybrid") else "rule"
        analyst_only = ANALYST_ONLY_ALIASES.get((self.llm_analyst_only or "").strip().lower(), "")
        if mode == "rule":
            return RunConfig(
                agent_mode="rule",
                llm_enabled=False,
                llm_stage_analysts=False,
                llm_stage_research=False,
                llm_stage_debate=False,
                llm_analyst_only="",
            )
        return RunConfig(
            agent_mode=mode,
            llm_enabled=bool(self.llm_enabled),
            llm_stage_analysts=bool(self.llm_stage_analysts),
            llm_stage_research=bool(self.llm_stage_research),
            llm_stage_debate=bool(self.llm_stage_debate),
            llm_analyst_only=analyst_only,
        )

    def to_dict(self) -> dict[str, object]:
        return asdict(self.normalized())

    def fingerprint(self) -> str:
        raw = json.dumps(self.to_dict(), ensure_ascii=False, sort_keys=True)
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]


def run_config_from_env() -> RunConfig:
    """Build defaults from imported environment configuration."""
    from src import config as app_config

    return RunConfig(
        agent_mode=app_config.AGENT_MODE,
        llm_enabled=app_config.LLM_ENABLED,
        llm_stage_analysts=app_config.LLM_STAGE_ANALYSTS,
        llm_stage_research=app_config.LLM_STAGE_RESEARCH,
        llm_stage_debate=app_config.LLM_STAGE_DEBATE,
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
        llm_stage_research=True,
        llm_stage_debate=True,
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
    app_config.LLM_STAGE_RESEARCH = cfg.llm_stage_research
    app_config.LLM_STAGE_DEBATE = cfg.llm_stage_debate
    app_config.LLM_ANALYST_ONLY = cfg.llm_analyst_only

    agent_factory.AGENT_MODE = cfg.agent_mode
    agent_factory.LLM_STAGE_ANALYSTS = cfg.llm_stage_analysts
    agent_factory.LLM_STAGE_RESEARCH = cfg.llm_stage_research
    agent_factory.LLM_STAGE_DEBATE = cfg.llm_stage_debate
    agent_factory.LLM_ANALYST_ONLY = cfg.llm_analyst_only

    orchestrator.AGENT_MODE = cfg.agent_mode
    orchestrator.LLM_ENABLED = cfg.llm_enabled

    llm_analyst.LLM_ENABLED = cfg.llm_enabled
