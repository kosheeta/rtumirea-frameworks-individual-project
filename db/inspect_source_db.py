import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SOURCE_DB = BASE_DIR / "data" / "sources.sqlite"

if not SOURCE_DB.exists():
    raise FileNotFoundError(f"исходная база не найдена: {SOURCE_DB}")

with sqlite3.connect(SOURCE_DB) as conn:
    tables = conn.execute(
        "SELECT name FROM sqlite_master "
        "WHERE type = 'table' AND name NOT LIKE 'sqlite_%' ORDER BY name"
    ).fetchall()
    for (table,) in tables:
        print(f"\nТаблица: {table}")
        for column in conn.execute(f'PRAGMA table_info("{table}")'):
            print(f"  {column[1]} {column[2]} notnull={column[3]} "
                  f"pk={column[5]}")
        count = conn.execute(f'SELECT COUNT(*) FROM "{table}"').fetchone()
        print(f"Записей: {count[0]}")
