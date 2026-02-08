import sqlite3
from pathlib import Path

DB_PATH = Path("data/crypto.db")

def get_connection():
    DB_PATH.parent.mkdir(exist_ok=True)
    return sqlite3.connect(DB_PATH)

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS price_history (
            timestamp INTEGER PRIMARY KEY,
            price REAL,
            volume REAL,
            market_cap REAL
        )
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tables()
    print("Database & table created successfully.")
