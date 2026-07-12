"""Unit tests for Streamlit report session lifecycle."""

from __future__ import annotations

from unittest.mock import patch

import pytest

from src.core.run_config import run_config_for_mode
from src.viz import generation_state as gs
from src.viz import streamlit_common as sc


@pytest.fixture
def clean_generation_state() -> None:
    gs._STORE.clear()
    yield
    gs._STORE.clear()


def test_store_report_bundle_persists_and_returns(clean_generation_state) -> None:
    bundle = ({"meta": {"title": "t"}}, {"5m": "df"}, {"5m": {}})
    session = {
        sc.SESSION_ID_KEY: "sess-a",
        sc.GENERATION_ID_KEY: "gen-1",
    }
    job_key = "sess-a:gen-1"
    gs.create_job("sess-a", "gen-1")

    with patch.object(sc, "st") as mock_st:
        mock_st.session_state = session
        out = sc._store_report_bundle(job_key, bundle, "fp-abc")

    assert out is bundle
    assert session[sc.REPORT_SESSION_KEY] is bundle
    assert session[sc.REPORT_GENERATION_ID_KEY] == "gen-1"
    assert session[sc.REPORT_CONFIG_FINGERPRINT_KEY] == "fp-abc"
    assert gs.access_job(job_key) is None


def test_ensure_report_returns_finished_bundle_without_second_rerun(clean_generation_state) -> None:
    run_config = run_config_for_mode("llm")
    bundle = (
        {"meta": {"title": "done", "updated_at": "now", "methodology": "test"}},
        {"5m": object()},
        {"5m": {}},
    )
    session = {
        sc.RUN_CONFIG_READY_KEY: True,
        sc.RUN_CONFIG_KEY: run_config,
        sc.SESSION_ID_KEY: "sess-b",
        sc.GENERATION_ID_KEY: "gen-0",
    }
    job = gs.create_job("sess-b", "gen-0")
    job.result = bundle

    with patch.object(sc, "st") as mock_st:
        mock_st.session_state = session
        mock_st.pop = session.pop
        out = sc.ensure_report()

    assert out is bundle
    assert session[sc.REPORT_SESSION_KEY] is bundle
    mock_st.rerun.assert_not_called()
    mock_st.stop.assert_not_called()


def test_generation_jobs_isolated_by_session_uuid(clean_generation_state) -> None:
    job_a = gs.create_job("session-a", "gen-0")
    job_b = gs.create_job("session-b", "gen-0")
    job_a.result = ({"meta": {"who": "a"}}, {}, {})
    job_b.result = ({"meta": {"who": "b"}}, {}, {})

    assert gs.get_job("session-a:gen-0", session_id="session-a") is job_a
    assert gs.get_job("session-b:gen-0", session_id="session-b") is job_b
    assert gs.get_job("session-a:gen-0", session_id="session-b") is None
