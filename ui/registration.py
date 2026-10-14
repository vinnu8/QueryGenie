"""QueryGenie registration page prototype (frontend only, no account creation)."""

from __future__ import annotations

import streamlit as st


def render_registration() -> None:
    """Render a frontend-only registration placeholder."""
    st.markdown(
        """
        <div class="qg-header qg-entrance qg-delay-1">
            <div class="qg-logo">
                <span class="qg-icon" aria-hidden="true">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"
                         stroke-linecap="round" stroke-linejoin="round">
                        <circle cx="12" cy="8" r="4"></circle>
                        <path d="M4 20c0-4 3.6-6 8-6s8 2 8 6"></path>
                    </svg>
                </span>
                <span class="qg-wordmark">QueryGenie</span>
            </div>
            <p class="qg-subtitle">Account registration</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.container(border=True):
        st.text_input(
            "Full name",
            placeholder="Jane Doe",
            help="UI-only field; no account is created.",
            key="registration_name",
        )
        st.text_input(
            "Email or username",
            placeholder="name@company.com",
            help="UI-only field; no account is created.",
            key="registration_username",
        )
        password_show = st.checkbox("Show password", value=False, key="registration_show_password")
        st.text_input(
            "Password",
            type="text" if password_show else "password",
            placeholder="Create a password",
            help="UI-only field; no account is created.",
            key="registration_password",
        )
        create_clicked = st.button("Create account", use_container_width=True, key="registration_create")

        if create_clicked:
            st.info("Account registration will be configured later.")

    st.markdown(
        '<p class="qg-note qg-entrance qg-delay-4">'
        '<span class="qg-dot"></span>'
        'Registration setup coming soon - this is a frontend prototype only.'
        '</p>',
        unsafe_allow_html=True,
    )
