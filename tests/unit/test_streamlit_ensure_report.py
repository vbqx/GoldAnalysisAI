"""Unit tests for Streamlit report session lifecycle."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from src.core.run_config import run_config_for_mode
from src.viz import streamlit_common as sc


@pytest.fixture
def clean_generation_state(monkeypatch: pytest.MonkeyPatch) -> None:
    sc._GEN_RESULTS.clear()
    sc._GEN_ERRORS.clear()
    sc._LIVE_GEN_STATE.clear()
    sc._GEN_THREADS.clear()
    monkeypatch.setattr(sc, "_GEN_THREADS", sc._GEN_THREADS)
    monkeypatch.setattr(sc, "_GEN_RESULTS", sc._GEN_RESULTS)
    monkeypatch.setattr(sc, "_GEN_ERRORS", sc._GEN_ERRORS)
    monkeypatch.setattr(sc, "_LIVE_GEN_STATE", sc._LIVE_GEN_STATE)


def test_store_report_bundle_persists_and_returns(clean_generation_state) -> None:
    bundle = ({"meta": {"title": "t"}}, {"5m": "df"}, {"5m": {}})
    session: dict = {}

    with patch.object(sc, "st") as mock_st:
        mock_st.session_state = session
        out = sc._store_report_bundle(3, bundle, "fp-abc")

    assert out is bundle
    assert session[sc.REPORT_SESSION_KEY] is bundle
    assert session[f"{sc.REPORT_SESSION_KEY}_counter"] == 3
    assert session[sc.REPORT_CONFIG_FINGERPRINT_KEY] == "fp-abc"
    assert 3 not in sc._LIVE_GEN_STATE


def test_ensure_report_returns_finished_bundle_without_second_rerun(clean_generation_state) -> None:
    run_config = run_config_for_mode("llm")
    bundle = (
        {"meta": {"title": "done", "updated_at": "now", "methodology": "test"}},
        {"5m": object()},
        {"5m": {}},
    )
    sc._GEN_RESULTS[0] = bundle
    session = {
        sc.RUN_CONFIG_READY_KEY: True,
        sc.RUN_CONFIG_KEY: run_config,
        sc.REFRESH_COUNTER_KEY: 0,
    }

    with patch.object(sc, "st") as mock_st:
        mock_st.session_state = session
        mock_st.pop = session.pop
        out = sc.ensure_report()

    assert out is bundle
    assert session[sc.REPORT_SESSION_KEY] is bundle
    assert 0 not in sc._GEN_RESULTS
    mock_st.rerun.assert_not_called()
    mock_st.stop.assert_not_called()
