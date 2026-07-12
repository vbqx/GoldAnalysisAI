"""Shared Streamlit page chrome."""

from __future__ import annotations

import streamlit as st


def render_page_hero(title: str, subtitle: str = "") -> None:
    sub = f"<p>{subtitle}</p>" if subtitle else ""
    st.markdown(
        f'<div class="page-hero"><h1>{title}</h1>{sub}</div>',
        unsafe_allow_html=True,
    )
