def generate_market_signal(df):
    if len(df) < 20:
        return "Not enough data ⏳"

    latest = df.iloc[-1]

    if latest["sma_5"] > latest["sma_20"]:
        return "Bullish 📈"
    elif latest["sma_5"] < latest["sma_20"]:
        return "Bearish 📉"
    else:
        return "Sideways ⚖️"
