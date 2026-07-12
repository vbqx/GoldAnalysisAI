"""Unit tests for run config panel selection logic (no Streamlit runtime)."""

from __future__ import annotations

from src.core.run_config import RunConfig, run_config_for_mode
from src.viz.run_config_panel import selected_run_config


class _FakeSessionState(dict):
    def get(self, key, default=None):  # type: ignore[override]
        return super().get(key, default)


def test_selected_run_config_replay_takes_priority() -> None:
    session = _FakeSessionState(
        {
            "run_config_replay_mode": True,
            "run_config_replay_run_id": "20260712T080000Z",
            "run_config_mode_label": "LLM 智能体",
        }
    )
    import src.viz.run_config_panel as panel

    original = panel.st.session_state
    panel.st.session_state = session  # type: ignore[assignment]
    try:
        cfg = selected_run_config()
    finally:
        panel.st.session_state = original

    assert cfg.replay_mode is True
    assert cfg.replay_run_id == "20260712T080000Z"
    assert cfg.agent_mode == "rule"


def test_selected_run_config_rule_mode_without_replay() -> None:
    session = _FakeSessionState(
        {
            "run_config_replay_mode": False,
            "run_config_mode_label": "规则引擎",
        }
    )
    import src.viz.run_config_panel as panel

    original = panel.st.session_state
    panel.st.session_state = session  # type: ignore[assignment]
    try:
        cfg = selected_run_config()
    finally:
        panel.st.session_state = original

    expected = run_config_for_mode("rule")
    assert cfg.fingerprint() == expected.fingerprint()


def test_selected_run_config_advanced_all_off_uses_llm_preset() -> None:
    session = _FakeSessionState(
        {
            "run_config_replay_mode": False,
            "run_config_mode_label": "LLM 智能体",
            "run_config_advanced": True,
            "run_config_llm_narrative": True,
            "run_config_stage_analysts": False,
            "run_config_stage_bullish": False,
            "run_config_stage_bearish": False,
            "run_config_stage_debate": False,
            "run_config_stage_levels": False,
            "run_config_stage_trader": False,
            "run_config_stage_risk": False,
            "run_config_stage_manager": False,
            "run_config_llm_technical": False,
            "run_config_llm_fundamentals": False,
            "run_config_llm_news": False,
            "run_config_llm_sentiment": False,
        }
    )
    import src.viz.run_config_panel as panel

    original = panel.st.session_state
    panel.st.session_state = session  # type: ignore[assignment]
    try:
        cfg = selected_run_config()
    finally:
        panel.st.session_state = original

    expected = run_config_for_mode("llm", llm_enabled=True)
    assert cfg.llm_stage_analysts is True
    assert cfg.llm_stage_bullish is True
    assert cfg.llm_stage_debate is True
    assert cfg.llm_stage_trader is True
    assert cfg.fingerprint() == expected.fingerprint()


def test_replay_run_config_fingerprint_stable() -> None:
    a = RunConfig(replay_mode=True, replay_run_id="20260712T074512Z").normalized()
    b = RunConfig(replay_mode=True, replay_run_id="20260712T080000Z").normalized()
    assert a.fingerprint() != b.fingerprint()
