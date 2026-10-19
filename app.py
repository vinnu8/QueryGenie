"""QueryGenie application entry point (frontend prototype)."""

from __future__ import annotations

import streamlit as st

from ui.login import render_login
from ui.theme import inject_theme


st.set_page_config(
    page_title="QueryGenie - Sign in",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="collapsed",
)

inject_theme()

# The login prototype is the default view. The sibling `ui/registration.py`
# module is intentionally kept separate so genuine authentication and
# account registration can be wired in here later without rebuilding the UI.
render_login()
