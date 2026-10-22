# QueryGenie

QueryGenie is a local, session-based dataset workspace. It opens directly to the
workspace shown in the design reference, with a dataset rail, table preview,
schema panel, query editor, and query history.

## Run locally

```powershell
python -m pip install -r requirements.txt
streamlit run app.py
```

The bundled `global_ecommerce_sales.csv` is loaded as the demonstration
dataset. Uploaded CSV files (up to 10 MB) and query history stay in the active
Streamlit session; there is no MySQL connection or persistent user database.
The sample dataset cannot be deleted. User-uploaded datasets can be renamed or
removed from the session.

The question helper generates SQL for common requests such as “top 5 products
by profit” and “total sales by region”. It is a local helper rather than a
hosted AI integration. Queries run against an in-memory SQLite copy of the
selected dataset; only read-only `SELECT` queries are allowed, execution is
time-limited, and results are capped at 500 rows.
