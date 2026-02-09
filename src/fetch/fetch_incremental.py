# import requests
# import time
# from src.db.database import get_connection
# from src.fetch.utils import get_last_timestamp, get_days_to_fetch
# from src.config import COINGECKO_API_KEY

# COIN_ID = "bitcoin"
# VS_CURRENCY = "usd"

# def fetch_incremental_data(days):
#     url = f"https://api.coingecko.com/api/v3/coins/{COIN_ID}/market_chart"
#     params = {
#         "vs_currency": VS_CURRENCY,
#         "days": days,
#         "interval": "hourly"
#     }

#     r = requests.get(url, params=params)
#     r.raise_for_status()
#     return r.json()

# def insert_data(data):
#     conn = get_connection()
#     cur = conn.cursor()

#     last_ts = get_last_timestamp()

#     for i in range(len(data["prices"])):
#         ts = int(data["prices"][i][0] / 1000)

#         if ts <= last_ts:
#             continue

#         price = data["prices"][i][1]
#         volume = data["total_volumes"][i][1]
#         cap = data["market_caps"][i][1]

#         cur.execute("""
#             INSERT INTO price_history
#             (timestamp, price, volume, market_cap)
#             VALUES (?, ?, ?, ?)
#         """, (ts, price, volume, cap))

#     conn.commit()
#     conn.close()

# def run():
#     last_ts = get_last_timestamp()
#     days = get_days_to_fetch(last_ts)

#     print(f"Fetching last {days} day(s)")
#     data = fetch_incremental_data(days)
#     insert_data(data)

# if __name__ == "__main__":
#     run()

import requests
from src.db.database import get_connection
from src.fetch.utils import get_last_timestamp, get_days_to_fetch

COIN_ID = "bitcoin"
VS_CURRENCY = "usd"

HEADERS = {
    "User-Agent": "CryptoDashboard/1.0 (contact: ayu@example.com)"
}

def fetch_incremental_data(days):
    url = f"https://api.coingecko.com/api/v3/coins/{COIN_ID}/market_chart"
    params = {
        "vs_currency": VS_CURRENCY,
        "days": days
    }

    r = requests.get(url, params=params, headers=HEADERS, timeout=15)
    r.raise_for_status()
    return r.json()

def insert_data(data):
    conn = get_connection()
    cur = conn.cursor()

    last_ts = get_last_timestamp()

    for i in range(len(data["prices"])):
        ts = int(data["prices"][i][0] / 1000)

        if last_ts and ts <= last_ts:
            continue

        price = data["prices"][i][1]
        volume = data["total_volumes"][i][1]
        cap = data["market_caps"][i][1]

        cur.execute("""
            INSERT OR IGNORE INTO price_history
            (timestamp, price, volume, market_cap)
            VALUES (?, ?, ?, ?)
        """, (ts, price, volume, cap))

    conn.commit()
    conn.close()

def run():
    last_ts = get_last_timestamp()
    days = get_days_to_fetch(last_ts)

    print(f"Fetching last {days} day(s)")
    data = fetch_incremental_data(days)
    insert_data(data)

if __name__ == "__main__":
    run()
