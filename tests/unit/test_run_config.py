"""Runtime run configuration tests."""

from __future__ import annotations

from src.core.run_config import RunConfig, apply_run_config, run_config_for_mode, run_config_from_env


def test_rule_run_config_disables_llm_stages() -> None:
    config = run_config_for_mode("rule", llm_enabled=True, llm_analyst_only="technical")

    assert config.agent_mode == "rule"
    assert config.llm_enabled is False
    assert config.llm_stage_analysts is False
    assert config.llm_stage_research is False
    assert config.llm_stage_debate is False
    assert config.llm_analyst_only == ""


def test_run_config_fingerprint_changes_with_mode() -> None:
    rule = run_config_for_mode("rule")
    llm = run_config_for_mode("llm")

    assert rule.fingerprint() != llm.fingerprint()
    assert rule.to_dict()["agent_mode"] == "rule"
    assert llm.to_dict()["agent_mode"] == "llm"


def test_apply_run_config_updates_import_bound_modules() -> None:
    from src import config as app_config
    from src.agents import factory as agent_factory
    from src.core import orchestrator
    from src.llm import analyst as llm_analyst

    original = run_config_from_env()
    target = RunConfig(
        agent_mode="llm",
        llm_enabled=True,
        llm_stage_analysts=True,
        llm_stage_research=True,
        llm_stage_debate=True,
        llm_analyst_only="technical",
    )

    try:
        apply_run_config(target)

        assert app_config.AGENT_MODE == "llm"
        assert agent_factory.AGENT_MODE == "llm"
        assert agent_factory.LLM_STAGE_ANALYSTS is True
        assert agent_factory.LLM_ANALYST_ONLY == "technical"
        assert orchestrator.AGENT_MODE == "llm"
        assert orchestrator.LLM_ENABLED is True
        assert llm_analyst.LLM_ENABLED is True
    finally:
        apply_run_config(original)
