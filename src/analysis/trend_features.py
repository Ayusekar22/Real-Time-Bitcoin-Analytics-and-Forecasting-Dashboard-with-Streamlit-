def add_trend_features(df):
    df = df.copy()

    df["sma_5"] = df["price"].rolling(5).mean()
    df["sma_20"] = df["price"].rolling(20).mean()

    df["price_change"] = df["price"].diff()
    df["pct_change"] = df["price"].pct_change() * 100

    df["momentum_10"] = df["price"] - df["price"].shift(10)

    return df
