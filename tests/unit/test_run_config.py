"""Advice V2 runtime configuration tests."""

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


def test_default_is_deterministic_advice() -> None:
    cfg = default_panel_run_config()
    assert cfg.generation_mode == "rule"
    assert cfg.llm_enabled is False
    assert run_config_widget_state(cfg)["run_config_mode_label"] == "确定性建议"


def test_llm_mode_only_enables_wording_pass() -> None:
    cfg = run_config_for_mode("llm")
    assert cfg.generation_mode == "llm"
    assert cfg.llm_enabled is True
    assert set(cfg.to_dict()) == {"generation_mode", "llm_enabled", "replay_mode", "replay_run_id"}
    assert cfg.fingerprint() != run_config_for_mode("rule").fingerprint()


def test_old_hybrid_snapshot_maps_to_llm_advisor() -> None:
    cfg = coerce_run_config({"agent_mode": "hybrid", "llm_enabled": True, "llm_stage_debate": True})
    assert cfg is not None
    assert cfg.generation_mode == "llm"
    assert cfg.llm_enabled is True


def test_advanced_config_no_longer_exists() -> None:
    assert is_advanced_run_config(run_config_for_mode("rule")) is False
    assert is_advanced_run_config(run_config_for_mode("llm")) is False


def test_apply_run_config_binds_thread_context() -> None:
    from src.core.run_context import get_run_config, reset_run_config, set_run_config

    token = set_run_config(run_config_from_env())
    try:
        target = RunConfig(generation_mode="llm", llm_enabled=True)
        apply_run_config(target)
        assert get_run_config() == target.normalized()
    finally:
        reset_run_config(token)


def test_replay_normalization_disables_generation_mode() -> None:
    cfg = RunConfig(
        generation_mode="llm",
        llm_enabled=True,
        replay_mode=True,
        replay_run_id="20260712T100000Z",
    ).normalized()
    assert cfg.replay_mode is True
    assert cfg.replay_run_id == "20260712T100000Z"
    assert cfg.generation_mode == "rule"
    assert cfg.llm_enabled is False


def test_run_config_scope_restores_previous() -> None:
    from src.run.context import get_run_config, run_config_scope

    outer = run_config_from_env()
    with run_config_scope(run_config_for_mode("llm")):
        assert get_run_config().generation_mode == "llm"
    assert get_run_config().generation_mode == outer.generation_mode
