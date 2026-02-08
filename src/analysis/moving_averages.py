# src/analysis/moving_average.py

def add_moving_averages(df, short_window=5, long_window=20):
    df = df.copy()

    df[f"sma_{short_window}"] = df["price"].rolling(window=short_window).mean()
    df[f"sma_{long_window}"] = df["price"].rolling(window=long_window).mean()

    return df
