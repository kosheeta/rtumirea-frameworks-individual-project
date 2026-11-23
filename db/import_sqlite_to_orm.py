import os
import sqlite3
import sys
from pathlib import Path

import django

BASE_DIR = Path(__file__).resolve().parent.parent
SOURCE_DB = BASE_DIR / "data" / "sources.sqlite"

sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sourcehub.settings")
django.setup()

from django.db import transaction  # noqa: E402

from researches.models import Research  # noqa: E402
from sources.models import Source  # noqa: E402
from users.models import User  # noqa: E402


def read_rows(conn, table):
    conn.row_factory = sqlite3.Row
    return conn.execute(f"SELECT * FROM {table} ORDER BY id").fetchall()


@transaction.atomic
def transfer(conn):
    # порядок важен: сначала независимые таблицы
    for row in read_rows(conn, "users"):
        User.objects.update_or_create(
            id=row["id"],
            defaults={"name": row["name"], "email": row["email"]},
        )
    for row in read_rows(conn, "researches"):
        Research.objects.update_or_create(
            id=row["id"],
            defaults={
                "user_id": row["user_id"],
                "title": row["title"],
                "description": row["description"] or "",
            },
        )
    for row in read_rows(conn, "sources"):
        Source.objects.update_or_create(
            id=row["id"],
            defaults={
                "research_id": row["research_id"],
                "user_id": row["user_id"],
                "author": row["author"],
                "title": row["title"],
                "year": row["year"],
                "url": row["url"] or "",
            },
        )


def main():
    with sqlite3.connect(SOURCE_DB) as conn:
        transfer(conn)
    print(f"Пользователей: {User.objects.count()}")
    print(f"Исследований: {Research.objects.count()}")
    print(f"Источников: {Source.objects.count()}")


if __name__ == "__main__":
    main()
