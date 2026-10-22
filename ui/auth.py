"""Sign-in and account registration screens."""

from __future__ import annotations

import streamlit as st

from services.auth import authenticate, create_account


def _render_brand() -> None:
    st.markdown(
        '<div class="qg-auth-brand"><span class="qg-brand-mark">⌕</span>'
        '<span>QueryGenie</span></div>',
        unsafe_allow_html=True,
    )


def render_auth() -> None:
    """Render sign-in and self-service registration."""
    left, center, right = st.columns([1, 1.35, 1])
    with center:
        _render_brand()
        st.markdown('<div class="qg-auth-heading">Make sense of your data.</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="qg-auth-description">Upload a dataset and explore it with simple questions.</div>',
            unsafe_allow_html=True,
        )
        sign_in, register = st.tabs(["Sign in", "Create account"])

        with sign_in:
            with st.form("qg_signin_form"):
                email = st.text_input("Email", placeholder="you@company.com", autocomplete="email")
                password = st.text_input(
                    "Password",
                    type="password",
                    placeholder="Your password",
                    autocomplete="current-password",
                )
                submitted = st.form_submit_button("Sign in", type="primary", use_container_width=True)
            if submitted:
                try:
                    user = authenticate(email, password)
                except RuntimeError as error:
                    st.error(str(error))
                else:
                    if user is None:
                        st.error("Email or password is incorrect.")
                    else:
                        st.session_state.qg_authenticated_user = user
                        st.rerun()
            st.caption("New to QueryGenie? Create an account to get started.")

        with register:
            with st.form("qg_register_form"):
                name = st.text_input("Full name", placeholder="Jane Doe", autocomplete="name")
                email = st.text_input("Email", placeholder="you@company.com", autocomplete="email")
                password = st.text_input(
                    "Password",
                    type="password",
                    placeholder="At least 10 characters",
                    autocomplete="new-password",
                )
                confirm_password = st.text_input(
                    "Confirm password",
                    type="password",
                    placeholder="Enter your password again",
                    autocomplete="new-password",
                )
                submitted = st.form_submit_button(
                    "Create account",
                    type="primary",
                    use_container_width=True,
                )
            if submitted:
                if password != confirm_password:
                    st.error("The passwords do not match.")
                else:
                    try:
                        user = create_account(name, email, password)
                    except ValueError as error:
                        st.error(str(error))
                    except RuntimeError as error:
                        st.error(str(error))
                    else:
                        st.session_state.qg_authenticated_user = user
                        st.rerun()
            st.caption("Your account is stored locally on this server.")
