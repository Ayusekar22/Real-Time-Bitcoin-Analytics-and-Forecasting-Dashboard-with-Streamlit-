import sqlite3
from src.db.database import DB_PATH

def get_last_timestamp():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT MAX(timestamp) FROM price_history")
    result = cursor.fetchone()[0]

    conn.close()
    return result
