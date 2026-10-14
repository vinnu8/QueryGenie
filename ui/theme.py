"""Shared visual theme for the QueryGenie UI prototypes."""

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
    --qg-primary-dark: #1B45C4;
    --qg-secondary: #60A5FA;
    --qg-teal: #0D9488;
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
@keyframes qgFlowPulse {
    0%, 100% { transform: translateY(0); opacity: 0.85; }
    50%      { transform: translateY(3px); opacity: 1; }
}
@keyframes qgArrowPulse {
    0%, 100% { opacity: 0.55; }
    50%      { opacity: 1; }
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
    .qg-pulse, .qg-flow-arrow { animation: none !important; }
    * { transition-duration: 0.01ms !important; }
}

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

.qg-flow-card {
    position: relative;
    margin: 0 auto 0.9rem;
    max-width: 460px;
    background: rgba(255, 255, 255, 0.72);
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    border: 1px solid var(--qg-border);
    border-radius: var(--qg-radius-lg);
    padding: 1.5rem 1.6rem;
    text-align: center;
    box-shadow: var(--qg-shadow);
    transition: transform 0.24s var(--qg-ease), box-shadow 0.24s var(--qg-ease), border-color 0.24s var(--qg-ease);
}
.qg-flow-card:hover {
    transform: translateY(-4px);
    border-color: var(--qg-border-hover);
    box-shadow: var(--qg-shadow-hover);
}
.qg-flow-card h3 {
    margin: 0 0 0.4rem;
    font-size: 1.18rem;
    font-weight: 700;
    color: var(--qg-text);
    letter-spacing: -0.01em;
}
.qg-flow-card .qg-support {
    margin: 0;
    color: var(--qg-text-muted);
    font-size: 0.92rem;
}
.qg-flow-card::before {
    content: '';
    position: absolute;
    inset: -1px;
    border-radius: var(--qg-radius-lg);
    background: linear-gradient(135deg, rgba(36,87,230,0.18), rgba(96,165,250,0.05), transparent 70%);
    z-index: -1;
    opacity: 0;
    transition: opacity 0.3s var(--qg-ease);
}
.qg-flow-card:hover::before { opacity: 1; }

.qg-down-arrow {
    text-align: center;
    margin-bottom: 1rem;
    color: var(--qg-primary);
}
.qg-down-arrow svg {
    animation: qgFlowPulse 1.6s var(--qg-ease) infinite;
}

.qg-bridge {
    width: 100%;
    margin: 0 0 0.6rem;
    opacity: 0.9;
}
.qg-bridge svg { width: 100%; height: 36px; display: block; }
.qg-flow-line {
    stroke-dasharray: 6 6;
    animation: qgArrowPulse 2.2s ease-in-out infinite;
}

.qg-role-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1.25rem;
    margin-bottom: 2rem;
}
@media (max-width: 640px) {
    .qg-role-grid { grid-template-columns: 1fr; gap: 1rem; }
}

.qg-role-card {
    border-radius: var(--qg-radius-md);
    padding: 1.35rem 1.4rem;
    color: #E8EDF7;
    box-shadow: var(--qg-shadow);
    transition: transform 0.24s var(--qg-ease), box-shadow 0.24s var(--qg-ease), border-color 0.24s var(--qg-ease);
    border: 1px solid rgba(255,255,255,0.08);
    position: relative;
    overflow: hidden;
}
.qg-role-card:hover {
    transform: translateY(-5px);
    box-shadow: var(--qg-shadow-hover);
}
.qg-role-card h4 {
    margin: 0 0 0.75rem;
    font-size: 1.05rem;
    font-weight: 700;
    letter-spacing: -0.01em;
    display: flex;
    align-items: center;
    gap: 8px;
}
.qg-role-card .qg-badge {
    font-size: 0.72rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    padding: 3px 8px;
    border-radius: 999px;
    background: rgba(255,255,255,0.12);
    margin-left: auto;
}
.qg-feature-list {
    list-style: none;
    padding: 0;
    margin: 0;
    display: flex;
    flex-direction: column;
    gap: 0.45rem;
}
.qg-feature-list li {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 0.9rem;
    color: rgba(232, 237, 247, 0.9);
}
.qg-feature-list li::before {
    content: '';
    width: 6px;
    height: 6px;
    border-radius: 50%;
    flex: 0 0 6px;
}

.qg-role-admin {
    background: linear-gradient(155deg, #1E293B 0%, #0F172A 100%);
}
.qg-role-admin h4 { color: #BFDBFE; }
.qg-role-admin .qg-feature-list li::before { background: var(--qg-secondary); }
.qg-role-admin:hover { border-color: rgba(96, 165, 250, 0.45); }

.qg-role-employee {
    background: linear-gradient(155deg, #0F2420 0%, #0B1A17 100%);
}
.qg-role-employee h4 { color: #A7F3D0; }
.qg-role-employee .qg-feature-list li::before { background: var(--qg-teal); }
.qg-role-employee:hover { border-color: rgba(13, 148, 136, 0.45); }

.qg-role-caption {
    margin: 0.9rem 0 0;
    font-size: 0.78rem;
    color: var(--qg-text-muted);
    text-align: center;
    font-style: italic;
}

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

.qg-note {
    text-align: center;
    color: var(--qg-text-muted);
    font-size: 0.82rem;
    margin-top: 0.6rem;
}
.qg-note .qg-dot {
    display: inline-block;
    width: 7px; height: 7px;
    border-radius: 50%;
    background: var(--qg-teal);
    margin-right: 6px;
    vertical-align: middle;
}

@media (max-width: 640px) {
    .block-container { padding-left: 1rem !important; padding-right: 1rem !important; }
    .qg-flow-card { padding: 1.25rem 1.15rem; }
}
</style>
"""


def inject_theme() -> None:
    """Inject the shared QueryGenie theme CSS into the Streamlit page."""
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
