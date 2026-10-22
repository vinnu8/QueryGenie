"""Post-login dataset workspace."""

from __future__ import annotations

import hashlib
import html
from datetime import datetime

import pandas as pd
import streamlit as st

from services.datasets import (
    MAX_PREVIEW_ROWS,
    MAX_UPLOAD_BYTES,
    read_uploaded_dataset,
    schema_rows,
    table_name_for_dataset,
)
from services.auth import User
from services.query import generate_sql, run_query


DEFAULT_SQL = "SELECT * FROM {table} LIMIT 100"


def _initialize_workspace(user: User) -> None:
    if st.session_state.get("qg_dataset_owner") != user["id"]:
        st.session_state.qg_dataset_owner = user["id"]
        st.session_state.qg_datasets = {}
        st.session_state.qg_selected_dataset = None
        st.session_state.qg_query_history = []
        st.session_state.qg_query_result = None
        st.session_state.qg_processed_uploads = set()
        st.session_state.pop("qg_workspace_view", None)
        st.session_state.pop("sql_editor", None)
        st.session_state.pop("qg_editor_dataset", None)


def _unique_filename(filename: str, datasets: dict[str, pd.DataFrame]) -> str:
    if filename not in datasets:
        return filename
    stem, suffix = filename.rsplit(".", 1) if "." in filename else (filename, "")
    counter = 2
    while True:
        candidate = f"{stem} ({counter})"
        if suffix:
            candidate = f"{candidate}.{suffix}"
        if candidate not in datasets:
            return candidate
        counter += 1


def _render_upload(key: str) -> None:
    uploaded = st.file_uploader(
        "Upload CSV",
        type=["csv"],
        help=f"CSV files only, up to {MAX_UPLOAD_BYTES // (1024 * 1024)} MB.",
        label_visibility="collapsed",
        key=key,
    )
    if uploaded is None:
        return

    content = uploaded.getvalue()
    upload_id = hashlib.sha256(uploaded.name.encode("utf-8") + content).hexdigest()
    if upload_id in st.session_state.qg_processed_uploads:
        return
    try:
        frame = read_uploaded_dataset(uploaded.name, content)
    except ValueError as error:
        st.error(str(error))
        return

    datasets = st.session_state.qg_datasets
    filename = _unique_filename(uploaded.name, datasets)
    datasets[filename] = frame
    st.session_state.qg_selected_dataset = filename
    st.session_state.qg_processed_uploads.add(upload_id)
    st.session_state.qg_upload_notice = f"{filename} uploaded."
    st.rerun()


def _render_dataset_rail(user: User) -> None:
    datasets: dict[str, pd.DataFrame] = st.session_state.qg_datasets
    st.markdown(
        '<div class="qg-brand"><span class="qg-brand-mark">⌕</span>QueryGenie</div>',
        unsafe_allow_html=True,
    )
    st.markdown('<div class="qg-section-label">Datasets</div>', unsafe_allow_html=True)

    if not datasets:
        st.markdown('<div class="qg-empty-rail">No datasets yet</div>', unsafe_allow_html=True)
    else:
        for index, (filename, frame) in enumerate(datasets.items()):
            selected = filename == st.session_state.qg_selected_dataset
            label = f"{'▣' if selected else '▱'}  {filename}"
            if st.button(
                label,
                key=f"qg_dataset_{index}",
                help=f"{len(frame):,} rows · {len(frame.columns)} columns",
                type="primary" if selected else "secondary",
                use_container_width=True,
            ):
                st.session_state.qg_selected_dataset = filename
                st.rerun()
            if selected:
                st.markdown(
                    f'<div class="qg-dataset-card"><div class="qg-dataset-meta">'
                    f'{len(frame):,} rows · {len(frame.columns)} cols · active</div></div>',
                    unsafe_allow_html=True,
                )

    st.markdown("")
    _render_upload("qg_upload")
    notice = st.session_state.pop("qg_upload_notice", None)
    if notice:
        st.caption(notice)
    st.markdown('<div class="qg-user-card">', unsafe_allow_html=True)
    st.markdown(
        f'<div class="qg-user-name">{html.escape(user["name"])}</div>'
        f'<div class="qg-user-email" title="{html.escape(user["email"])}">'
        f'{html.escape(user["email"])}</div>',
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)
    if st.button("Sign out", key="qg_signout", use_container_width=True):
        st.session_state.clear()
        st.rerun()


def _render_dataset_actions(filename: str) -> None:
    datasets: dict[str, pd.DataFrame] = st.session_state.qg_datasets
    rename_column, delete_column = st.columns(2, gap="small")
    with rename_column:
        with st.popover("Rename", use_container_width=True):
            with st.form("qg_rename_form"):
                new_name = st.text_input(
                    "Dataset name",
                    value=filename,
                    help="Keep the .csv extension.",
                ).strip()
                submitted = st.form_submit_button("Save name", use_container_width=True)
            if submitted:
                if not new_name.lower().endswith(".csv") or new_name == ".csv":
                    st.error("Enter a dataset name ending in .csv.")
                elif new_name != filename and new_name in datasets:
                    st.error("A dataset with that name already exists.")
                elif new_name != filename:
                    datasets[new_name] = datasets.pop(filename)
                    for item in st.session_state.qg_query_history:
                        if item["filename"] == filename:
                            item["filename"] = new_name
                    query_result = st.session_state.get("qg_query_result")
                    if query_result and query_result["filename"] == filename:
                        query_result["filename"] = new_name
                    if st.session_state.qg_sample_filename == filename:
                        st.session_state.qg_sample_filename = new_name
                    st.session_state.qg_selected_dataset = new_name
                    st.rerun()
    with delete_column:
        with st.popover("Delete", use_container_width=True):
            st.warning(f"Remove {filename} from this session?")
            if st.button("Delete dataset", key="qg_confirm_delete", type="primary"):
                datasets.pop(filename)
                st.session_state.qg_query_history = [
                    item
                    for item in st.session_state.qg_query_history
                    if item["filename"] != filename
                ]
                query_result = st.session_state.get("qg_query_result")
                if query_result and query_result["filename"] == filename:
                    st.session_state.qg_query_result = None
                st.session_state.qg_selected_dataset = next(iter(datasets), None)
                st.rerun()


def _render_preview(frame: pd.DataFrame) -> None:
    st.markdown(
        f'<div class="qg-table-label">Preview (first {MAX_PREVIEW_ROWS} rows)</div>',
        unsafe_allow_html=True,
    )
    st.dataframe(
        frame.head(MAX_PREVIEW_ROWS),
        use_container_width=True,
        height=555,
        hide_index=True,
    )


def _render_query_tab(filename: str, frame: pd.DataFrame, table_name: str) -> None:
    editor_dataset_key = st.session_state.get("qg_editor_dataset")
    if editor_dataset_key != filename:
        st.session_state.sql_editor = DEFAULT_SQL.format(table=table_name)
        st.session_state.qg_editor_dataset = filename

    st.subheader("Ask your dataset")
    st.caption(
        "Try a supported question, then review the generated SQL before running it. "
        "You can also write a read-only SELECT query."
    )
    st.text_input(
        "Natural-language question",
        placeholder="e.g. Total sales by region",
        key="qg_question",
    )
    if st.button("Generate SQL", key="qg_generate_sql"):
        try:
            st.session_state.sql_editor = generate_sql(
                st.session_state.qg_question,
                [str(column) for column in frame.columns],
                table_name,
            )
            st.session_state.qg_query_error = None
        except ValueError as error:
            st.session_state.qg_query_error = str(error)

    query_error = st.session_state.pop("qg_query_error", None)
    if query_error:
        st.warning(query_error)

    sql = st.text_area(
        "SQL query",
        key="sql_editor",
        height=150,
        help=f"Available table: {table_name}. Only SELECT queries are allowed.",
    )
    if st.button("Run query", type="primary", key="qg_run_query"):
        try:
            result, truncated = run_query(frame, table_name, sql)
        except ValueError as error:
            st.session_state.qg_query_error = str(error)
            st.rerun()
        history = st.session_state.qg_query_history
        history.insert(
            0,
            {
                "filename": filename,
                "question": st.session_state.qg_question.strip() or "SQL query",
                "sql": sql,
                "rows": len(result),
                "time": datetime.now().strftime("%H:%M"),
            },
        )
        del history[30:]
        st.session_state.qg_query_result = {
            "filename": filename,
            "frame": result,
            "truncated": truncated,
        }

    query_result = st.session_state.get("qg_query_result")
    if not query_result or query_result["filename"] != filename:
        return

    result: pd.DataFrame = query_result["frame"]
    st.markdown('<div class="qg-divider"></div>', unsafe_allow_html=True)
    st.subheader("Results")
    st.caption(f"{len(result):,} row(s) returned.")
    if query_result["truncated"]:
        st.info("Showing the first 500 rows. Narrow the query with a LIMIT clause.")
    if result.empty:
        st.info("The query completed successfully and returned no rows.")
        return

    st.dataframe(result, use_container_width=True, hide_index=True)
    numeric_columns = [
        str(column)
        for column in result.columns
        if pd.api.types.is_numeric_dtype(result[column])
    ]
    if numeric_columns:
        chart_column, x_column = st.columns(2)
        with chart_column:
            chart_type = st.selectbox(
                "Chart",
                ["Bar", "Line", "Area"],
                key="qg_chart_type",
            )
        with x_column:
            x_options = [str(column) for column in result.columns if column not in numeric_columns]
            x_axis = st.selectbox(
                "Group by",
                x_options or numeric_columns,
                key="qg_chart_x",
            )
        chart_data = result.set_index(x_axis)[numeric_columns] if x_axis in result.columns else result[numeric_columns]
        if chart_type == "Bar":
            st.bar_chart(chart_data)
        elif chart_type == "Line":
            st.line_chart(chart_data)
        else:
            st.area_chart(chart_data)
        numeric_column = numeric_columns[0]
        total = pd.to_numeric(result[numeric_column], errors="coerce").sum()
        st.caption(f"Quick insight: {numeric_column} totals {total:,.2f} across the displayed results.")


def _render_schema_panel(filename: str, frame: pd.DataFrame, table_name: str) -> None:
    st.markdown('<div class="qg-section-label">▤ &nbsp; Dataset Schema</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="qg-dataset-name">{html.escape(filename)}</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="qg-muted">{len(frame.columns)} columns · {len(frame):,} rows</div>',
        unsafe_allow_html=True,
    )
    st.markdown(f'<div class="qg-muted">SQL table: {html.escape(table_name)}</div>', unsafe_allow_html=True)

    rows = schema_rows(frame)
    body = "".join(
        "<tr>"
        f"<td>{html.escape(name)}</td>"
        f"<td>{html.escape(dtype)}</td>"
        f"<td>{nulls}</td>"
        "</tr>"
        for name, dtype, nulls in rows
    )
    st.markdown(
        '<table class="qg-schema-table"><thead><tr><th>Column</th><th>Type</th>'
        f'<th>Nulls</th></tr></thead><tbody>{body}</tbody></table>',
        unsafe_allow_html=True,
    )
    st.markdown('<div class="qg-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="qg-section-label">Query History</div>', unsafe_allow_html=True)
    history = [
        item
        for item in st.session_state.qg_query_history
        if item["filename"] == filename
    ]
    if not history:
        st.caption("Queries you run appear here.")
        return
    for item in history[:8]:
        with st.expander(f'{item["time"]} · {item["question"]}', expanded=False):
            st.caption(f'{item["rows"]:,} row(s)')
            st.code(item["sql"], language="sql")


def _render_empty_workspace() -> None:
    st.markdown(
        '<div class="qg-empty-state"><div class="qg-empty-icon">↑</div>'
        '<div class="qg-empty-title">Your workspace is ready</div>'
        '<div class="qg-empty-copy">Upload a CSV file to preview your records, explore its schema, '
        'and ask questions about your data.</div></div>',
        unsafe_allow_html=True,
    )
    _render_upload("qg_empty_upload")


def _render_empty_schema_panel() -> None:
    st.markdown('<div class="qg-section-label">Dataset Schema</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="qg-empty-aside">Your column names, data types, and query history '
        'will appear here after you upload a dataset.</div>',
        unsafe_allow_html=True,
    )
    st.markdown('<div class="qg-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="qg-section-label">Query History</div>', unsafe_allow_html=True)
    st.caption("Queries you run appear here.")


def render_workspace(user: User) -> None:
    """Render the authenticated dataset workspace."""
    _initialize_workspace(user)
    datasets: dict[str, pd.DataFrame] = st.session_state.qg_datasets
    selected_filename = st.session_state.qg_selected_dataset
    if selected_filename not in datasets:
        selected_filename = next(iter(datasets), None)
        st.session_state.qg_selected_dataset = selected_filename
    frame = datasets.get(selected_filename) if selected_filename else None
    table_name = table_name_for_dataset(selected_filename) if selected_filename else ""
    left, center, right = st.columns([1.65, 6.1, 2.25], gap="medium")
    with left:
        with st.container(key="qg-rail-panel"):
            _render_dataset_rail(user)
    with center:
        with st.container(key="qg-main-panel"):
            header_column, toggle_column = st.columns([5, 2], vertical_alignment="center")
            with header_column:
                breadcrumb = (
                    f'Workspace&nbsp; / &nbsp;{html.escape(selected_filename)}'
                    if selected_filename
                    else "Workspace"
                )
                st.markdown(
                    f'<div class="qg-crumb">{breadcrumb}</div>',
                    unsafe_allow_html=True,
                )
            with toggle_column:
                active_view = st.segmented_control(
                    "Workspace view",
                    ["Schema", "Query"],
                    selection_mode="single",
                    default="Schema",
                    label_visibility="collapsed",
                    key="qg_workspace_view",
                    width="stretch",
                )
            if frame is None or selected_filename is None:
                st.markdown('<div class="qg-divider"></div>', unsafe_allow_html=True)
                if active_view == "Schema":
                    _render_empty_workspace()
                else:
                    st.markdown(
                        '<div class="qg-empty-state"><div class="qg-empty-title">'
                        'Upload a dataset to start querying</div><div class="qg-empty-copy">'
                        'Your questions and SQL editor will be ready as soon as your CSV is uploaded.</div></div>',
                        unsafe_allow_html=True,
                    )
                    _render_upload("qg_empty_upload")
            else:
                title_column, action_column = st.columns([4.7, 2], vertical_alignment="center")
                with title_column:
                    st.markdown(f'<div class="qg-title">{html.escape(selected_filename)}</div>', unsafe_allow_html=True)
                    st.markdown(
                        f'<div class="qg-muted">{len(frame.columns)} columns · {len(frame):,} rows · '
                        f'table {html.escape(table_name)}</div>',
                        unsafe_allow_html=True,
                    )
                with action_column:
                    _render_dataset_actions(selected_filename)
                st.markdown('<div class="qg-divider"></div>', unsafe_allow_html=True)
                if active_view == "Schema":
                    _render_preview(frame)
                else:
                    _render_query_tab(selected_filename, frame, table_name)
    with right:
        with st.container(key="qg-schema-panel"):
            if frame is None or selected_filename is None:
                _render_empty_schema_panel()
            else:
                _render_schema_panel(selected_filename, frame, table_name)
