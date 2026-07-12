"""Streamlit session keys and report cache helpers."""

from __future__ import annotations

import uuid

import streamlit as st

from src.viz.generation_state import drop_job

REPORT_SESSION_KEY = "report_bundle"
FORCE_REFRESH_KEY = "force_refresh_report"
RUN_CONFIG_KEY = "report_run_config"
RUN_CONFIG_READY_KEY = "report_run_config_ready"
REPORT_CONFIG_FINGERPRINT_KEY = f"{REPORT_SESSION_KEY}_run_config_fingerprint"
RUN_CONFIG_REFRESH_UI_KEY = "run_config_refresh_ui"
RUN_CONFIG_WIDGETS_SEEDED_KEY = "run_config_widgets_seeded"
SESSION_ID_KEY = "_ga_session_uuid"
GENERATION_ID_KEY = "_ga_generation_uuid"
REPORT_GENERATION_ID_KEY = f"{REPORT_SESSION_KEY}_generation_id"


def session_id() -> str:
    if SESSION_ID_KEY not in st.session_state:
        st.session_state[SESSION_ID_KEY] = str(uuid.uuid4())
    return str(st.session_state[SESSION_ID_KEY])


def generation_id() -> str:
    if GENERATION_ID_KEY not in st.session_state:
        st.session_state[GENERATION_ID_KEY] = str(uuid.uuid4())
    return str(st.session_state[GENERATION_ID_KEY])


def job_key() -> str:
    return f"{session_id()}:{generation_id()}"


def rotate_generation_id() -> str:
    new_id = str(uuid.uuid4())
    st.session_state[GENERATION_ID_KEY] = new_id
    return new_id


def invalidate_report_cache() -> None:
    old_key = job_key()
    drop_job(old_key, session_id=session_id())
    rotate_generation_id()
    st.session_state.pop(REPORT_SESSION_KEY, None)
    st.session_state.pop(REPORT_GENERATION_ID_KEY, None)
    st.session_state.pop(REPORT_CONFIG_FINGERPRINT_KEY, None)
