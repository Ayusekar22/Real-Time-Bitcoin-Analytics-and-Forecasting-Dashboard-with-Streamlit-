import sqlite3
import pandas as pd
from pathlib import Path

DB_PATH = Path("data/crypto.db")

def main():
    conn = sqlite3.connect(DB_PATH)

    # ambil 10 data terbaru
    df = pd.read_sql("""
        SELECT
            timestamp,
            datetime(timestamp, 'unixepoch') AS datetime,
            price,
            volume,
            market_cap
        FROM price_history
        ORDER BY timestamp DESC
        LIMIT 25
    """, conn)

    conn.close()

    print("\n📊 SAMPLE DATA (LATEST 10 ROWS)")
    print(df)

if __name__ == "__main__":
    main()
