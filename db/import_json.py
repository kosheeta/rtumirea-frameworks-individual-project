from db.database import create_tables, get_connection
from storage import RESEARCHES_FILE, SOURCES_FILE, USERS_FILE, load_json


def import_users(conn):
    conn.executemany(
        "INSERT INTO users (id, name, email) VALUES (?, ?, ?)",
        [(u["id"], u["name"], u["email"]) for u in load_json(USERS_FILE)],
    )


def import_researches(conn):
    conn.executemany(
        """
        INSERT INTO researches (id, user_id, title, description)
        VALUES (?, ?, ?, ?)
        """,
        [
            (r["id"], r["user_id"], r["title"], r["description"])
            for r in load_json(RESEARCHES_FILE)
        ],
    )


def import_sources(conn):
    conn.executemany(
        """
        INSERT INTO sources
            (id, research_id, user_id, author, title, year, url)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        [
            (
                s["id"], s["research_id"], s["user_id"], s["author"],
                s["title"], s["year"], s["url"],
            )
            for s in load_json(SOURCES_FILE)
        ],
    )


def import_all(conn):
    create_tables(conn)
    # чистим таблицы чтобы импорт можно было запускать повторно
    conn.execute("DELETE FROM sources")
    conn.execute("DELETE FROM researches")
    conn.execute("DELETE FROM users")
    import_users(conn)
    import_researches(conn)
    import_sources(conn)


def main():
    conn = get_connection()
    try:
        import_all(conn)
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
    print("данные перенесены в базу")


if __name__ == "__main__":
    main()
