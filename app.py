"""QueryGenie application entry point (frontend prototype)."""

from __future__ import annotations

import importlib
from pathlib import Path

import streamlit as st

import UI.login
import UI.theme


def _reload_if_changed(module) -> None:
    """Re-import a UI module when its source file changed.

    Streamlit watches the project folder and reruns the script whenever a
    file changes, but an already imported module stays cached in
    ``sys.modules``. Without this guard, edits inside ``UI/`` would only show
    up after restarting the server. Reloading on change keeps the live preview
    in sync with the files on disk
    """
    source = Path(module.__file__)
    modified = source.stat().st_mtime
    if modified > getattr(module, "_qg_source_mtime", 0.0):
        importlib.reload(module)
        module._qg_source_mtime = modified


st.set_page_config(
    page_title="QueryGenie - Sign in",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="collapsed",
)

for _ui_module in (UI.login, UI.theme):
    _reload_if_changed(_ui_module)

UI.theme.inject_theme()

# The login prototype is the default view. The sibling `UI/registration.py`
# module is intentionally kept separate so genuine authentication and
# account registration can be wired in here later without rebuilding the UI.
UI.login.render_login()