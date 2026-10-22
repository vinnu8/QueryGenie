"""CSV import and schema helpers."""

from __future__ import annotations

import io
import re
import pandas as pd


MAX_UPLOAD_BYTES = 10 * 1024 * 1024
MAX_PREVIEW_ROWS = 20


def read_uploaded_dataset(filename: str, content: bytes) -> pd.DataFrame:
    """Validate and read an uploaded CSV dataset."""
    if not filename.lower().endswith(".csv"):
        raise ValueError("Only CSV files are supported.")
    if not content:
        raise ValueError("The uploaded file is empty.")
    if len(content) > MAX_UPLOAD_BYTES:
        raise ValueError("Files must be 10 MB or smaller.")

    try:
        frame = pd.read_csv(io.BytesIO(content))
    except (pd.errors.ParserError, UnicodeDecodeError, ValueError) as error:
        raise ValueError(f"Could not read this CSV file: {error}") from error
    if frame.empty and len(frame.columns) == 0:
        raise ValueError("The CSV file must contain a header row.")
    if len(frame.columns) == 0:
        raise ValueError("The CSV file must contain at least one column.")
    if frame.columns.has_duplicates:
        raise ValueError("Column names must be unique.")
    if any(not str(column).strip() for column in frame.columns):
        raise ValueError("Column names cannot be empty.")
    return frame


def table_name_for_dataset(filename: str) -> str:
    """Return a safe SQL table identifier derived from a dataset filename."""
    stem = Path(filename).stem.lower()
    table_name = re.sub(r"\W+", "_", stem).strip("_")
    if not table_name or table_name[0].isdigit():
        table_name = f"dataset_{table_name}"
    return table_name


def schema_rows(frame: pd.DataFrame) -> list[tuple[str, str, int]]:
    """Return column name, display type, and null count for a dataset."""
    rows = []
    for column in frame.columns:
        dtype = frame[column].dtype
        if pd.api.types.is_integer_dtype(dtype):
            display_type = "INT"
        elif pd.api.types.is_float_dtype(dtype):
            display_type = "DECIMAL"
        elif pd.api.types.is_bool_dtype(dtype):
            display_type = "BOOLEAN"
        elif pd.api.types.is_datetime64_any_dtype(dtype):
            display_type = "DATETIME"
        else:
            display_type = "TEXT"
        rows.append((str(column), display_type, int(frame[column].isna().sum())))
    return rows
