"""QueryGenie Streamlit application."""

from __future__ import annotations

import streamlit as st

from UI.auth import render_auth
from UI.theme import inject_theme
from UI.workspace import render_workspace


st.set_page_config(
    page_title="QueryGenie",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="collapsed",
)

inject_theme()
user = st.session_state.get("qg_authenticated_user")
if user is None:
    render_auth()
else:
    render_workspace(user)
