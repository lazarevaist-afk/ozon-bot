import sqlite3
from datetime import datetime, timedelta

DB = "bot.db"


def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS sellers (
        name TEXT,
        added_at TEXT
    )
    """)

    conn.commit()
    conn.close()


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


def add_seller(name: str):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute(
        "INSERT INTO sellers VALUES (?, ?)",
        (name, datetime.utcnow().isoformat())
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
