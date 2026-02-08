import requests
import sqlite3
from datetime import datetime
from src.db.database import get_connection

COIN_ID = "bitcoin"
VS_CURRENCY = "usd"

def fetch_bitcoin_data():
    url = f"https://api.coingecko.com/api/v3/coins/{COIN_ID}"
    params = {
        "localization": "false",
        "tickers": "false",
        "market_data": "true",
        "community_data": "false",
        "developer_data": "false",
        "sparkline": "false"
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    market_data = data["market_data"]

    return {
        "timestamp": int(datetime.utcnow().timestamp()),
        "price": market_data["current_price"][VS_CURRENCY],
        "volume": market_data["total_volume"][VS_CURRENCY],
        "market_cap": market_data["market_cap"][VS_CURRENCY],
    }

def insert_price_data(record):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO price_history (timestamp, price, volume, market_cap)
        VALUES (?, ?, ?, ?)
    """, (
        record["timestamp"],
        record["price"],
        record["volume"],
        record["market_cap"]
    ))

    conn.commit()
    conn.close()

def fetch_and_store():
    record = fetch_bitcoin_data()
    insert_price_data(record)
    print(f"Inserted data at {record['timestamp']}")

if __name__ == "__main__":
    fetch_and_store()
