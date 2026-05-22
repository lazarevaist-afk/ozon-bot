import sqlite3
from datetime import datetime, timedelta

DB = "bot.db"


def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    # пользователи (доступ)
    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY
    )
    """)

    # продавцы / лиды (SAAS-структура)
    c.execute("""
    CREATE TABLE IF NOT EXISTS sellers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        title TEXT,
        link TEXT,
        query TEXT,
        added_at TEXT
    )
    """)

    conn.commit()
    conn.close()


# ================= USERS =================

def add_user(user_id: int):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO users VALUES (?)", (user_id,))
    conn.commit()
    conn.close()


def is_allowed(user_id: int) -> bool:
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT user_id FROM users WHERE user_id=?", (user_id,))
    res = c.fetchone()
    conn.close()
    return res is not None


# ================= SELLERS / LEADS =================

def add_seller(name: str, title: str, link: str, query: str):
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute(
        """
        INSERT INTO sellers (name, title, link, query, added_at)
        VALUES (?, ?, ?, ?, ?)
        """,
        (name, title, link, query, datetime.utcnow().isoformat())
    )

    conn.commit()
    conn.close()


def seller_exists(name: str) -> bool:
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    limit_date = datetime.utcnow() - timedelta(days=90)

    c.execute("SELECT added_at FROM sellers WHERE name=?", (name,))
    rows = c.fetchall()

    conn.close()

    for r in rows:
        if datetime.fromisoformat(r[0]) > limit_date:
            return True

    return False


def get_sellers(limit: int = 30):
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute("""
        SELECT name, title, link, query, added_at
        FROM sellers
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))

    rows = c.fetchall()
    conn.close()

    return rows
