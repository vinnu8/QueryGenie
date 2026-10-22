# QueryGenie

QueryGenie is a Streamlit workspace for exploring your own CSV files. New
visitors sign in or create an account before reaching a clean, empty workspace.
The first step is uploading a CSV; no demo dataset is bundled or loaded.

## Run locally

```powershell
python -m pip install -r requirements.txt
streamlit run app.py
```

Accounts are stored locally in the ignored `.querygenie.sqlite3` SQLite file.
Passwords are salted and hashed with PBKDF2-HMAC-SHA256. No MySQL connection
or external account service is required.

Uploaded datasets and query history stay in the active browser session and
aren't written to disk. Each signed-in session starts with an empty dataset
library. CSV uploads are limited to 10 MB. Datasets can be renamed or removed.

The question helper generates SQL for common requests such as “top 5 products
by profit” and “total sales by region”. It is a local helper rather than a
hosted AI integration. Queries run against an in-memory SQLite copy of the
selected dataset; only read-only `SELECT` queries are allowed, execution is
time-limited, and results are capped at 500 rows.
