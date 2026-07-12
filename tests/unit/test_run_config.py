"""Runtime run configuration tests."""

from __future__ import annotations

from src.core.run_config import (
    RunConfig,
    apply_run_config,
    coerce_run_config,
    default_panel_run_config,
    is_advanced_run_config,
    run_config_for_mode,
    run_config_from_env,
    run_config_widget_state,
)


def test_default_panel_run_config_is_rule_engine() -> None:
    cfg = default_panel_run_config()
    state = run_config_widget_state(cfg)
    assert cfg.agent_mode == "rule"
    assert state["run_config_mode_label"] == "规则引擎"
    assert cfg.llm_enabled is False


def test_rule_run_config_disables_llm_stages() -> None:
    config = run_config_for_mode("rule", llm_enabled=True, llm_analyst_only="technical")

    assert config.agent_mode == "rule"
    assert config.llm_enabled is False
    assert config.llm_stage_analysts is False
    assert config.llm_stage_bullish is False
    assert config.llm_stage_bearish is False
    assert config.llm_stage_debate is False
    assert config.llm_analyst_only == ""


def test_run_config_fingerprint_changes_with_mode() -> None:
    rule = run_config_for_mode("rule")
    llm = run_config_for_mode("llm")

    assert rule.fingerprint() != llm.fingerprint()
    assert rule.to_dict()["agent_mode"] == "rule"
    assert llm.to_dict()["agent_mode"] == "llm"


def test_coerce_run_config_accepts_dict_snapshot() -> None:
    raw = run_config_for_mode("hybrid", llm_enabled=False).to_dict()
    cfg = coerce_run_config(raw)
    assert cfg is not None
    assert cfg.agent_mode == "hybrid"
    assert cfg.llm_enabled is False


def test_run_config_widget_state_rule_mode() -> None:
    cfg = run_config_for_mode("rule")
    state = run_config_widget_state(cfg)
    assert state["run_config_mode_label"] == "规则引擎"
    assert state["run_config_llm_narrative"] is False
    assert state["run_config_advanced"] is False


def test_run_config_widget_state_marks_advanced_partial_analyst() -> None:
    cfg = RunConfig(
        agent_mode="llm",
        llm_enabled=True,
        llm_stage_analysts=True,
        llm_stage_bullish=True,
        llm_stage_bearish=True,
        llm_stage_debate=True,
        llm_analyst_only="technical",
    )
    state = run_config_widget_state(cfg)
    assert state["run_config_advanced"] is True
    assert state["run_config_llm_technical"] is True
    assert state["run_config_llm_fundamentals"] is False


def test_is_advanced_run_config_partial_analyst() -> None:
    cfg = run_config_for_mode("llm").normalized()
    assert is_advanced_run_config(cfg) is False

    partial = RunConfig(
        agent_mode="llm",
        llm_enabled=True,
        llm_stage_analysts=True,
        llm_stage_bullish=True,
        llm_stage_bearish=True,
        llm_stage_debate=True,
        llm_analyst_only="technical",
    )
    assert is_advanced_run_config(partial) is True


def test_is_advanced_run_config_disabled_stage() -> None:
    cfg = RunConfig(
        agent_mode="hybrid",
        llm_enabled=True,
        llm_stage_analysts=True,
        llm_stage_bullish=False,
        llm_stage_bearish=True,
        llm_stage_debate=True,
    )
    assert is_advanced_run_config(cfg) is True


def test_apply_run_config_binds_thread_context() -> None:
    from src.core.run_context import get_run_config, reset_run_config, set_run_config

    original = run_config_from_env()
    token = set_run_config(original)
    target = RunConfig(
        agent_mode="llm",
        llm_enabled=True,
        llm_stage_analysts=True,
        llm_stage_bullish=True,
        llm_stage_bearish=False,
        llm_stage_debate=True,
        llm_analyst_only="technical",
    )
    try:
        apply_run_config(target)
        cfg = get_run_config()
        assert cfg.agent_mode == "llm"
        assert cfg.llm_enabled is True
        assert cfg.llm_stage_analysts is True
        assert cfg.llm_stage_bullish is True
        assert cfg.llm_stage_bearish is False
        assert cfg.llm_analyst_only == "technical"
    finally:
        reset_run_config(token)


def test_replay_normalized_strips_llm_fields() -> None:
    cfg = RunConfig(
        agent_mode="llm",
        llm_enabled=True,
        llm_stage_analysts=True,
        llm_stage_trader=True,
        replay_mode=True,
        replay_run_id="20260712T100000Z",
    ).normalized()
    assert cfg.replay_mode is True
    assert cfg.replay_run_id == "20260712T100000Z"
    assert cfg.llm_enabled is False
    assert cfg.agent_mode == "rule"
    assert cfg.llm_stage_trader is False


def test_run_config_for_mode_llm_enables_levels() -> None:
    cfg = run_config_for_mode("llm")
    assert cfg.llm_stage_levels is True
    assert cfg.llm_enabled is True


def test_run_config_scope_restores_previous() -> None:
    from src.run.context import get_run_config, run_config_scope

    outer = run_config_from_env()
    inner = run_config_for_mode("llm")
    with run_config_scope(inner):
        assert get_run_config().agent_mode == "llm"
    assert get_run_config().agent_mode == outer.agent_mode
