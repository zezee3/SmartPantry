"""SQLite connection and schema setup helpers."""

import sqlite3
from pathlib import Path


def connect_db(database_path):
    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def initialize_database(database_path):
    database_path = Path(database_path)
    database_path.parent.mkdir(parents=True, exist_ok=True)
    schema_path = Path(__file__).resolve().parents[2] / "database" / "schema.sql"
    schema = schema_path.read_text(encoding="utf-8")

    connection = connect_db(database_path)
    try:
        connection.executescript(schema)
        connection.commit()
    finally:
        connection.close()
