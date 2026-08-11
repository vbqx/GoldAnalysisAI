"""Advice V2 run-config panel selection logic."""

from __future__ import annotations

from src.core.run_config import RunConfig, run_config_for_mode
from src.viz.run_config_panel import selected_run_config


class _FakeSessionState(dict):
    def get(self, key, default=None):  # type: ignore[override]
        return super().get(key, default)


def _select(state: dict) -> RunConfig:
    import src.viz.run_config_panel as panel

    original = panel.st.session_state
    panel.st.session_state = _FakeSessionState(state)  # type: ignore[assignment]
    try:
        return selected_run_config()
    finally:
        panel.st.session_state = original


def test_replay_takes_priority() -> None:
    cfg = _select(
        {
            "run_config_replay_mode": True,
            "run_config_replay_run_id": "20260712T080000Z",
            "run_config_mode_label": "LLM 解释增强",
        }
    )
    assert cfg == RunConfig(replay_mode=True, replay_run_id="20260712T080000Z").normalized()


def test_deterministic_mode() -> None:
    cfg = _select({"run_config_replay_mode": False, "run_config_mode_label": "确定性建议"})
    assert cfg == run_config_for_mode("rule")


def test_llm_mode_is_single_wording_pass() -> None:
    cfg = _select({"run_config_replay_mode": False, "run_config_mode_label": "LLM 解释增强"})
    assert cfg == run_config_for_mode("llm")


def test_replay_fingerprint_includes_run_id() -> None:
    a = RunConfig(replay_mode=True, replay_run_id="a").normalized()
    b = RunConfig(replay_mode=True, replay_run_id="b").normalized()
    assert a.fingerprint() != b.fingerprint()
