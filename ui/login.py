"""QueryGenie login page prototype (frontend only, no authentication)."""

from __future__ import annotations

import streamlit as st


_HEADER_HTML = """
<div class="qg-header qg-entrance qg-delay-1">
    <div class="qg-logo">
        <span class="qg-icon" aria-hidden="true">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"
                 stroke-linecap="round" stroke-linejoin="round">
                <ellipse cx="12" cy="5" rx="8" ry="3"></ellipse>
                <path d="M4 5v6c0 1.7 3.6 3 8 3s8-1.3 8-3V5"></path>
                <path d="M4 11v6c0 1.7 3.6 3 8 3s8-1.3 8-3v-6"></path>
                <path d="M19 3l1.2 1.2L22 5" stroke="#FDE68A"></path>
            </svg>
        </span>
        <span class="qg-wordmark">QueryGenie</span>
    </div>
    <p class="qg-subtitle">Welcome / Login page</p>
</div>
"""

_FLOW_CARD_HTML = """
<div class="qg-flow-card qg-entrance qg-delay-2">
    <h3>Enter username + password</h3>
    <p class="qg-support">System verifies credentials and role</p>
</div>
<div class="qg-down-arrow qg-entrance qg-delay-2">
    <svg width="26" height="26" viewBox="0 0 24 24" fill="none"
         stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
         class="qg-pulse">
        <path d="M12 5v14"></path>
        <path d="M5 12l7 7 7-7"></path>
    </svg>
</div>
"""

_ROLE_CARDS_HTML = """
<div class="qg-bridge qg-entrance qg-delay-3">
    <svg viewBox="0 0 100 40" preserveAspectRatio="none">
        <line x1="50" y1="0" x2="25" y2="40" class="qg-flow-line"
              stroke="#2457E6" stroke-width="1.6" stroke-linecap="round"/>
        <line x1="50" y1="0" x2="75" y2="40" class="qg-flow-line"
              stroke="#0D9488" stroke-width="1.6" stroke-linecap="round"/>
        <polygon points="22,36 25,40 28,36" fill="#2457E6" class="qg-flow-line"/>
        <polygon points="72,36 75,40 78,36" fill="#0D9488" class="qg-flow-line"/>
    </svg>
</div>
<div class="qg-role-grid qg-entrance qg-delay-3">
    <div class="qg-role-card qg-role-admin">
        <h4>Admin Dashboard
            <span class="qg-badge">admin</span>
        </h4>
        <ul class="qg-feature-list">
            <li>Ask queries</li>
            <li>View charts</li>
            <li>Manage records</li>
            <li>Create employee accounts</li>
        </ul>
    </div>
    <div class="qg-role-card qg-role-employee">
        <h4>Employee Dashboard
            <span class="qg-badge">employee</span>
        </h4>
        <ul class="qg-feature-list">
            <li>Ask queries</li>
            <li>View charts</li>
            <li>Explore insights</li>
            <li>No record editing</li>
        </ul>
    </div>
</div>
<p class="qg-role-caption qg-entrance qg-delay-3">
    Role-based dashboards are previews only - they are not implemented yet.
</p>
"""


def render_login() -> None:
    """Render the frontend-only login page prototype."""
    st.markdown(_HEADER_HTML, unsafe_allow_html=True)
    st.markdown(_FLOW_CARD_HTML, unsafe_allow_html=True)
    st.markdown(_ROLE_CARDS_HTML, unsafe_allow_html=True)

    with st.container(border=True):
        username = st.text_input(
            "Email or username",
            placeholder="name@company.com",
            help="UI-only field; no authentication is performed.",
            key="login_username",
        )
        show_password = st.checkbox("Show password", value=False, key="show_password_toggle")
        password = st.text_input(
            "Password",
            type="text" if show_password else "password",
            placeholder="Enter your password",
            help="UI-only field; no authentication is performed.",
            key="login_password",
        )
        st.checkbox("Remember me", value=False, key="remember_me")
        sign_in_clicked = st.button("Sign in", use_container_width=True, key="login_sign_in")

        if sign_in_clicked:
            if not (username or "").strip() or not (password or ""):
                st.warning("Please enter both email/username and password.")
            else:
                st.info("Authentication will be configured soon.")

    st.markdown(
        '<p class="qg-note qg-entrance qg-delay-4">'
        '<span class="qg-dot"></span>'
        'Authentication setup coming soon - login is a frontend prototype only.'
        '</p>',
        unsafe_allow_html=True,
    )
