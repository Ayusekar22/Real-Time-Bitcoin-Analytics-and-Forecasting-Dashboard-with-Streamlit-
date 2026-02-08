

def add_volatility_features(df, window=20):
    df = df.copy()

    # hitung pct_change dulu
    df["pct_change"] = df["price"].pct_change()

    # volatility = std dari pct_change
    df["volatility"] = df["pct_change"].rolling(window).std()

    return df
