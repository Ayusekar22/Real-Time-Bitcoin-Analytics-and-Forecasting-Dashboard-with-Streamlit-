# import numpy as np
# import pandas as pd
# from sklearn.linear_model import LinearRegression


# def add_prediction_line(df, horizon=24):
#     """
#     horizon: berapa jam ke depan mau diprediksi
#     """
#     df = df.copy()

#     # pastikan timestamp datetime
#     df["ts_num"] = (
#         pd.to_datetime(df["timestamp"])
#         .astype("int64") // 10**9
#     )

#     X = df["ts_num"].values.reshape(-1, 1)
#     y = df["price"].values

#     model = LinearRegression()
#     model.fit(X, y)

#     # future timestamps
#     last_ts = df["ts_num"].iloc[-1]
#     future_ts = np.array([
#         last_ts + 3600 * i for i in range(1, horizon + 1)
#     ]).reshape(-1, 1)

#     future_price = model.predict(future_ts)

#     df_future = pd.DataFrame({
#         "timestamp": pd.to_datetime(future_ts.flatten(), unit="s"),
#         "predicted_price": future_price
#     })

#     return df_future

import sqlite3
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

def load_price_data(db_path="data/crypto.db"):
    conn = sqlite3.connect(db_path)
    df = pd.read_sql("""
        SELECT timestamp, price
        FROM price_history
        ORDER BY timestamp
    """, conn)
    conn.close()

    df["datetime"] = pd.to_datetime(df["timestamp"], unit="s")
    return df.set_index("datetime")

def prepare_5m_data(df):
    df_5m = df.resample("5T").last()
    df_5m["price"] = df_5m["price"].interpolate()
    return df_5m.dropna()

def predict_linear(df_5m, window=288, steps=12):
    df_window = df_5m.tail(window)

    X = np.arange(len(df_window)).reshape(-1, 1)
    y = df_window["price"].values

    model = LinearRegression()
    model.fit(X, y)

    X_future = np.arange(len(X), len(X) + steps).reshape(-1, 1)
    preds = model.predict(X_future)

    last_price = y[-1]
    preds = preds - preds[0] + last_price

    last_time = df_window.index[-1]

    now = (
        pd.Timestamp.now(tz="Asia/Jakarta")
        .floor("5min")
        .tz_localize(None)
    )

    start_time = max(
        last_time + pd.Timedelta(minutes=5),
        now
    )

    future_time = pd.date_range(
        start=start_time,
        periods=steps,
        freq="5min"
    )

    return pd.DataFrame({
        "datetime": future_time,
        "predicted_price": preds
    })

