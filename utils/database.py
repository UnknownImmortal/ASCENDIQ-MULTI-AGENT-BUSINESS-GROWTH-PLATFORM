import sqlite3
import os

DB_PATH = "growthpilot.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS analyses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            business_type TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            report_summary TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_analysis(business_type: str, report_summary: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "INSERT INTO analyses (business_type, report_summary) VALUES (?, ?)",
        (business_type, report_summary[:500])
    )
    conn.commit()
    conn.close()

def get_recent_analyses(limit: int = 5):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "SELECT business_type, timestamp FROM analyses ORDER BY timestamp DESC LIMIT ?",
        (limit,)
    )
    rows = c.fetchall()
    conn.close()
    return rows

init_db()
