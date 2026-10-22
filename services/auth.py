"""Local account registration and password verification."""

from __future__ import annotations

import hashlib
import hmac
import re
import secrets
import sqlite3
from pathlib import Path
from typing import TypedDict


DATABASE_PATH = Path(__file__).resolve().parent.parent / ".querygenie.sqlite3"
PBKDF2_ITERATIONS = 600_000
_DUMMY_SALT = b"QueryGenie timing protection"
_DUMMY_HASH = hashlib.pbkdf2_hmac(
    "sha256",
    b"not-a-real-password",
    _DUMMY_SALT,
    PBKDF2_ITERATIONS,
)


class User(TypedDict):
    id: int
    name: str
    email: str


def _connect() -> sqlite3.Connection:
    try:
        connection = sqlite3.connect(DATABASE_PATH, timeout=10)
        connection.row_factory = sqlite3.Row
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE COLLATE NOCASE,
                password_salt BLOB NOT NULL,
                password_hash BLOB NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        return connection
    except sqlite3.Error as error:
        raise RuntimeError(f"Could not access the local account store: {error}") from error


def _validate_email(email: str) -> str:
    normalized = email.strip().lower()
    if len(normalized) > 254 or not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", normalized):
        raise ValueError("Enter a valid email address.")
    return normalized


def _hash_password(password: str, salt: bytes) -> bytes:
    return hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, PBKDF2_ITERATIONS)


def create_account(name: str, email: str, password: str) -> User:
    """Create a locally stored account and return its public profile."""
    normalized_name = " ".join(name.split())
    normalized_email = _validate_email(email)
    if not normalized_name or len(normalized_name) > 80:
        raise ValueError("Enter your name (up to 80 characters).")
    if len(password) < 10:
        raise ValueError("Use a password with at least 10 characters.")
    if len(password) > 128:
        raise ValueError("Passwords must be 128 characters or fewer.")

    salt = secrets.token_bytes(16)
    password_hash = _hash_password(password, salt)
    connection = _connect()
    try:
        cursor = connection.execute(
            "INSERT INTO users (name, email, password_salt, password_hash) VALUES (?, ?, ?, ?)",
            (normalized_name, normalized_email, salt, password_hash),
        )
        connection.commit()
        return {"id": int(cursor.lastrowid), "name": normalized_name, "email": normalized_email}
    except sqlite3.IntegrityError as error:
        raise ValueError("An account with this email already exists. Please sign in.") from error
    except sqlite3.Error as error:
        raise RuntimeError(f"Could not create the account: {error}") from error
    finally:
        connection.close()


def authenticate(email: str, password: str) -> User | None:
    """Verify credentials without returning stored password material."""
    normalized_email = email.strip().lower()
    connection = _connect()
    try:
        row = connection.execute(
            "SELECT id, name, email, password_salt, password_hash "
            "FROM users WHERE email = ?",
            (normalized_email,),
        ).fetchone()
    except sqlite3.Error as error:
        raise RuntimeError(f"Could not access the local account store: {error}") from error
    finally:
        connection.close()

    salt = bytes(row["password_salt"]) if row else _DUMMY_SALT
    expected_hash = bytes(row["password_hash"]) if row else _DUMMY_HASH
    supplied_hash = _hash_password(password[:128], salt)
    if not row or len(password) > 128 or not hmac.compare_digest(supplied_hash, expected_hash):
        return None
    return {"id": int(row["id"]), "name": str(row["name"]), "email": str(row["email"])}
