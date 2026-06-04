"""Database helpers for EngineX.

The SQLite database is the contract between the crawler half (partner) and
the search half (friend). The schema lives in `schema.sql`.

Typical usage:

    from db import connect, init_db

    init_db()                 # create tables (idempotent)
    with connect() as conn:
        rows = conn.execute("SELECT id, url, title FROM pages").fetchall()
"""
from __future__ import annotations

import sqlite3
from pathlib import Path

# Database file lives next to this module so both halves agree on its path.
DB_PATH = Path(__file__).resolve().parent / "enginex.db"
SCHEMA_PATH = Path(__file__).resolve().parent / "schema.sql"


def connect(db_path: Path = DB_PATH) -> sqlite3.Connection:
    """Open a connection with sensible defaults.

    - `row_factory = sqlite3.Row` lets callers access columns by name.
    - `PRAGMA foreign_keys = ON` enforces the FKs declared in schema.sql
      (SQLite leaves them off by default).
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db(db_path: Path = DB_PATH) -> None:
    """Create all tables if they don't already exist. Idempotent."""
    schema = SCHEMA_PATH.read_text(encoding="utf-8")
    with connect(db_path) as conn:
        conn.executescript(schema)


if __name__ == "__main__":
    init_db()
    print(f"Initialized database at {DB_PATH}")
