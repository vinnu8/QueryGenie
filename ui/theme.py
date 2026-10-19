"""Shared visual theme for the QueryGenie UI prototypes.

The palette is intentionally light: white surfaces, a very light blue canvas and
royal-blue accents. Dark panels and neon-on-black styling are avoided on purpose
so the UI keeps a premium, modern SaaS feel.
"""

from __future__ import annotations

import streamlit as st


CUSTOM_CSS = r"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

:root {
    --qg-bg: #FFFFFF;
    --qg-bg-alt: #F5F8FF;
    --qg-surface: #FFFFFF;
    --qg-primary: #2457E6;
    --qg-primary-dark: #173DB5;
    --qg-secondary: #60A5FA;
    --qg-text: #172033;
    --qg-text-muted: #64748B;
    --qg-border: #E2E8F0;
    --qg-border-hover: #BFD4FB;
    --qg-shadow: 0 10px 40px rgba(36, 87, 230, 0.08);
    --qg-shadow-hover: 0 18px 50px rgba(36, 87, 230, 0.16);
    --qg-radius-lg: 20px;
    --qg-radius-md: 14px;
    --qg-radius-sm: 10px;
    --qg-ease: cubic-bezier(0.22, 1, 0.36, 1);
}

html, body, [data-testid="stAppViewContainer"] {
    background:
        radial-gradient(1000px 600px at 15% -10%, rgba(96, 165, 250, 0.12), transparent 60%),
        radial-gradient(900px 600px at 85% 110%, rgba(36, 87, 230, 0.10), transparent 60%),
        var(--qg-bg) !important;
    color: var(--qg-text);
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

[data-testid="stAppViewContainer"] > .main {
    background: transparent !important;
}

[data-testid="stHeader"],
[data-testid="stToolbar"],
[data-testid="stDecoration"],
footer,
#MainMenu {
    display: none !important;
    visibility: hidden !important;
}

.block-container {
    padding-top: 2.5rem !important;
    padding-bottom: 3rem !important;
    max-width: 920px !important;
}

@keyframes qgFadeSlideUp {
    from { opacity: 0; transform: translateY(22px); }
    to   { opacity: 1; transform: translateY(0); }
}

@keyframes qgDotPulse {
    0%, 100% { opacity: 0.55; transform: scale(0.9); }
    50%      { opacity: 1; transform: scale(1.1); }
}

.qg-entrance {
    animation: qgFadeSlideUp 0.7s var(--qg-ease) both;
}
.qg-delay-1 { animation-delay: 0.05s; }
.qg-delay-2 { animation-delay: 0.15s; }
.qg-delay-3 { animation-delay: 0.28s; }
.qg-delay-4 { animation-delay: 0.42s; }

@media (prefers-reduced-motion: reduce) {
    .qg-entrance { animation: none !important; opacity: 1 !important; transform: none !important; }
    * { transition-duration: 0.01ms !important; }
}

/* ------------------------------------------------------------------ brand */
.qg-header {
    text-align: center;
    margin-bottom: 2.2rem;
}
.qg-logo {
    display: inline-flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 0.35rem;
}
.qg-icon {
    width: 40px;
    height: 40px;
    border-radius: 12px;
    background: linear-gradient(135deg, var(--qg-primary), var(--qg-secondary));
    display: inline-flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 8px 24px rgba(36, 87, 230, 0.28);
    color: #FFFFFF;
}
.qg-icon svg { width: 22px; height: 22px; }
.qg-wordmark {
    font-size: 1.85rem;
    font-weight: 800;
    letter-spacing: -0.02em;
    background: linear-gradient(135deg, var(--qg-primary), var(--qg-secondary));
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
}
.qg-subtitle {
    color: var(--qg-text-muted);
    font-size: 0.98rem;
    font-weight: 500;
    margin: 0;
}

/* ------------------------------------------------------------ form fields */
[data-testid="stVerticalBlockBorderWrapper"] {
    background: var(--qg-surface) !important;
    border: 1px solid var(--qg-border) !important;
    border-radius: var(--qg-radius-lg) !important;
    padding: 1.7rem 1.7rem 1.4rem !important;
    box-shadow: var(--qg-shadow) !important;
    animation: qgFadeSlideUp 0.7s var(--qg-ease) both;
    animation-delay: 0.42s;
    transition: border-color 0.24s var(--qg-ease), box-shadow 0.24s var(--qg-ease);
}
[data-testid="stVerticalBlockBorderWrapper"]:hover {
    border-color: var(--qg-border-hover);
    box-shadow: var(--qg-shadow-hover);
}

[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input {
    border-radius: var(--qg-radius-sm) !important;
    border: 1px solid var(--qg-border) !important;
    background: #FFFFFF !important;
    color: var(--qg-text) !important;
    padding: 0.6rem 0.85rem !important;
    transition: border-color 0.2s var(--qg-ease), box-shadow 0.2s var(--qg-ease);
}
[data-testid="stTextInput"] input:focus {
    border-color: var(--qg-primary) !important;
    box-shadow: 0 0 0 3px rgba(36, 87, 230, 0.15) !important;
    outline: none !important;
}
[data-testid="stTextInput"] label,
[data-testid="stCheckbox"] label {
    color: var(--qg-text) !important;
    font-weight: 500 !important;
    font-size: 0.92rem !important;
}

[data-testid="stButton"] button {
    background: linear-gradient(135deg, var(--qg-primary), var(--qg-secondary)) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: var(--qg-radius-sm) !important;
    font-weight: 600 !important;
    padding: 0.62rem 1.1rem !important;
    box-shadow: 0 8px 24px rgba(36, 87, 230, 0.28) !important;
    transition: transform 0.18s var(--qg-ease), box-shadow 0.18s var(--qg-ease), filter 0.18s var(--qg-ease) !important;
}
[data-testid="stButton"] button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 12px 30px rgba(36, 87, 230, 0.36) !important;
    filter: brightness(1.06) !important;
}
[data-testid="stButton"] button:active {
    transform: translateY(0) scale(0.985) !important;
}
[data-testid="stButton"] button:focus-visible {
    outline: 3px solid rgba(36, 87, 230, 0.35) !important;
    outline-offset: 2px !important;
}

/* ----------------------------------------------------------------- alerts */
[data-testid="stAlert"] {
    background: var(--qg-bg-alt) !important;
    border: 1px solid var(--qg-border-hover) !important;
    border-radius: 12px !important;
    color: var(--qg-primary-dark) !important;
    font-size: 0.88rem !important;
    padding: 0.7rem 0.9rem !important;
}
[data-testid="stAlert"] [data-testid="stMarkdownContainer"] p {
    color: var(--qg-primary-dark) !important;
}

/* ------------------------------------------------------------------- note */
.qg-note {
    text-align: center;
    color: var(--qg-text-muted);
    font-size: 0.82rem;
    margin-top: 0.6rem;
    line-height: 1.5;
}
.qg-note .qg-dot {
    display: inline-block;
    width: 7px; height: 7px;
    border-radius: 50%;
    background: var(--qg-primary);
    margin-right: 6px;
    vertical-align: middle;
    animation: qgDotPulse 2.4s var(--qg-ease) infinite;
}

@media (max-width: 640px) {
    .block-container { padding-left: 1rem !important; padding-right: 1rem !important; }
}
</style>
"""


def inject_theme() -> None:
    """Inject the shared QueryGenie theme CSS into the Streamlit page."""
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
