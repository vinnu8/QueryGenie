"""Local natural-language helpers and read-only SQL execution."""

from __future__ import annotations

import re
import sqlite3
import time

import pandas as pd


MAX_RESULT_ROWS = 500
QUERY_TIMEOUT_SECONDS = 2

_WRITE_ACTIONS = {
    sqlite3.SQLITE_INSERT,
    sqlite3.SQLITE_UPDATE,
    sqlite3.SQLITE_DELETE,
    sqlite3.SQLITE_CREATE_INDEX,
    sqlite3.SQLITE_CREATE_TABLE,
    sqlite3.SQLITE_CREATE_TEMP_INDEX,
    sqlite3.SQLITE_CREATE_TEMP_TABLE,
    sqlite3.SQLITE_CREATE_TEMP_TRIGGER,
    sqlite3.SQLITE_CREATE_TEMP_VIEW,
    sqlite3.SQLITE_CREATE_TRIGGER,
    sqlite3.SQLITE_CREATE_VIEW,
    sqlite3.SQLITE_DROP_INDEX,
    sqlite3.SQLITE_DROP_TABLE,
    sqlite3.SQLITE_DROP_TEMP_INDEX,
    sqlite3.SQLITE_DROP_TEMP_TABLE,
    sqlite3.SQLITE_DROP_TEMP_TRIGGER,
    sqlite3.SQLITE_DROP_TEMP_VIEW,
    sqlite3.SQLITE_DROP_TRIGGER,
    sqlite3.SQLITE_DROP_VIEW,
    sqlite3.SQLITE_ALTER_TABLE,
    sqlite3.SQLITE_ATTACH,
    sqlite3.SQLITE_DETACH,
    sqlite3.SQLITE_PRAGMA,
    sqlite3.SQLITE_TRANSACTION,
    sqlite3.SQLITE_SAVEPOINT,
    sqlite3.SQLITE_ANALYZE,
    sqlite3.SQLITE_REINDEX,
}

_COLUMN_ALIASES = {
    "sales": "total_sales",
    "revenue": "total_sales",
    "earnings": "profit",
    "orders": "order_id",
    "date": "order_date",
    "product": "product_name",
    "category": "product_category",
}


def _quote_identifier(identifier: str) -> str:
    return '"' + identifier.replace('"', '""') + '"'


def _column_for_phrase(phrase: str, columns: list[str]) -> str | None:
    normalized_phrase = re.sub(r"[^a-z0-9]+", " ", phrase.lower()).strip()
    candidates = sorted(columns, key=len, reverse=True)
    for column in candidates:
        normalized_column = re.sub(r"[^a-z0-9]+", " ", column.lower()).strip()
        if re.search(rf"\b{re.escape(normalized_column)}\b", normalized_phrase):
            return column
    for alias, column_name in _COLUMN_ALIASES.items():
        if re.search(rf"\b{re.escape(alias)}\b", normalized_phrase):
            return next((column for column in columns if column.lower() == column_name), None)
    return None


def generate_sql(question: str, columns: list[str], table_name: str) -> str:
    """Translate a small, explicit set of common analytics questions to SQL."""
    prompt = question.strip()
    if not prompt:
        raise ValueError("Enter a question first.")

    quoted_table = _quote_identifier(table_name)
    top_match = re.search(r"\btop\s+(\d+)\b(.*)", prompt, re.IGNORECASE)
    if top_match:
        limit = min(int(top_match.group(1)), 500)
        order_phrase = re.split(r"\b(?:by|ordered by|ranked by)\b", top_match.group(2), maxsplit=1)
        order_column = _column_for_phrase(order_phrase[-1], columns) if len(order_phrase) > 1 else None
        if order_column:
            return (
                f"SELECT * FROM {quoted_table} ORDER BY "
                f"{_quote_identifier(order_column)} DESC LIMIT {limit}"
            )
        return f"SELECT * FROM {quoted_table} LIMIT {limit}"

    aggregate_match = re.search(
        r"\b(total|sum|average|avg|mean|count)\b(.*)",
        prompt,
        re.IGNORECASE,
    )
    if aggregate_match:
        remainder = aggregate_match.group(2)
        grouped_phrase = re.split(r"\bby\b", remainder, maxsplit=1)
        group_column = _column_for_phrase(grouped_phrase[-1], columns) if len(grouped_phrase) > 1 else None
        metric_column = _column_for_phrase(grouped_phrase[0], columns)
        operation = aggregate_match.group(1).lower()
        if operation in {"total", "sum"} and metric_column:
            aggregate = f"SUM({_quote_identifier(metric_column)})"
        elif operation in {"average", "avg", "mean"} and metric_column:
            aggregate = f"AVG({_quote_identifier(metric_column)})"
        elif operation == "count":
            aggregate = "COUNT(*)"
        else:
            aggregate = None
        if aggregate:
            if group_column:
                return (
                    f"SELECT {_quote_identifier(group_column)}, {aggregate} AS value "
                    f"FROM {quoted_table} GROUP BY {_quote_identifier(group_column)} "
                    "ORDER BY value DESC"
                )
            if operation == "count":
                return f"SELECT {aggregate} AS value FROM {quoted_table}"
            if metric_column:
                return f"SELECT {aggregate} AS value FROM {quoted_table}"

    if re.search(r"\b(show|list|display|preview|all|every|rows?)\b", prompt, re.IGNORECASE):
        return f"SELECT * FROM {quoted_table} LIMIT 100"
    raise ValueError(
        "I couldn't map that question to a query. Try “show the first rows”, "
        "“top 5 products by profit”, or “total sales by region”, or write SQL directly."
    )


def _authorize(action: int, arg1: str | None, arg2: str | None, *_: object) -> int:
    if action in _WRITE_ACTIONS:
        return sqlite3.SQLITE_DENY
    if action == sqlite3.SQLITE_FUNCTION and (arg2 or arg1 or "").lower() == "load_extension":
        return sqlite3.SQLITE_DENY
    return sqlite3.SQLITE_OK


def execute_read_only_query(
    frame: pd.DataFrame,
    table_name: str,
    sql: str,
) -> tuple[pd.DataFrame, bool]:
    """Run one bounded, read-only query over an in-memory copy of a dataset."""
    if not re.match(r"^\s*(SELECT|WITH)\b", sql, re.IGNORECASE):
        raise ValueError("Only read-only SELECT queries are allowed.")
    if not sql.strip():
        raise ValueError("Enter a SQL query first.")

    connection = sqlite3.connect(":memory:")
    deadline = time.monotonic() + QUERY_TIMEOUT_SECONDS
    connection.setlimit(sqlite3.SQLITE_LIMIT_LENGTH, 10 * 1024 * 1024)
    connection.setlimit(sqlite3.SQLITE_LIMIT_SQL_LENGTH, 100_000)
    connection.setlimit(sqlite3.SQLITE_LIMIT_COLUMN, 200)
    connection.setlimit(sqlite3.SQLITE_LIMIT_EXPR_DEPTH, 100)
    connection.setlimit(sqlite3.SQLITE_LIMIT_COMPOUND_SELECT, 50)
    connection.set_progress_handler(
        lambda: int(time.monotonic() > deadline),
        1000,
    )
    try:
        frame.to_sql(table_name, connection, index=False, if_exists="replace")
        connection.set_authorizer(_authorize)
        cursor = connection.execute(sql)
        column_names = [description[0] for description in cursor.description or []]
        result_rows = cursor.fetchmany(MAX_RESULT_ROWS + 1)
        truncated = len(result_rows) > MAX_RESULT_ROWS
        result = pd.DataFrame(result_rows[:MAX_RESULT_ROWS], columns=column_names)
        return result, truncated
    except sqlite3.Error as error:
        message = str(error)
        if "not authorized" in message.lower():
            raise ValueError("This query attempted an operation that is not allowed.") from error
        if "interrupted" in message.lower():
            raise ValueError("The query exceeded the 2-second execution limit.") from error
        raise ValueError(f"Could not run this SQL query: {message}") from error
    finally:
        connection.close()


def run_query(
    frame: pd.DataFrame,
    table_name: str,
    sql: str,
) -> tuple[pd.DataFrame, bool]:
    """Public query entry point."""
    return execute_read_only_query(frame, table_name, sql)
