"""Visual theme for the QueryGenie dataset workspace."""

from __future__ import annotations

import streamlit as st


WORKSPACE_CSS = """
<style>
:root {
    --qg-ink: #202a2d;
    --qg-muted: #738084;
    --qg-border: #dfe5e5;
    --qg-soft: #f4f7f7;
    --qg-teal: #168c76;
    --qg-teal-soft: #e5f3ef;
}

html, body, [data-testid="stAppViewContainer"] {
    background: #f5f7f7 !important;
    color: var(--qg-ink);
    font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}
[data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stDecoration"],
[data-testid="stStatusWidget"], footer, #MainMenu {
    display: none !important;
}
[data-testid="stMainBlockContainer"] {
    max-width: 100% !important;
    padding: 0.5rem 0.65rem 1rem !important;
}
[data-testid="stHorizontalBlock"] { gap: 0.65rem; }
[data-testid="stVerticalBlock"] { gap: 0.65rem; }

.qg-brand {
    display: flex;
    align-items: center;
    gap: 0.55rem;
    min-height: 2.2rem;
    padding: 0 0.2rem 0.65rem;
    border-bottom: 1px solid var(--qg-border);
    font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
    font-size: 1.05rem;
    font-weight: 700;
}
.qg-brand-mark {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 1.55rem;
    height: 1.55rem;
    border-radius: 0.42rem;
    color: white;
    background: var(--qg-teal);
    font-family: sans-serif;
}
.qg-section-label {
    color: #3d4a4e;
    font-size: 0.76rem;
    font-weight: 650;
    letter-spacing: 0.035em;
    text-transform: uppercase;
}
.qg-dataset-card {
    padding: 0.68rem;
    border: 1px solid #d6ebe5;
    border-radius: 0.5rem;
    background: var(--qg-teal-soft);
    overflow-wrap: anywhere;
}
.qg-dataset-name {
    font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
    font-size: 0.78rem;
    font-weight: 650;
}
.qg-dataset-meta, .qg-muted {
    color: var(--qg-muted);
    font-size: 0.73rem;
}
.qg-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 0.75rem;
    min-height: 2.45rem;
    padding: 0 0.2rem 0.2rem;
    border-bottom: 1px solid var(--qg-border);
}
.qg-crumb {
    color: #506065;
    font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
    font-size: 0.78rem;
}
.qg-panel {
    min-height: calc(100vh - 4.2rem);
    padding: 0.7rem;
    border: 1px solid var(--qg-border);
    border-radius: 0.55rem;
    background: white;
}
.qg-title {
    font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
    font-size: 1rem;
    font-weight: 700;
    overflow-wrap: anywhere;
}
.qg-table-label {
    color: #465459;
    font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
    font-size: 0.76rem;
}
.qg-schema-table {
    width: 100%;
    border-collapse: collapse;
    table-layout: fixed;
    font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
    font-size: 0.66rem;
}
.qg-schema-table th, .qg-schema-table td {
    padding: 0.27rem 0.14rem;
    border-bottom: 1px solid #edf0f0;
    text-align: left;
    overflow-wrap: anywhere;
}
.qg-schema-table th:first-child, .qg-schema-table td:first-child {
    width: 58%;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}
.qg-schema-table th:nth-child(2), .qg-schema-table td:nth-child(2) { width: 27%; }
.qg-schema-table th:last-child, .qg-schema-table td:last-child { width: 15%; }
.qg-schema-table th {
    color: #738084;
    font-size: 0.6rem;
    font-weight: 500;
    text-transform: uppercase;
}
.qg-schema-table td:last-child, .qg-schema-table th:last-child { text-align: right; }
.qg-divider {
    height: 1px;
    margin: 0.6rem 0;
    background: var(--qg-border);
}

/* Compact controls keep the three-column workspace usable at laptop widths. */
[data-testid="stTextInput"] input, [data-testid="stTextArea"] textarea {
    border-color: var(--qg-border) !important;
    border-radius: 0.35rem !important;
    font-size: 0.8rem !important;
}
[data-testid="stButton"] button, [data-testid="stPopover"] button {
    min-height: 2rem;
    border-color: var(--qg-border);
    border-radius: 0.35rem;
    font-size: 0.76rem;
}
[data-testid="stButton"] button[kind="primary"] {
    border-color: var(--qg-teal) !important;
    background: var(--qg-teal) !important;
}
div[class*="st-key-qg_dataset_"] button[kind="primary"] {
    border-color: #d6ebe5 !important;
    background: var(--qg-teal-soft) !important;
    color: var(--qg-ink) !important;
}
[data-testid="stFileUploader"] section {
    padding: 0.65rem;
    border-color: var(--qg-border);
    border-radius: 0.4rem;
}
[data-testid="stDataFrame"] {
    border: 1px solid var(--qg-border);
    border-radius: 0.35rem;
}
[data-testid="stTabs"] button {
    font-size: 0.78rem;
}

@media (max-width: 900px) {
    [data-testid="stMainBlockContainer"] { padding: 0.4rem !important; }
    .qg-panel { min-height: auto; }
}
</style>
"""


def inject_theme() -> None:
    """Inject the workspace styles."""
    st.markdown(WORKSPACE_CSS, unsafe_allow_html=True)
