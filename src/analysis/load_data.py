import sqlite3
import pandas as pd
from pathlib import Path

DB_PATH = Path("data/crypto.db")

def load_price_history(limit=None):
    conn = sqlite3.connect(DB_PATH)

    query = """
        SELECT
            timestamp,
            price,
            volume,
            market_cap
        FROM price_history
        ORDER BY timestamp ASC
    """

    if limit:
        query += f" LIMIT {limit}"

    df = pd.read_sql_query(query, conn)
    conn.close()

    # convert unix timestamp → datetime
    df["timestamp"] = (
    pd.to_datetime(df["timestamp"], unit="s", utc=True)
      .dt.tz_convert("Asia/Jakarta")
      .dt.tz_localize(None)
)

    return df
