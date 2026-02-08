# def get_summary_metrics(df):
#     df = df.dropna().copy()

#     # ======================
#     # CURRENT PRICE
#     # ======================
#     current_price = df["price"].iloc[-1]

#     # ======================
#     # % CHANGE (20 periods)
#     # ======================
#     past_price = df["price"].iloc[-20]
#     pct_change = ((current_price - past_price) / past_price) * 100

#     # ======================
#     # VOLATILITY (avg 20)
#     # ======================
#     volatility = df["volatility"].tail(20).mean()

#     return {
#         "current_price": current_price,
#         "pct_change": pct_change,
#         "volatility": volatility,
#     }

def get_summary_metrics(df):
    latest = df.iloc[-1]

    # kalau data sedikit, pakai data paling awal
    lookback = min(20, len(df) - 1)

    if lookback <= 0:
        pct_change = 0.0
    else:
        past_price = df["price"].iloc[-(lookback + 1)]
        pct_change = ((latest["price"] - past_price) / past_price) * 100

    return {
        "current_price": latest["price"],
        "pct_change": pct_change,
        "volatility": latest.get("volatility", 0),
        "timestamp": latest["timestamp"]
    }
