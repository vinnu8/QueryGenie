"""QueryGenie premium split-screen sign-in page (frontend prototype only).

The screen is split in two halves:

* **left** - the QueryGenie branding, the ``Sign In`` / ``Sign Up`` segmented
  control and the sign-in form,
* **right** - a decorative analytics showcase with floating dashboard previews.

``Sign Up`` is reserved for administrators: selecting the tab opens an
``Admin Access Only`` notice instead of a registration form.

Nothing in this module talks to MySQL, creates accounts, verifies credentials
or performs password recovery. The screen is a UI prototype only, therefore
the real admin-only registration flow has to be enforced by the backend later
on.
"""

from __future__ import annotations

import streamlit as st


TAB_SIGN_IN = "Sign In"
TAB_SIGN_UP = "Sign Up"

_TAB_KEY = "qg_auth_tab"
_ADMIN_DIALOG_KEY = "qg_admin_dialog_open"

_DIALOG_TITLE = "Admin Access Only"
_DIALOG_MESSAGE = (
    "Account registration is reserved for administrators. "
    "Employee accounts will be managed by an administrator."
)


# ===========================================================================
#  Session state helpers
# ===========================================================================
def _select_sign_in() -> None:
    """Activate the sign-in view and make sure no notice is left open."""
    st.session_state[_TAB_KEY] = TAB_SIGN_IN
    st.session_state[_ADMIN_DIALOG_KEY] = False


def _select_sign_up() -> None:
    """Sign up is admin only: raise the notice instead of showing a form."""
    st.session_state[_TAB_KEY] = TAB_SIGN_IN
    st.session_state[_ADMIN_DIALOG_KEY] = True


def _close_admin_dialog() -> None:
    """Dismiss the admin-only notice (button, close icon or escape key)."""
    st.session_state[_ADMIN_DIALOG_KEY] = False


def _markup(block: str) -> str:
    """Return an HTML block as one continuous raw markdown block.

    Blank lines are removed so the markdown parser keeps the whole snippet as
    a single raw HTML block (inline ``<svg>`` markup included) instead of
    turning indented fragments into code blocks.
    """
    return "\n".join(line for line in block.splitlines() if line.strip())


# ===========================================================================
#  Styles
# ===========================================================================
LOGIN_CSS = r"""
<style>
/* ============================================================ page shell */
html, body, [data-testid="stAppViewContainer"] {
    background: #EDF3F3 !important;
}

[data-testid="stMain"] {
    height: 100vh;
    height: 100dvh;
    overflow: hidden;
}

[data-testid="stMainBlockContainer"] {
    height: 100%;
    max-width: 100% !important;
    padding: 0 !important;
}

/* The theme stylesheet is injected as a markdown block above the split
   screen - it must not push the layout down. */
[data-testid="stMainBlockContainer"] > [data-testid="stVerticalBlock"] {
    gap: 0 !important;
    height: 100%;
}
[data-testid="stMainBlockContainer"] > [data-testid="stVerticalBlock"]
    > [data-testid="stElementContainer"] {
    height: 0 !important;
    overflow: hidden !important;
}
[data-testid="stMainBlockContainer"] > [data-testid="stVerticalBlock"]
    > [data-testid="stLayoutWrapper"] {
    height: 100%;
}

/* ------------------------------------------------------- split container */
.st-key-qg-shell {
    height: 100%;
    border-radius: 26px;
    overflow: hidden;
    background: #FFFFFF;
    border: 1px solid #E3E8E8;
    box-shadow: 0 30px 80px rgba(0, 63, 64, 0.16);
}
.st-key-qg-shell > [data-testid="stLayoutWrapper"] { height: 100%; }
.st-key-qg-shell > [data-testid="stLayoutWrapper"] > [data-testid="stHorizontalBlock"] {
    height: 100%;
    gap: 0 !important;
    align-items: stretch;
}
/* Only the two screen halves - nested column groups keep their own split. */
.st-key-qg-shell > [data-testid="stLayoutWrapper"] > [data-testid="stHorizontalBlock"]
    > [data-testid="stColumn"] { height: 100%; }
.st-key-qg-shell > [data-testid="stLayoutWrapper"] > [data-testid="stHorizontalBlock"]
    > [data-testid="stColumn"] > [data-testid="stVerticalBlock"] { height: 100%; }
.st-key-qg-shell > [data-testid="stLayoutWrapper"] > [data-testid="stHorizontalBlock"]
    > [data-testid="stColumn"] > [data-testid="stVerticalBlock"]
    > [data-testid="stLayoutWrapper"] { height: 100%; }

/* ====================================================== left: auth panel */
.st-key-qg-auth-panel {
    height: 100%;
    box-sizing: border-box;
    display: flex !important;
    flex-direction: column;
    gap: 0 !important;
    padding: 2.6rem 3.2rem 2.2rem;
    background: #FFFFFF;
    position: relative;
}
.st-key-qg-auth-panel > [data-testid="stElementContainer"] { flex: 0 0 auto; }
.st-key-qg-auth-panel > [data-testid="stLayoutWrapper"] { flex: 1 1 auto; min-height: 0; }

.st-key-qg-auth-main {
    height: 100%;
    display: flex !important;
    flex-direction: column;
    justify-content: center;
    gap: 0 !important;
}
.st-key-qg-auth-main > [data-testid="stElementContainer"] { flex: 0 0 auto; }
.st-key-qg-auth-main > [data-testid="stLayoutWrapper"] { flex: 0 0 auto; }

/* ---------------------------------------------------------------- brand */
.qg-brand {
    display: inline-flex;
    align-items: center;
    gap: 11px;
    animation: qgLeftIn 0.65s var(--qg-ease) both;
}
.qg-brand-mark {
    width: 40px;
    height: 40px;
    flex: 0 0 40px;
    border-radius: 13px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    color: #FFFFFF;
    background: linear-gradient(140deg, #168C91 0%, #0E6E73 100%);
    box-shadow: 0 10px 22px rgba(22, 140, 145, 0.28);
}
.qg-brand-mark svg { width: 22px; height: 22px; display: block; }
.qg-brand-name {
    font-size: 1.2rem;
    font-weight: 700;
    letter-spacing: -0.015em;
    color: #173536;
    line-height: 1.1;
}
.qg-brand-tag {
    display: block;
    margin-top: 2px;
    font-size: 0.7rem;
    font-weight: 500;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: #7B8588;
}

/* -------------------------------------------------------------- welcome */
.qg-welcome {
    text-align: center;
    margin-bottom: 1.6rem;
    animation: qgLeftIn 0.65s var(--qg-ease) 0.08s both;
}
.qg-welcome-title {
    margin: 0;
    font-size: 1.95rem;
    font-weight: 700;
    letter-spacing: -0.028em;
    line-height: 1.2;
    color: #173536;
}
.qg-welcome-text {
    margin: 0.55rem auto 0;
    max-width: 27rem;
    font-size: 0.95rem;
    line-height: 1.6;
    color: #7B8588;
}

/* ------------------------------------------------------ segmented tabs */
.st-key-qg-tabs {
    background: #E8F3F3;
    border: 1px solid #E3E8E8;
    border-radius: 15px;
    padding: 5px;
    gap: 5px !important;
    max-width: 24rem;
    margin: 0 auto 1.5rem;
    width: 100%;
    animation: qgLeftIn 0.65s var(--qg-ease) 0.16s both;
}
.st-key-qg-tabs [data-testid="stHorizontalBlock"] {
    gap: 5px !important;
    flex-wrap: nowrap !important;
}
.st-key-qg-tabs [data-testid="stColumn"] {
    min-width: 0 !important;
    width: auto !important;
    flex: 1 1 0% !important;
}
.st-key-qg-tabs [data-testid="stColumn"] > div { height: auto !important; }
.st-key-qg-tabs [data-testid="stButton"] button {
    min-width: 0 !important;
    width: 100% !important;
}

.st-key-qg-tabs [data-testid="stButton"] button {
    background: transparent !important;
    color: #7B8588 !important;
    border: 1px solid transparent !important;
    border-radius: 11px !important;
    box-shadow: none !important;
    font-size: 0.92rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.01em;
    padding: 0.55rem 0.5rem !important;
    transition: background 0.24s var(--qg-ease), color 0.24s var(--qg-ease),
                box-shadow 0.24s var(--qg-ease), transform 0.18s var(--qg-ease) !important;
}
.st-key-qg-tabs [data-testid="stButton"] button:hover {
    background: rgba(255, 255, 255, 0.62) !important;
    color: #003F40 !important;
    transform: none !important;
    box-shadow: none !important;
    filter: none !important;
}
.st-key-qg-tabs [data-testid="stButton"] button:focus-visible {
    outline: 2px solid rgba(22, 140, 145, 0.5) !important;
    outline-offset: 1px !important;
}

.st-key-qg-tab-signin-active [data-testid="stButton"] button,
.st-key-qg-tab-signup-active [data-testid="stButton"] button {
    background: #FFFFFF !important;
    color: #003F40 !important;
    border-color: #FFFFFF !important;
    box-shadow: 0 6px 16px rgba(0, 63, 64, 0.10) !important;
}
.st-key-qg-tab-signin-active [data-testid="stButton"] button:hover,
.st-key-qg-tab-signup-active [data-testid="stButton"] button:hover {
    background: #FFFFFF !important;
    color: #003F40 !important;
    transform: none !important;
    box-shadow: 0 8px 20px rgba(0, 63, 64, 0.14) !important;
    filter: none !important;
}

/* ----------------------------------------------------------- sign in form */
.st-key-qg-form {
    width: 100%;
    max-width: 24rem;
    margin: 0 auto;
    display: flex !important;
    flex-direction: column;
    gap: 0 !important;
    animation: qgLeftIn 0.65s var(--qg-ease) 0.24s both;
}
.st-key-qg-form [data-testid="stTextInput"] { margin-bottom: 0.3rem; }
.st-key-qg-form [data-testid="stTextInput"] label p {
    color: #173536 !important;
    font-size: 0.82rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.005em;
    margin-bottom: 0.35rem !important;
}
.st-key-qg-form [data-testid="stTextInput"] input {
    border-radius: 12px !important;
    border: 1px solid #E3E8E8 !important;
    background: #FFFFFF !important;
    color: #173536 !important;
    font-size: 0.93rem !important;
    padding: 0.66rem 0.85rem 0.66rem 2.55rem !important;
    box-shadow: 0 1px 2px rgba(23, 53, 54, 0.04) !important;
    transition: border-color 0.22s var(--qg-ease), box-shadow 0.22s var(--qg-ease) !important;
}
.st-key-qg-form [data-testid="stTextInput"] input:hover {
    border-color: #CFE0E0 !important;
}
.st-key-qg-form [data-testid="stTextInput"] input:focus {
    border-color: #168C91 !important;
    box-shadow: 0 0 0 3px rgba(22, 140, 145, 0.13) !important;
}
.st-key-qg-form [data-testid="stTextInput"] input::placeholder { color: #A9B3B5; }

/* The built-in reveal control of the password field. */
.st-key-qg-form [data-testid="stTextInput"] button {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    border-radius: 8px !important;
    color: #7B8588 !important;
    padding: 2px !important;
    transition: color 0.2s var(--qg-ease), background 0.2s var(--qg-ease) !important;
}
.st-key-qg-form [data-testid="stTextInput"] button:hover {
    background: #E8F3F3 !important;
    color: #168C91 !important;
}

.st-key-qg-submit { margin-top: 0.7rem; }
.st-key-qg-submit [data-testid="stButton"] button {
    background: linear-gradient(135deg, #1AA0A5 0%, #168D95 48%, #0F7B82 100%) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 12px !important;
    font-size: 0.95rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.02em;
    padding: 0.74rem 1rem !important;
    box-shadow: 0 12px 26px rgba(22, 140, 145, 0.30) !important;
    transition: transform 0.18s var(--qg-ease), box-shadow 0.18s var(--qg-ease),
                filter 0.18s var(--qg-ease) !important;
}
.st-key-qg-submit [data-testid="stButton"] button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 16px 32px rgba(22, 140, 145, 0.38) !important;
    filter: brightness(1.05) !important;
}
.st-key-qg-submit [data-testid="stButton"] button:active {
    transform: translateY(0) scale(0.99) !important;
    box-shadow: 0 8px 20px rgba(22, 140, 145, 0.30) !important;
}
.st-key-qg-submit [data-testid="stButton"] button:focus-visible {
    outline: 3px solid rgba(22, 140, 145, 0.35) !important;
    outline-offset: 2px !important;
}

/* ------------------------------------------------------- prototype notes */
.qg-alert {
    display: flex;
    align-items: flex-start;
    gap: 9px;
    margin-top: 0.9rem;
    padding: 0.7rem 0.85rem;
    border-radius: 12px;
    font-size: 0.83rem;
    line-height: 1.5;
    animation: qgLeftIn 0.45s var(--qg-ease) both;
}
.qg-alert svg { width: 16px; height: 16px; flex: 0 0 16px; margin-top: 1px; }
.qg-alert--info {
    background: #E8F3F3;
    border: 1px solid #CFE6E6;
    color: #0F5E62;
}
.qg-alert--warn {
    background: #FFF6E9;
    border: 1px solid #F2E0C0;
    color: #8A6216;
}

.qg-auth-foot {
    text-align: center;
    font-size: 0.78rem;
    line-height: 1.55;
    color: #9AA5A7;
    margin: 0;
    animation: qgLeftIn 0.65s var(--qg-ease) 0.32s both;
}
.qg-auth-foot strong { color: #6E7A7C; font-weight: 600; }

/* ================================================ right: analytics panel */
.st-key-qg-showcase {
    height: 100%;
    box-sizing: border-box;
    position: relative;
    overflow: hidden;
    display: flex !important;
    flex-direction: column;
    padding: 2.9rem 2.7rem 2.1rem;
    color: #FFFFFF;
    background:
        radial-gradient(640px 420px at 82% 4%, rgba(22, 140, 145, 0.55), transparent 62%),
        radial-gradient(520px 420px at 4% 98%, rgba(0, 53, 54, 0.85), transparent 66%),
        linear-gradient(158deg, #00494A 0%, #003F40 46%, #003536 100%);
}
.st-key-qg-showcase::before {
    content: "";
    position: absolute;
    inset: 0;
    pointer-events: none;
    opacity: 0.5;
    background-image:
        linear-gradient(rgba(255, 255, 255, 0.055) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255, 255, 255, 0.055) 1px, transparent 1px);
    background-size: 44px 44px;
    -webkit-mask-image: radial-gradient(120% 90% at 70% 20%, #000 0%, transparent 72%);
    mask-image: radial-gradient(120% 90% at 70% 20%, #000 0%, transparent 72%);
}
.st-key-qg-showcase::after {
    content: "";
    position: absolute;
    right: -170px;
    bottom: -190px;
    width: 460px;
    height: 460px;
    border-radius: 50%;
    border: 1px solid rgba(255, 255, 255, 0.10);
    pointer-events: none;
}
.st-key-qg-showcase > [data-testid="stElementContainer"] {
    flex: 1 1 auto;
    min-height: 0;
    display: flex;
    flex-direction: column;
}
.st-key-qg-showcase [data-testid="stMarkdownContainer"],
.st-key-qg-showcase [data-testid="stMarkdown"],
.st-key-qg-showcase [data-testid="stMarkdown"] > div {
    flex: 1 1 auto;
    min-height: 0;
    display: flex;
    flex-direction: column;
}
.st-key-qg-showcase [data-testid="stMarkdownContainer"] { margin: 0 !important; }

.qg-showcase {
    display: flex;
    flex-direction: column;
    flex: 1 1 auto;
    min-height: 0;
    position: relative;
    z-index: 1;
}

/* -------------------------------------------------------- floating cards */
.qg-stage {
    position: relative;
    height: 435px;
    flex: 0 0 auto;
    margin-bottom: 0.6rem;
}
.qg-card-wrap {
    position: absolute;
    animation: qgCardIn 0.75s var(--qg-ease) both;
}
.qg-card-wrap--sales    { top: 0;     left: 0;   width: 432px; z-index: 2; animation-delay: 0.12s; }
.qg-card-wrap--insights { top: 120px; left: 36%; width: 368px; z-index: 3; animation-delay: 0.26s; }
.qg-card-wrap--regions  { top: 235px; left: 1%;  width: 368px; z-index: 4; animation-delay: 0.4s; }

.qg-card {
    background: #FFFFFF;
    border-radius: 17px;
    border: 1px solid rgba(0, 63, 64, 0.06);
    box-shadow: 0 18px 38px rgba(0, 30, 31, 0.28);
    padding: 0.9rem 1.05rem 0.95rem;
    color: #173536;
    display: flex;
    flex-direction: column;
    animation: qgFloat 7.5s ease-in-out infinite alternate;
    transition: transform 0.3s var(--qg-ease), box-shadow 0.3s var(--qg-ease);
}
/* Every card keeps its own height budget and spreads its content evenly. */
.qg-card-wrap--sales .qg-card    { min-height: 168px; justify-content: space-between; }
.qg-card-wrap--insights .qg-card { min-height: 141px; justify-content: space-between; }
.qg-card-wrap--regions .qg-card  { min-height: 193px; }
.qg-card-wrap--regions .qg-regions { flex: 1 1 auto; justify-content: space-between; }
.qg-card-wrap--sales .qg-card    { animation-delay: 0.12s, 0.6s; }
.qg-card-wrap--insights .qg-card { animation-delay: 0.26s, 1.2s; }
.qg-card-wrap--regions .qg-card  { animation-delay: 0.4s, 0.9s; }
.qg-card:hover {
    transform: translateY(-6px);
    box-shadow: 0 26px 50px rgba(0, 30, 31, 0.34);
}

.qg-card-head {
    display: flex;
    align-items: center;
    gap: 7px;
    margin-bottom: 0.55rem;
}
.qg-card-title {
    font-size: 0.83rem;
    font-weight: 700;
    color: #173536;
    letter-spacing: -0.005em;
}
.qg-card-chip {
    margin-left: auto;
    font-size: 0.55rem;
    font-weight: 700;
    letter-spacing: 0.09em;
    text-transform: uppercase;
    color: #168C91;
    background: #E8F3F3;
    border-radius: 999px;
    padding: 3px 8px;
}
.qg-card-main {
    display: flex;
    align-items: center;
    gap: 0.9rem;
}
.qg-stat-label {
    display: block;
    font-size: 0.65rem;
    font-weight: 500;
    color: #8A9598;
    letter-spacing: 0.02em;
}
.qg-stat-value {
    display: block;
    margin-top: 1px;
    font-size: 1.14rem;
    font-weight: 700;
    letter-spacing: -0.02em;
    color: #0F3536;
}
.qg-card-stats { flex: 1 1 auto; min-width: 0; }

.qg-donut {
    width: 64px;
    height: 64px;
    flex: 0 0 64px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    background: conic-gradient(
        #168C91 0 46%,
        #35B3B8 46% 72%,
        #9BD3D6 72% 88%,
        #E9EFEF 88% 100%
    );
}
.qg-donut-hole {
    width: 44px;
    height: 44px;
    border-radius: 50%;
    background: #FFFFFF;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.65rem;
    font-weight: 700;
    color: #0F6E73;
}

.qg-progress {
    margin-top: 0.55rem;
    height: 5px;
    border-radius: 999px;
    background: #EDF2F2;
    overflow: hidden;
}
.qg-progress-fill {
    display: block;
    height: 100%;
    border-radius: 999px;
    background: linear-gradient(90deg, #168C91 0%, #35B3B8 100%);
}
.qg-legend {
    display: flex;
    flex-wrap: nowrap;
    gap: 12px;
    margin-top: 0.6rem;
}
.qg-legend-item {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    font-size: 0.56rem;
    color: #7B8588;
    white-space: nowrap;
}
.qg-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    display: inline-block;
    flex: 0 0 6px;
}
.qg-dot--a { background: #168C91; }
.qg-dot--b { background: #35B3B8; }
.qg-dot--c { background: #9BD3D6; }

.qg-insight-text {
    margin: 0.1rem 0 0;
    font-size: 0.72rem;
    line-height: 1.45;
    color: #5E6C6E;
}
.qg-trend {
    margin-left: auto;
    display: inline-flex;
    align-items: center;
    gap: 3px;
    font-size: 0.67rem;
    font-weight: 700;
    color: #0F7B82;
    background: #E8F3F3;
    border-radius: 999px;
    padding: 3px 8px;
}
.qg-progress-meta {
    display: flex;
    justify-content: flex-end;
    gap: 6px;
    margin-top: 0.35rem;
    font-size: 0.61rem;
    color: #8A9598;
}
.qg-progress-meta strong { color: #0F6E73; font-weight: 700; }

.qg-regions {
    list-style: none;
    margin: 0;
    padding: 0;
    display: flex;
    flex-direction: column;
    gap: 0.44rem;
}
.qg-regions li {
    display: grid;
    grid-template-columns: 52px 1fr 62px;
    align-items: center;
    gap: 8px;
}
.qg-region-name {
    font-size: 0.65rem;
    color: #5E6C6E;
    font-weight: 500;
}
.qg-region-bar {
    height: 5px;
    border-radius: 999px;
    background: #EDF2F2;
    overflow: hidden;
}
.qg-region-bar span {
    display: block;
    height: 100%;
    border-radius: 999px;
    background: linear-gradient(90deg, #168C91 0%, #46C0C4 100%);
}
.qg-region-value {
    font-size: 0.63rem;
    font-weight: 600;
    color: #0F3536;
    text-align: right;
}

/* ------------------------------------------------------------ promo block */
.qg-promo {
    flex: 1 1 auto;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 0.5rem 0 0.9rem;
    animation: qgLeftIn 0.7s var(--qg-ease) 0.5s both;
}
.qg-promo-tile {
    width: 54px;
    height: 54px;
    border-radius: 17px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    color: #FFFFFF;
    background: rgba(255, 255, 255, 0.12);
    border: 1px solid rgba(255, 255, 255, 0.22);
    box-shadow: 0 14px 30px rgba(0, 30, 31, 0.28);
    backdrop-filter: blur(6px);
    -webkit-backdrop-filter: blur(6px);
}
.qg-promo-tile svg { width: 26px; height: 26px; display: block; }
.qg-promo-title {
    margin: 1.05rem 0 0;
    max-width: 22rem;
    font-size: 1.42rem;
    font-weight: 700;
    letter-spacing: -0.022em;
    line-height: 1.28;
    color: #FFFFFF;
}
.qg-promo-text {
    margin: 0.6rem 0 0;
    max-width: 23rem;
    font-size: 0.88rem;
    line-height: 1.65;
    color: rgba(255, 255, 255, 0.72);
}
.qg-sample-note {
    margin: 0.9rem 0 0;
    text-align: center;
    font-size: 0.6rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: rgba(255, 255, 255, 0.38);
}

/* -------------------------------------------------- decorative segments */
.qg-segments {
    flex: 0 0 auto;
    display: flex;
    flex-direction: column;
    gap: 7px;
    margin-top: 0.6rem;
    animation: qgLeftIn 0.7s var(--qg-ease) 0.62s both;
}
.qg-segment {
    display: block;
    height: 3px;
    border-radius: 999px;
    background: rgba(255, 255, 255, 0.12);
    overflow: hidden;
}
.qg-segment span {
    display: block;
    height: 100%;
    border-radius: 999px;
    background: rgba(255, 255, 255, 0.34);
}
.qg-segment--a { width: 100%; }
.qg-segment--a span { width: 72%; background: linear-gradient(90deg, #35B3B8, rgba(53,179,184,.25)); }
.qg-segment--b { width: 82%; }
.qg-segment--b span { width: 58%; background: rgba(255,255,255,.28); }
.qg-segment--c { width: 64%; }
.qg-segment--c span { width: 46%; background: rgba(255,255,255,.22); }
.qg-segment--d { width: 44%; }
.qg-segment--d span { width: 34%; background: rgba(255,255,255,.18); }

/* =========================================================== admin modal */
/* The Streamlit dialog is a full screen overlay - the actual modal card is
   the section inside it. */
[data-testid="stDialog"] {
    background: rgba(0, 45, 46, 0.32) !important;
    border-radius: 0 !important;
    box-shadow: none !important;
    overflow: visible;
}
[data-testid="stDialog"] section {
    background: #FFFFFF;
    border-radius: 20px;
    box-shadow: 0 30px 70px rgba(0, 63, 64, 0.28) !important;
    position: relative;
    overflow: hidden;
}
/* A slim teal accent line along the top of the modal. */
[data-testid="stDialog"] section::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(90deg, #0F6E73 0%, #168C91 38%, #46C0C4 72%, rgba(70,192,196,.18) 100%);
}
[data-testid="stDialog"] [data-testid="stDialogIcon"] { color: #168C91 !important; }
[data-testid="stDialog"] h1,
[data-testid="stDialog"] h2,
[data-testid="stDialog"] h3 {
    color: #173536 !important;
    font-size: 1.15rem !important;
    font-weight: 700 !important;
    letter-spacing: -0.02em !important;
}
[data-testid="stDialog"] h2 p {
    color: #173536 !important;
    font-size: 1.15rem !important;
    font-weight: 700 !important;
}
.qg-admin-message {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    margin-top: 0.35rem;
}
.qg-admin-badge {
    flex: 0 0 38px;
    width: 38px;
    height: 38px;
    border-radius: 12px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    color: #FFFFFF;
    background: linear-gradient(140deg, #168C91 0%, #0F6E73 100%);
    box-shadow: 0 8px 18px rgba(22, 140, 145, 0.30);
}
.qg-admin-badge svg { width: 19px; height: 19px; display: block; }
.qg-admin-message p {
    color: #6E7A7C !important;
    font-size: 0.92rem !important;
    line-height: 1.6 !important;
    margin: 0 !important;
    padding-top: 2px;
}
.st-key-qg-gotit { margin-top: 1.1rem; }
.st-key-qg-gotit [data-testid="stButton"] button {
    background: linear-gradient(135deg, #1AA0A5 0%, #168D95 50%, #0F7B82 100%) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 12px !important;
    font-size: 0.92rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.02em;
    padding: 0.62rem 1rem !important;
    box-shadow: 0 12px 26px rgba(22, 140, 145, 0.30) !important;
    transition: transform 0.18s var(--qg-ease), box-shadow 0.18s var(--qg-ease),
                filter 0.18s var(--qg-ease) !important;
}
.st-key-qg-gotit [data-testid="stMarkdownContainer"] p {
    color: #FFFFFF !important;
    font-size: 0.92rem !important;
    font-weight: 600 !important;
}
.st-key-qg-gotit [data-testid="stButton"] button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 16px 32px rgba(22, 140, 145, 0.38) !important;
    filter: brightness(1.05) !important;
}
.st-key-qg-gotit [data-testid="stButton"] button:active {
    transform: translateY(0) scale(0.99) !important;
}
.st-key-qg-gotit [data-testid="stButton"] button:focus-visible {
    outline: 3px solid rgba(22, 140, 145, 0.35) !important;
    outline-offset: 2px !important;
}

/* =========================================================== animations */
@keyframes qgLeftIn {
    from { opacity: 0; transform: translateY(18px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes qgCardIn {
    from { opacity: 0; transform: translateY(22px) scale(0.96); }
    to   { opacity: 1; transform: translateY(0) scale(1); }
}
@keyframes qgFloat {
    from { translate: 0 -4px; }
    to   { translate: 0 5px; }
}
@keyframes qgDialogIn {
    from { opacity: 0; transform: translateY(14px) scale(0.98); }
    to   { opacity: 1; transform: translateY(0) scale(1); }
}
[data-testid="stDialog"] [data-testid="stDialogContent"],
[data-testid="stDialog"] > div { animation: qgDialogIn 0.4s var(--qg-ease) both; }

@media (prefers-reduced-motion: reduce) {
    .qg-brand, .qg-welcome, .st-key-qg-tabs, .st-key-qg-form, .qg-auth-foot,
    .qg-card-wrap, .qg-promo, .qg-segments, .qg-alert,
    [data-testid="stDialog"] [data-testid="stDialogContent"] {
        animation: none !important;
        opacity: 1 !important;
        transform: none !important;
        translate: none !important;
    }
    .qg-card { animation: none !important; }
}

/* ========================================================== responsive */
@media (max-width: 1100px) {
    .st-key-qg-auth-panel { padding: 2.2rem 2.1rem 1.9rem; }
    .st-key-qg-showcase { padding: 2.4rem 2rem 1.9rem; }
    .qg-stage { height: 390px; }
    .qg-card-wrap--sales    { width: 340px; }
    .qg-card-wrap--insights { width: 310px; left: 36%; top: 108px; }
    .qg-card-wrap--regions  { width: 312px; top: 212px; }
    .qg-card-wrap--sales .qg-card    { min-height: 150px; }
    .qg-card-wrap--insights .qg-card { min-height: 128px; }
    .qg-card-wrap--regions .qg-card  { min-height: 170px; }
    .qg-legend-item:nth-child(3) { display: none; }
}

@media (max-width: 900px) {
    [data-testid="stMain"] { height: auto; overflow: auto; }
    [data-testid="stMainBlockContainer"] { height: auto; padding: 0 0 1.2rem !important; }
    [data-testid="stMainBlockContainer"] > [data-testid="stVerticalBlock"] { height: auto; }
    [data-testid="stMainBlockContainer"] > [data-testid="stVerticalBlock"]
        > [data-testid="stLayoutWrapper"] { height: auto; }
    .st-key-qg-shell {
        height: auto;
        min-height: 0;
        border-radius: 22px;
        flex-direction: column;
    }
    .st-key-qg-shell > [data-testid="stLayoutWrapper"] { height: auto; }
    .st-key-qg-shell > [data-testid="stLayoutWrapper"] > [data-testid="stHorizontalBlock"] {
        height: auto;
        flex-direction: column;
        flex-wrap: nowrap !important;
    }
    .st-key-qg-shell > [data-testid="stLayoutWrapper"] > [data-testid="stHorizontalBlock"]
        > [data-testid="stColumn"] {
        width: 100% !important;
        flex: 0 0 auto !important;
        height: auto;
    }
    .st-key-qg-shell > [data-testid="stLayoutWrapper"] > [data-testid="stHorizontalBlock"]
        > [data-testid="stColumn"] > [data-testid="stVerticalBlock"],
    .st-key-qg-shell > [data-testid="stLayoutWrapper"] > [data-testid="stHorizontalBlock"]
        > [data-testid="stColumn"] > [data-testid="stVerticalBlock"]
        > [data-testid="stLayoutWrapper"] { height: auto; }

    .st-key-qg-auth-panel { min-height: 0; padding: 1.9rem 1.4rem 1.6rem; }
    .st-key-qg-auth-panel > [data-testid="stLayoutWrapper"] { flex: 0 0 auto; }
    .st-key-qg-auth-main { height: auto; padding: 1.4rem 0 0.6rem; }
    .st-key-qg-showcase { min-height: 0; padding: 1.9rem 1.4rem 1.6rem; }
    .st-key-qg-showcase > [data-testid="stElementContainer"] { flex: 0 0 auto; }
    .st-key-qg-showcase [data-testid="stMarkdownContainer"],
    .st-key-qg-showcase [data-testid="stMarkdown"],
    .st-key-qg-showcase [data-testid="stMarkdown"] > div { flex: 0 0 auto; }
    .qg-showcase { flex: 0 0 auto; }
    .qg-stage { height: 300px; }
    .qg-promo { padding: 0.6rem 0 0.9rem; }
    .qg-promo-title { font-size: 1.24rem; }
}

@media (max-width: 560px) {
    .qg-welcome-title { font-size: 1.6rem; }
    .st-key-qg-auth-panel { padding: 1.5rem 1.1rem 1.3rem; }
    .st-key-qg-showcase { padding: 1.6rem 1.1rem 1.4rem; }
    .qg-stage { height: 262px; }
    .qg-card-wrap--sales    { width: 230px; }
    .qg-card-wrap--insights { width: 190px; left: 45%; top: 112px; }
    .qg-card-wrap--regions  { display: none; }
    .qg-card-wrap--sales .qg-card    { min-height: 150px; }
    .qg-card-wrap--insights .qg-card { min-height: 140px; }
    .qg-card { padding: 0.72rem 0.85rem 0.78rem; border-radius: 15px; }
    .qg-legend { flex-wrap: nowrap; gap: 9px; }
    .qg-legend-item { font-size: 0.54rem; }
    .qg-legend-item:nth-child(3) { display: none; }
    .qg-stat-value { font-size: 1rem; }
    .qg-donut { width: 54px; height: 54px; flex: 0 0 54px; }
    .qg-donut-hole { width: 38px; height: 38px; }
    .qg-promo-title { font-size: 1.12rem; }
    .qg-promo-text { font-size: 0.82rem; }
}

/* Short laptop screens: shrink the floating previews so the promo block and
   the decorative segments still fit on the panel. */
@media (max-height: 820px) and (min-width: 901px) {
    .st-key-qg-showcase { padding: 2rem 2.2rem 1.6rem; }
    .qg-stage { height: 303px; }
    .qg-card-wrap { scale: 0.7; transform-origin: top left; }
    .qg-card-wrap--insights { top: 92px; left: 40%; }
    .qg-card-wrap--regions  { top: 176px; }
    .qg-promo { padding: 0.1rem 0 0.3rem; }
    .qg-promo-tile { width: 40px; height: 40px; border-radius: 13px; }
    .qg-promo-tile svg { width: 19px; height: 19px; }
    .qg-promo-title { font-size: 1.06rem; margin-top: 0.6rem; max-width: 20rem; }
    .qg-promo-text { font-size: 0.74rem; margin-top: 0.35rem; max-width: 22rem; }
    .qg-sample-note { margin-top: 0.45rem; font-size: 0.55rem; }
    .qg-segments { gap: 5px; margin-top: 0.35rem; }
}
</style>
"""


# ===========================================================================
#  Markup
# ===========================================================================
_BRAND_HTML = """
<div class="qg-brand">
    <span class="qg-brand-mark" aria-hidden="true">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7"
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
        <span class="qg-brand-tag">Business Analytics</span>
    </span>
</div>
"""

_WELCOME_HTML = """
<div class="qg-welcome">
    <h1 class="qg-welcome-title">Welcome to QueryGenie</h1>
    <p class="qg-welcome-text">
        Ask questions, explore your data, and discover meaningful business insights.
    </p>
</div>
"""

_FOOT_HTML = """
<p class="qg-auth-foot">
    <strong>QueryGenie</strong> &middot; AI powered database and business analytics.<br>
    Prototype interface &mdash; accounts are provisioned by your administrator.
</p>
"""

_ALERT_INFO_HTML = """
<div class="qg-alert qg-alert--info">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"
         stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="12" r="9"></circle>
        <path d="M12 11v5"></path>
        <path d="M12 7.6h.01"></path>
    </svg>
    <span>Authentication setup coming soon &mdash; this is a frontend prototype, so no
    account is created and no credentials are checked.</span>
</div>
"""

_ALERT_WARN_HTML = """
<div class="qg-alert qg-alert--warn">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"
         stroke-linecap="round" stroke-linejoin="round">
        <path d="M10.3 3.9L2.4 17.5A2 2 0 0 0 4.1 20.5h15.8a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0z"></path>
        <path d="M12 9v4"></path>
        <path d="M12 16.4h.01"></path>
    </svg>
    <span>{message}</span>
</div>
"""

_DIALOG_HTML = """
<div class="qg-admin-message">
    <span class="qg-admin-badge" aria-hidden="true">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"
             stroke-linecap="round" stroke-linejoin="round">
            <rect x="4.5" y="10" width="15" height="10" rx="2.2"></rect>
            <path d="M8 10V7.6a4 4 0 0 1 8 0V10"></path>
            <path d="M12 14v2.4"></path>
        </svg>
    </span>
    <p>{message}</p>
</div>
"""

_SHOWCASE_HTML = """
<div class="qg-showcase">
    <div class="qg-stage">
        <div class="qg-card-wrap qg-card-wrap--sales">
            <article class="qg-card">
                <header class="qg-card-head">
                    <span class="qg-card-title">Sales Overview</span>
                    <span class="qg-card-chip">Sample</span>
                </header>
                <div class="qg-card-main">
                    <div class="qg-donut" role="img" aria-label="Illustrative sales split">
                        <span class="qg-donut-hole">68%</span>
                    </div>
                    <div class="qg-card-stats">
                        <span class="qg-stat-label">Total sales</span>
                        <span class="qg-stat-value">&#8377;2,45,680</span>
                        <div class="qg-progress"><span class="qg-progress-fill" style="width:68%"></span></div>
                    </div>
                </div>
                <div class="qg-legend">
                    <span class="qg-legend-item"><i class="qg-dot qg-dot--a"></i>Electronics 46%</span>
                    <span class="qg-legend-item"><i class="qg-dot qg-dot--b"></i>Clothing 26%</span>
                    <span class="qg-legend-item"><i class="qg-dot qg-dot--c"></i>Other 28%</span>
                </div>
            </article>
        </div>
        <div class="qg-card-wrap qg-card-wrap--insights">
            <article class="qg-card">
                <header class="qg-card-head">
                    <span class="qg-card-title">Business Insights</span>
                    <span class="qg-trend">&#9650; 18.4%</span>
                </header>
                <p class="qg-insight-text">Revenue increased this period.</p>
                <div class="qg-progress" style="margin-top:0.6rem;"><span class="qg-progress-fill" style="width:74%"></span></div>
                <div class="qg-progress-meta">
                    <span>Target attainment</span>
                    <strong>74%</strong>
                </div>
            </article>
        </div>
        <div class="qg-card-wrap qg-card-wrap--regions">
            <article class="qg-card">
                <header class="qg-card-head">
                    <span class="qg-card-title">Regional Performance</span>
                    <span class="qg-card-chip">Sample</span>
                </header>
                <ul class="qg-regions">
                    <li>
                        <span class="qg-region-name">North</span>
                        <span class="qg-region-bar"><span style="width:86%"></span></span>
                        <span class="qg-region-value">&#8377;86,420</span>
                    </li>
                    <li>
                        <span class="qg-region-name">South</span>
                        <span class="qg-region-bar"><span style="width:68%"></span></span>
                        <span class="qg-region-value">&#8377;61,250</span>
                    </li>
                    <li>
                        <span class="qg-region-name">West</span>
                        <span class="qg-region-bar"><span style="width:47%"></span></span>
                        <span class="qg-region-value">&#8377;52,980</span>
                    </li>
                    <li>
                        <span class="qg-region-name">East</span>
                        <span class="qg-region-bar"><span style="width:32%"></span></span>
                        <span class="qg-region-value">&#8377;45,030</span>
                    </li>
                </ul>
            </article>
        </div>
    </div>
    <div class="qg-promo">
        <span class="qg-promo-tile" aria-hidden="true">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"
                 stroke-linecap="round" stroke-linejoin="round">
                <ellipse cx="10" cy="6" rx="6" ry="2.4"></ellipse>
                <path d="M4 6v5.2c0 1.33 2.7 2.4 6 2.4 1.1 0 2.1-.11 3-.33"></path>
                <path d="M4 11.2v5.2c0 1.33 2.7 2.4 6 2.4 1 0 1.9-.1 2.7-.27"></path>
                <path d="M19 2.2l.7 1.8 1.8.7-1.8.7-.7 1.8-.7-1.8-1.8-.7 1.8-.7z"
                      fill="currentColor" stroke="none"></path>
            </svg>
        </span>
        <h2 class="qg-promo-title">A Smarter Way to Understand Your Data</h2>
        <p class="qg-promo-text">
            Turn natural-language questions into actionable business insights with
            intelligent querying and analytics.
        </p>
        <p class="qg-sample-note">Illustrative preview data</p>
    </div>
    <div class="qg-segments" aria-hidden="true">
        <span class="qg-segment qg-segment--a"><span></span></span>
        <span class="qg-segment qg-segment--b"><span></span></span>
        <span class="qg-segment qg-segment--c"><span></span></span>
        <span class="qg-segment qg-segment--d"><span></span></span>
    </div>
</div>
"""


# ===========================================================================
#  Rendering
# ===========================================================================
@st.dialog(
    _DIALOG_TITLE,
    width="small",
    on_dismiss=_close_admin_dialog,
)
def _admin_only_dialog() -> None:
    """Show the admin-only notice raised by the Sign Up tab."""
    st.markdown(_markup(_DIALOG_HTML.format(message=_DIALOG_MESSAGE)), unsafe_allow_html=True)

    with st.container(key="qg-gotit"):
        if st.button("Got it", key="qg-admin-got-it", width="stretch"):
            st.session_state[_ADMIN_DIALOG_KEY] = False
            st.rerun()


def _render_tabs() -> None:
    """Render the Sign In / Sign Up segmented control."""
    active_tab = st.session_state[_TAB_KEY]

    with st.container(key="qg-tabs"):
        sign_in_col, sign_up_col = st.columns(2, gap="small")

        with sign_in_col:
            with st.container(
                key="qg-tab-signin-active" if active_tab == TAB_SIGN_IN else "qg-tab-signin-idle"
            ):
                st.button(
                    TAB_SIGN_IN,
                    key="qg-tab-sign-in",
                    width="stretch",
                    on_click=_select_sign_in,
                )

        with sign_up_col:
            with st.container(
                key="qg-tab-signup-active" if active_tab == TAB_SIGN_UP else "qg-tab-signup-idle"
            ):
                st.button(
                    TAB_SIGN_UP,
                    key="qg-tab-sign-up",
                    width="stretch",
                    on_click=_select_sign_up,
                )


def _render_sign_in_form() -> None:
    """Render the sign-in form. Nothing is submitted to a backend."""
    with st.container(key="qg-form"):
        st.text_input(
            "Email Address",
            placeholder="you@company.com",
            icon=":material/mail:",
            key="qg-email",
        )
        st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password",
            icon=":material/lock:",
            key="qg-password",
        )

        with st.container(key="qg-submit"):
            submitted = st.button("Sign In", type="primary", key="qg-sign-in", width="stretch")

    if not submitted:
        return

    email = (st.session_state.get("qg-email") or "").strip()
    password = st.session_state.get("qg-password") or ""

    if not email:
        st.markdown(
            _markup(_ALERT_WARN_HTML.format(message="Please enter your email address to sign in.")),
            unsafe_allow_html=True,
        )
    elif not password:
        st.markdown(
            _markup(_ALERT_WARN_HTML.format(message="Please enter your password to sign in.")),
            unsafe_allow_html=True,
        )
    else:
        st.markdown(_markup(_ALERT_INFO_HTML), unsafe_allow_html=True)


def _render_auth_panel() -> None:
    """Render the white authentication panel (left half of the screen)."""
    with st.container(key="qg-auth-panel"):
        st.markdown(_markup(_BRAND_HTML), unsafe_allow_html=True)

        with st.container(key="qg-auth-main"):
            st.markdown(_markup(_WELCOME_HTML), unsafe_allow_html=True)
            _render_tabs()
            _render_sign_in_form()

        st.markdown(_markup(_FOOT_HTML), unsafe_allow_html=True)


def _render_showcase() -> None:
    """Render the teal analytics showcase (right half of the screen)."""
    with st.container(key="qg-showcase"):
        st.markdown(_markup(_SHOWCASE_HTML), unsafe_allow_html=True)


def render_login() -> None:
    """Render the frontend-only split-screen login page prototype."""
    st.html(LOGIN_CSS)

    if _TAB_KEY not in st.session_state:
        st.session_state[_TAB_KEY] = TAB_SIGN_IN
    if _ADMIN_DIALOG_KEY not in st.session_state:
        st.session_state[_ADMIN_DIALOG_KEY] = False

    with st.container(key="qg-shell"):
        auth_panel, showcase = st.columns([48, 52], gap="small", vertical_alignment="center")

        with auth_panel:
            _render_auth_panel()

        with showcase:
            _render_showcase()

    if st.session_state[_ADMIN_DIALOG_KEY]:
        _admin_only_dialog()
