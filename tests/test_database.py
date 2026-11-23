"""Тесты переноса данных в SQLite и запросов"""
import sqlite3

import pytest

from db.database import RELEVANCE, fetch_all, fetch_one, get_connection
from db.import_json import import_all


@pytest.fixture
def db_path(tmp_path):
    path = str(tmp_path / "test.sqlite")
    conn = get_connection(path)
    import_all(conn)
    conn.commit()
    conn.close()
    return path


def test_import_counts(db_path):
    """Все записи из JSON попадают в таблицы"""
    row = fetch_one(
        "SELECT (SELECT COUNT(*) FROM users) AS users_count, "
        "(SELECT COUNT(*) FROM sources) AS sources_count",
        path=db_path,
    )
    assert row["users_count"] == 3
    assert row["sources_count"] == 10


def test_join_and_group_by(db_path):
    """У каждого исследования считается число источников"""
    rows = fetch_all(
        """
        SELECT researches.id, COUNT(sources.id) AS sources_count
        FROM researches
        LEFT JOIN sources ON sources.research_id = researches.id
        GROUP BY researches.id
        """,
        path=db_path,
    )
    assert sum(row["sources_count"] for row in rows) == 10


def test_relevance(db_path):
    """Актуальность считается в запросе"""
    rows = fetch_all(
        f"SELECT {RELEVANCE} AS relevance FROM sources", path=db_path
    )
    assert {row["relevance"] for row in rows} <= {
        "актуальный", "требует проверки", "устаревший",
    }


def test_foreign_key(db_path):
    """Нельзя добавить источник к несуществующему исследованию"""
    conn = get_connection(db_path)
    with pytest.raises(sqlite3.IntegrityError):
        conn.execute(
            "INSERT INTO sources (research_id, user_id, author, title, year)"
            " VALUES (?, ?, ?, ?, ?)",
            (999, 1, "А", "Б", 2020),
        )
    conn.close()
