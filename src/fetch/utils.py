import sqlite3
from src.db.database import DB_PATH

def get_last_timestamp():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT MAX(timestamp) FROM price_history")
    result = cursor.fetchone()[0]

    conn.close()
    return result
import time

def get_days_to_fetch(last_ts):
    if not last_ts:
        return 30 

    now = int(time.time())
    diff_hours = (now - last_ts) / 3600

    if diff_hours <= 24:
        return 1
    elif diff_hours <= 168:
        return 7
    else:
        return 30

