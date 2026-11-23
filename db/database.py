import sqlite3

DB_PATH = "data/sources.sqlite"
SCHEMA_FILE = "sql/schema.sql"


def get_connection(path=DB_PATH):
    conn = sqlite3.connect(path)
    conn.execute("PRAGMA foreign_keys = ON")
    # встроенный lower в sqlite не работает с кириллицей
    conn.create_function("py_lower", 1, lambda value: value.lower())
    return conn


def create_tables(conn):
    with open(SCHEMA_FILE, encoding="utf-8") as file:
        conn.executescript(file.read())


def fetch_all(sql, params=(), path=DB_PATH):
    conn = get_connection(path)
    conn.row_factory = sqlite3.Row
    rows = conn.execute(sql, params).fetchall()
    conn.close()
    return rows


def fetch_one(sql, params=(), path=DB_PATH):
    rows = fetch_all(sql, params, path)
    return rows[0] if rows else None


# возраст и актуальность источника считаются прямо в запросе
AGE = "CAST(strftime('%Y', 'now') AS INTEGER) - sources.year"
RELEVANCE = f"""
    CASE
        WHEN {AGE} <= 3 THEN 'актуальный'
        WHEN {AGE} <= 7 THEN 'требует проверки'
        ELSE 'устаревший'
    END
"""
