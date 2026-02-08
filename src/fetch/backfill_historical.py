import requests
from src.db.database import get_connection
from src.config import COINGECKO_API_KEY

COIN_ID = "bitcoin"
VS_CURRENCY = "usd"
DAYS = 30  

def fetch_historical_data():
    url = f"https://api.coingecko.com/api/v3/coins/{COIN_ID}/market_chart"

    params = {
        "vs_currency": VS_CURRENCY,
        "days": DAYS,
        "x_cg_demo_api_key": COINGECKO_API_KEY
    
    }

    headers = {
        "User-Agent": "crypto-dashboard/1.0"
    }

    response = requests.get(url, params=params, headers=headers)

    # DEBUG helper (penting kalau error lagi)
    if response.status_code != 200:
        print("STATUS:", response.status_code)
        print("RESPONSE:", response.text)

    response.raise_for_status()
    return response.json()


def insert_historical_data(data):
    conn = get_connection()
    cursor = conn.cursor()

    prices = data["prices"]
    volumes = data["total_volumes"]
    market_caps = data["market_caps"]

    for i in range(len(prices)):
        timestamp = int(prices[i][0] / 1000)  # ms → s
        price = prices[i][1]
        volume = volumes[i][1]
        market_cap = market_caps[i][1]

        cursor.execute("""
            INSERT OR IGNORE INTO price_history
            (timestamp, price, volume, market_cap)
            VALUES (?, ?, ?, ?)
        """, (timestamp, price, volume, market_cap))

    conn.commit()
    conn.close()

def run_backfill():
    data = fetch_historical_data()
    insert_historical_data(data)
    print("Historical backfill completed")

if __name__ == "__main__":
    run_backfill()
