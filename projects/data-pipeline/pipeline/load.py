import os
import sqlite3
import pandas as pd
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "trending.db")

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS repo_snapshots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            snapshot_date TEXT NOT NULL,
            full_name TEXT NOT NULL,
            owner TEXT,
            description TEXT,
            stars INTEGER,
            forks INTEGER,
            open_issues INTEGER,
            language TEXT,
            topics TEXT,
            license TEXT,
            created_at TEXT,
            updated_at TEXT,
            url TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS daily_summary (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            snapshot_date TEXT UNIQUE NOT NULL,
            total_repos INTEGER,
            avg_stars REAL,
            top_language TEXT,
            snapshot_count INTEGER
        )
    """)
    conn.commit()
    return conn

def save_snapshot(df: pd.DataFrame, conn: sqlite3.Connection):
    today = datetime.now().strftime("%Y-%m-%d")
    df = df.copy()
    df["snapshot_date"] = today
    df.to_sql("repo_snapshots", conn, if_exists="append", index=False)

def update_summary(conn: sqlite3.Connection):
    today = datetime.now().strftime("%Y-%m-%d")
    df = pd.read_sql(f"SELECT * FROM repo_snapshots WHERE snapshot_date = '{today}'", conn)
    if df.empty:
        return
    conn.execute("""
        INSERT OR REPLACE INTO daily_summary (snapshot_date, total_repos, avg_stars, top_language, snapshot_count)
        VALUES (?, ?, ?, ?, ?)
    """, (
        today,
        len(df),
        round(df["stars"].mean(), 1),
        df["language"].mode().iloc[0] if not df.empty else "Unknown",
        len(df),
    ))
    conn.commit()

def get_history(conn: sqlite3.Connection) -> pd.DataFrame:
    return pd.read_sql("SELECT * FROM daily_summary ORDER BY snapshot_date", conn)
