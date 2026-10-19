"""QueryGenie login page prototype (frontend only, no authentication).

This module renders the split-screen login experience only:

* the left panel carries the QueryGenie branding and a *visual* Admin/Employee
  mode selector,
* the right panel carries the sign-in form.

Nothing here talks to MySQL, creates accounts, verifies credentials or performs
password recovery. The mode selector is a cosmetic control: it never grants or
verifies any permission.
"""

from __future__ import annotations

import streamlit as st


ADMIN_MODE = "Admin"
EMPLOYEE_MODE = "Employee"

_MODE_DETAILS: dict[str, dict[str, str]] = {
    ADMIN_MODE: {
        "label": "Admin Mode",
        "description": "Manage records and explore business analytics.",
        "icon": ":material/admin_panel_settings:",
    },
    EMPLOYEE_MODE: {
        "label": "Employee Mode",
        "description": "Explore data, run queries, and discover insights.",
        "icon": ":material/groups:",
    },
}

_MODE_STATE_KEY = "login_mode"


LOGIN_CSS = r"""
<style>
/* ============================================================ page shell */
html, body, [data-testid="stAppViewContainer"] {
    background: var(--qg-bg-alt) !important;
}

[data-testid="stMain"] {
    height: 100vh;
    height: 100dvh;
    overflow: auto;
}

[data-testid="stMainBlockContainer"] {
    height: 100%;
    max-width: 100% !important;
    padding: 0 !important;
}

[data-testid="stMainBlockContainer"] > div { height: 100%; }

/* The two theme/CSS markdown blocks live in the root vertical block and would
   otherwise add a 16px gap above the split screen. */
[data-testid="stMainBlockContainer"] > [data-testid="stVerticalBlock"] {
    gap: 0 !important;
}

/* The screen split itself: root block > layout wrapper > row > two columns. */
[data-testid="stMainBlockContainer"] > [data-testid="stVerticalBlock"]
    > [data-testid="stLayoutWrapper"] > [data-testid="stHorizontalBlock"] {
    height: 100%;
    gap: 0 !important;
    align-items: stretch;
}
[data-testid="stMainBlockContainer"] > [data-testid="stVerticalBlock"]
    > [data-testid="stLayoutWrapper"] > [data-testid="stHorizontalBlock"]
    > [data-testid="stColumn"] {
    height: 100%;
}
[data-testid="stColumn"] > div { height: 100%; }
[data-testid="stColumn"] > div > div { height: 100%; }

/* ====================================================== left brand panel */
.st-key-qg-left-panel {
    position: relative;
    overflow: hidden;
    box-sizing: border-box;
    height: 100%;
    min-height: 100vh;
    min-height: 100dvh;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    gap: 1.1rem;
    padding: 3.4rem 3.2rem;
    color: #FFFFFF;
    background:
        radial-gradient(760px 420px at 88% 8%, rgba(96, 165, 250, 0.55), transparent 62%),
        radial-gradient(560px 420px at 6% 96%, rgba(9, 33, 110, 0.55), transparent 64%),
        linear-gradient(158deg, #2E63EE 0%, #2457E6 34%, #1E4BD8 66%, #173DB5 100%);
    border-radius: 0 150px 150px 0 / 0 50% 50% 0;
    box-shadow: 0 26px 70px rgba(23, 61, 181, 0.26);
}

.st-key-qg-left-panel::before {
    content: "";
    position: absolute;
    inset: 0;
    z-index: 0;
    pointer-events: none;
    opacity: 0.5;
    background-image: radial-gradient(rgba(255, 255, 255, 0.30) 1px, transparent 1px);
    background-size: 26px 26px;
    -webkit-mask-image: radial-gradient(120% 90% at 82% 22%, #000 0%, transparent 72%);
    mask-image: radial-gradient(120% 90% at 82% 22%, #000 0%, transparent 72%);
}

.st-key-qg-left-panel::after {
    content: "";
    position: absolute;
    z-index: 0;
    pointer-events: none;
    right: -190px;
    top: 50%;
    width: 560px;
    height: 560px;
    transform: translateY(-50%);
    border-radius: 50%;
    border: 1px solid rgba(255, 255, 255, 0.16);
}

.st-key-qg-left-panel > * { position: relative; z-index: 1; flex-shrink: 0; }

.qg-brand {
    display: flex;
    align-items: center;
    gap: 16px;
    margin-bottom: 0.35rem;
}
.qg-brand-mark {
    width: 54px;
    height: 54px;
    flex: 0 0 54px;
    border-radius: 17px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    color: #FFFFFF;
    background: rgba(255, 255, 255, 0.14);
    border: 1px solid rgba(255, 255, 255, 0.28);
    box-shadow: 0 14px 30px rgba(9, 33, 110, 0.28);
    backdrop-filter: blur(6px);
    -webkit-backdrop-filter: blur(6px);
}
.qg-brand-mark svg { width: 28px; height: 28px; }
.qg-brand-name {
    display: block;
    font-size: 2.05rem;
    font-weight: 800;
    letter-spacing: -0.025em;
    line-height: 1.1;
    color: #FFFFFF;
}
.qg-brand-tagline {
    display: block;
    margin-top: 3px;
    font-size: 0.95rem;
    font-weight: 500;
    color: rgba(255, 255, 255, 0.82);
    letter-spacing: 0.01em;
}

.qg-lead {
    margin: 0.2rem 0 0;
    max-width: 30rem;
    font-size: 1.02rem;
    line-height: 1.65;
    font-weight: 400;
    color: rgba(255, 255, 255, 0.88);
}

.qg-chips {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin-top: 0.5rem;
}
.qg-chip {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    padding: 7px 13px 7px 10px;
    border-radius: 999px;
    font-size: 0.82rem;
    font-weight: 500;
    color: rgba(255, 255, 255, 0.92);
    background: rgba(255, 255, 255, 0.13);
    border: 1px solid rgba(255, 255, 255, 0.22);
}
.qg-chip svg { width: 15px; height: 15px; flex: 0 0 15px; color: #BFDBFE; }

/* ------------------------------------------------------- mode selector */
.qg-mode-block { margin-top: 0; }

.qg-mode-heading {
    display: flex;
    flex-direction: column;
    gap: 2px;
    margin-bottom: 0.75rem;
}
.qg-mode-title {
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: rgba(255, 255, 255, 0.95);
}
.qg-mode-hint {
    font-size: 0.86rem;
    color: rgba(255, 255, 255, 0.72);
}

.st-key-qg-mode-switch {
    max-width: 460px;
    background: rgba(255, 255, 255, 0.13);
    border: 1px solid rgba(255, 255, 255, 0.22);
    border-radius: 17px;
    padding: 6px;
    gap: 6px !important;
    box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.18);
}
.st-key-qg-mode-switch [data-testid="stHorizontalBlock"] { gap: 6px !important; }
/* Keep the two mode options side by side even on narrow screens. */
.st-key-qg-mode-switch [data-testid="stColumn"] { min-width: 0 !important; }

.st-key-qg-mode-switch [data-testid="stButton"] button {
    background: transparent !important;
    color: rgba(255, 255, 255, 0.84) !important;
    border: 1px solid transparent !important;
    border-radius: 12px !important;
    box-shadow: none !important;
    font-size: 0.9rem !important;
    font-weight: 600 !important;
    padding: 0.5rem 0.5rem !important;
    gap: 6px !important;
    transition: background 0.22s var(--qg-ease), color 0.22s var(--qg-ease),
                box-shadow 0.22s var(--qg-ease), transform 0.18s var(--qg-ease) !important;
}
.st-key-qg-mode-switch [data-testid="stButton"] button:hover {
    background: rgba(255, 255, 255, 0.14) !important;
    color: #FFFFFF !important;
    transform: none !important;
    box-shadow: none !important;
    filter: none !important;
}

.st-key-qg-mode-admin-active [data-testid="stButton"] button,
.st-key-qg-mode-employee-active [data-testid="stButton"] button {
    background: #FFFFFF !important;
    color: var(--qg-primary) !important;
    border-color: #FFFFFF !important;
    box-shadow: 0 10px 24px rgba(9, 33, 110, 0.26) !important;
}
.st-key-qg-mode-admin-active [data-testid="stButton"] button:hover,
.st-key-qg-mode-employee-active [data-testid="stButton"] button:hover {
    background: #FFFFFF !important;
    color: var(--qg-primary-dark) !important;
    transform: none !important;
    box-shadow: 0 12px 26px rgba(9, 33, 110, 0.30) !important;
    filter: none !important;
}

@keyframes qgModeDescIn {
    from { opacity: 0; transform: translateY(6px); }
    to   { opacity: 1; transform: translateY(0); }
}
.qg-mode-desc {
    display: flex;
    align-items: center;
    gap: 9px;
    margin: 0.85rem 0 0;
    font-size: 0.9rem;
    font-weight: 500;
    color: rgba(255, 255, 255, 0.9);
    animation: qgModeDescIn 0.45s var(--qg-ease) both;
}
.qg-mode-desc--admin { animation-name: qgModeDescIn; }
.qg-mode-desc--employee { animation-name: qgModeDescIn; }
.qg-mode-desc-dot {
    width: 7px;
    height: 7px;
    flex: 0 0 7px;
    border-radius: 50%;
    background: #BFDBFE;
    box-shadow: 0 0 0 4px rgba(191, 219, 254, 0.18);
}

.qg-mode-note {
    margin: 0.7rem 0 0;
    font-size: 0.78rem;
    line-height: 1.5;
    color: rgba(255, 255, 255, 0.62);
}

/* ========================================================= right: card */
.st-key-qg-login-wrap {
    min-height: 100vh;
    min-height: 100dvh;
    display: flex;
    flex-direction: column;
    align-items: stretch;
    justify-content: center;
    gap: 1rem;
    padding: 2.5rem 1.5rem;
    box-sizing: border-box;
}

.st-key-qg-login-card {
    width: 100%;
    max-width: 460px;
    margin: 0 auto;
    background: #FFFFFF;
    border: 1px solid var(--qg-border);
    border-radius: 22px;
    padding: 2.35rem 2.3rem 2rem;
    box-shadow: 0 24px 60px rgba(23, 61, 181, 0.10);
    animation: qgFadeSlideUp 0.65s var(--qg-ease) both;
}

.qg-card-head { margin-bottom: 1.5rem; }
.qg-card-title {
    margin: 0;
    font-size: 1.85rem;
    font-weight: 800;
    letter-spacing: -0.025em;
    color: var(--qg-text);
}
.qg-card-sub {
    margin: 0.4rem 0 0;
    font-size: 0.94rem;
    line-height: 1.55;
    color: var(--qg-text-muted);
}

.st-key-qg-login-card [data-testid="stTextInput"] label p {
    color: #475569 !important;
    font-size: 0.8rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.01em;
}
.st-key-qg-login-card [data-testid="stTextInput"] input {
    border-radius: 12px !important;
    border: 1px solid var(--qg-border) !important;
    background: #FFFFFF !important;
    color: var(--qg-text) !important;
    font-size: 0.95rem !important;
    padding: 0.66rem 0.9rem !important;
    box-shadow: 0 1px 2px rgba(23, 32, 51, 0.04) !important;
}
.st-key-qg-login-card [data-testid="stTextInput"] input:focus {
    border-color: var(--qg-primary) !important;
    box-shadow: 0 0 0 3px rgba(36, 87, 230, 0.14) !important;
}
.st-key-qg-login-card [data-testid="stTextInput"] input::placeholder { color: #94A3B8; }

/* Help + reveal affordances inside the inputs stay quiet until hovered. */
.st-key-qg-login-card [data-testid="stTextInput"] button {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    border-radius: 8px !important;
    color: #A9B6CA !important;
    padding: 2px !important;
    transition: color 0.2s var(--qg-ease), background 0.2s var(--qg-ease);
}
.st-key-qg-login-card [data-testid="stTextInput"] button:hover {
    background: #EEF3FD !important;
    color: var(--qg-primary) !important;
}

.st-key-qg-login-card [data-testid="stCheckbox"] label {
    color: var(--qg-text-muted) !important;
    font-size: 0.86rem !important;
    font-weight: 500 !important;
}
.st-key-qg-login-card [data-testid="stCheckbox"] svg { color: var(--qg-primary); }

.qg-forgot {
    text-align: right;
    font-size: 0.86rem;
    font-weight: 500;
    color: var(--qg-primary);
    cursor: default;
}

.st-key-qg-signin [data-testid="stButton"] button {
    background: linear-gradient(135deg, #2E63EE 0%, #2457E6 45%, #173DB5 100%) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 12px !important;
    font-size: 1rem !important;
    font-weight: 650 !important;
    letter-spacing: 0.01em;
    padding: 0.78rem 1rem !important;
    box-shadow: 0 14px 30px rgba(36, 87, 230, 0.30) !important;
}
.st-key-qg-signin [data-testid="stButton"] button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 18px 36px rgba(36, 87, 230, 0.38) !important;
    filter: none !important;
}

.st-key-qg-login-card [data-testid="stAlert"] {
    margin-top: 0.2rem;
    background: var(--qg-bg-alt) !important;
    border: 1px solid var(--qg-border-hover) !important;
    border-radius: 12px !important;
    padding: 0.35rem 0.85rem !important;
}
.st-key-qg-login-card [data-testid="stAlert"] > div {
    background: transparent !important;
    border-radius: 11px !important;
    padding: 0.45rem 0 !important;
}
.st-key-qg-login-card [data-testid="stAlert"] svg { color: var(--qg-primary) !important; }
.st-key-qg-login-card [data-testid="stAlert"] [data-testid="stMarkdownContainer"] p {
    color: var(--qg-primary-dark) !important;
    font-size: 0.85rem !important;
    line-height: 1.55 !important;
}

.qg-card-hint {
    margin-top: 1.15rem;
    padding: 0.7rem 0.9rem;
    border-radius: 12px;
    background: var(--qg-bg-alt);
    border: 1px solid var(--qg-border);
    font-size: 0.82rem;
    line-height: 1.5;
    color: var(--qg-text-muted);
    text-align: center;
}

.st-key-qg-login-wrap .qg-note {
    max-width: 460px;
    margin: 0 auto;
}

/* ========================================================== responsive */
@media (max-width: 1200px) {
    .st-key-qg-login-card { max-width: 420px; }
}

@media (max-width: 900px) {
    [data-testid="stMain"] { overflow: auto; }
    [data-testid="stMainBlockContainer"] > [data-testid="stVerticalBlock"]
        > [data-testid="stLayoutWrapper"] > [data-testid="stHorizontalBlock"] {
        flex-direction: column;
        flex-wrap: nowrap !important;
        height: auto;
    }
    /* Only the two screen halves stack - nested column groups keep their split. */
    [data-testid="stMainBlockContainer"] > [data-testid="stVerticalBlock"]
        > [data-testid="stLayoutWrapper"] > [data-testid="stHorizontalBlock"]
        > [data-testid="stColumn"] {
        width: 100% !important;
        flex: 0 0 auto !important;
        height: auto;
    }
    [data-testid="stColumn"] > div,
    [data-testid="stColumn"] > div > div { height: auto; }
    .st-key-qg-left-panel {
        min-height: 0;
        height: auto;
        border-radius: 0 0 44px 44px / 0 0 26px 26px;
        padding: 2.4rem 1.6rem;
    }
    .qg-mode-block { margin-top: 1.6rem; }
    .st-key-qg-login-wrap { min-height: 0; padding: 2rem 1.1rem 2.6rem; }
    .qg-brand-name { font-size: 1.7rem; }
    .qg-card-title { font-size: 1.6rem; }
    .st-key-qg-login-card { padding: 1.8rem 1.4rem 1.5rem; }
}
</style>
"""


_BRAND_HTML = """
<div class="qg-brand">
    <span class="qg-brand-mark" aria-hidden="true">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"
             stroke-linecap="round" stroke-linejoin="round">
            <ellipse cx="9.2" cy="5.9" rx="6.2" ry="2.4"></ellipse>
            <path d="M3 5.9v5.3c0 1.33 2.77 2.4 6.2 2.4 1.15 0 2.22-.13 3.14-.37"></path>
            <path d="M3 11.2v5.3c0 1.33 2.77 2.4 6.2 2.4 1.04 0 2.02-.11 2.84-.29"></path>
            <path d="M19 1.7l.86 2.1 2.1.86-2.1.86-.86 2.1-.86-2.1-2.1-.86 2.1-.86z"
                  fill="currentColor" stroke="none"></path>
        </svg>
    </span>
    <span>
        <span class="qg-brand-name">QueryGenie</span>
        <span class="qg-brand-tagline">Ask your data. Discover what matters.</span>
    </span>
</div>
<p class="qg-lead">
    Turn natural-language questions into meaningful business insights with
    intelligent database analytics.
</p>
<div class="qg-chips">
    <span class="qg-chip">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9"
             stroke-linecap="round" stroke-linejoin="round">
            <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
        </svg>
        Natural-language queries
    </span>
    <span class="qg-chip">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9"
             stroke-linecap="round" stroke-linejoin="round">
            <path d="M3 3v18h18"></path>
            <path d="M7 15l4-5 3 3 5-7"></path>
        </svg>
        Business analytics
    </span>
    <span class="qg-chip">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9"
             stroke-linecap="round" stroke-linejoin="round">
            <path d="M13 2L3 14h8l-1 8 10-12h-8z"></path>
        </svg>
        Instant insights
    </span>
</div>
"""

_MODE_HEADING_HTML = """
<div class="qg-mode-heading">
    <span class="qg-mode-title">Workspace mode</span>
    <span class="qg-mode-hint">Pick the view that fits how you work today.</span>
</div>
"""

_CARD_HEAD_HTML = """
<div class="qg-card-head">
    <h2 class="qg-card-title">Welcome back</h2>
    <p class="qg-card-sub">
        Sign in to your QueryGenie workspace to explore your data and uncover
        what matters.
    </p>
</div>
"""


def _set_mode(mode: str) -> None:
    """Store the visually selected mode (no permissions are implied)."""
    st.session_state[_MODE_STATE_KEY] = mode


def _render_brand_panel() -> None:
    """Render the royal-blue branding panel with the mode selector."""
    mode = st.session_state[_MODE_STATE_KEY]
    details = _MODE_DETAILS[mode]

    with st.container(key="qg-left-panel"):
        st.markdown(_BRAND_HTML, unsafe_allow_html=True)

        with st.container(key="qg-mode-block"):
            st.markdown(_MODE_HEADING_HTML, unsafe_allow_html=True)

            with st.container(key="qg-mode-switch"):
                admin_col, employee_col = st.columns(2, gap="small")

                with admin_col:
                    with st.container(
                        key="qg-mode-admin-active"
                        if mode == ADMIN_MODE
                        else "qg-mode-admin-idle"
                    ):
                        st.button(
                            _MODE_DETAILS[ADMIN_MODE]["label"],
                            icon=_MODE_DETAILS[ADMIN_MODE]["icon"],
                            key="qg-mode-admin",
                            width="stretch",
                            on_click=_set_mode,
                            args=(ADMIN_MODE,),
                        )

                with employee_col:
                    with st.container(
                        key="qg-mode-employee-active"
                        if mode == EMPLOYEE_MODE
                        else "qg-mode-employee-idle"
                    ):
                        st.button(
                            _MODE_DETAILS[EMPLOYEE_MODE]["label"],
                            icon=_MODE_DETAILS[EMPLOYEE_MODE]["icon"],
                            key="qg-mode-employee",
                            width="stretch",
                            on_click=_set_mode,
                            args=(EMPLOYEE_MODE,),
                        )

            st.markdown(
                f'<p class="qg-mode-desc qg-mode-desc--{mode.lower()}">'
                f'<span class="qg-mode-desc-dot"></span>{details["description"]}</p>',
                unsafe_allow_html=True,
            )
            st.markdown(
                '<p class="qg-mode-note">Preview only &mdash; the mode selector does not '
                "authenticate anyone or apply any permission.</p>",
                unsafe_allow_html=True,
            )


def _render_login_card() -> None:
    """Render the white sign-in card (frontend only, nothing is verified)."""
    with st.container(key="qg-login-wrap"):
        with st.container(key="qg-login-card"):
            st.markdown(_CARD_HEAD_HTML, unsafe_allow_html=True)

            st.text_input(
                "Email or username",
                placeholder="you@company.com",
                help="UI-only field; no credentials are checked.",
                key="login_username",
            )

            st.text_input(
                "Password",
                type="password",
                placeholder="Enter your password",
                help="UI-only field; no credentials are checked.",
                key="login_password",
            )

            remember_col, forgot_col = st.columns(
                [1, 1], gap="small", vertical_alignment="center"
            )
            with remember_col:
                st.checkbox("Remember me", key="login_remember")
            with forgot_col:
                st.markdown(
                    '<div class="qg-forgot" title="Password recovery is not available in '
                    'this prototype.">Forgot password?</div>',
                    unsafe_allow_html=True,
                )

            sign_in_clicked = st.button(
                "Sign in",
                type="primary",
                key="qg-signin",
                width="stretch",
            )

            if sign_in_clicked:
                # Prototype only: nothing is authenticated and no account is created.
                st.info(
                    "Authentication setup coming soon. No account is created and no "
                    "credentials are checked in this prototype."
                )

            st.markdown(
                '<div class="qg-card-hint">Accounts are provisioned by your QueryGenie '
                "administrator &mdash; ask them for access.</div>",
                unsafe_allow_html=True,
            )

        st.markdown(
            '<p class="qg-note"><span class="qg-dot"></span>'
            "Authentication setup coming soon &mdash; this login screen is a frontend "
            "prototype only.</p>",
            unsafe_allow_html=True,
        )


def render_login() -> None:
    """Render the frontend-only split-screen login page prototype."""
    st.markdown(LOGIN_CSS, unsafe_allow_html=True)

    if _MODE_STATE_KEY not in st.session_state:
        st.session_state[_MODE_STATE_KEY] = ADMIN_MODE

    left_panel, right_panel = st.columns(
        [46, 54], gap="small", vertical_alignment="center"
    )

    with left_panel:
        _render_brand_panel()

    with right_panel:
        _render_login_card()
