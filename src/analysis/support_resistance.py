def add_support_resistance(df, window=20):
    df = df.copy()

    df["resistance"] = df["price"].rolling(window).max()
    df["support"] = df["price"].rolling(window).min()

    return df
