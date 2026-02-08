import time
import requests
from src.db.database import get_connection
from src.fetch.utils import get_last_timestamp
from src.config import COINGECKO_API_KEY

COIN_ID = "bitcoin"
VS_CURRENCY = "usd"

def fetch_latest_price():
    url = "https://api.coingecko.com/api/v3/simple/price"

    params = {
        "ids": COIN_ID,
        "vs_currencies": VS_CURRENCY,
        "include_market_cap": "true",
        "include_24hr_vol": "true",
        "x_cg_demo_api_key": COINGECKO_API_KEY
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

def insert_if_new(data):
    btc = data[COIN_ID]
    now = int(time.time())

    last_ts = get_last_timestamp()

    # minimal 60 detik beda
    if last_ts and now - last_ts < 60:
        print("Skip insert (too soon)")
        return

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO price_history (timestamp, price, volume, market_cap)
        VALUES (?, ?, ?, ?)
    """, (
        now,
        btc["usd"],
        btc["usd_24h_vol"],
        btc["usd_market_cap"]
    ))

    conn.commit()
    conn.close()
    print("Realtime row inserted")

def run():
    data = fetch_latest_price()
    insert_if_new(data)

if __name__ == "__main__":
    run()
