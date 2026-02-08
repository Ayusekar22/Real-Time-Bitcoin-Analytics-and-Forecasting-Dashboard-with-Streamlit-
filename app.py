# app.py
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from datetime import timedelta

from src.analysis.load_data import load_price_history
from src.analysis.moving_averages  import add_moving_averages
from src.analysis.support_resistance import add_support_resistance
from src.analysis.market_signal import generate_market_signal
from src.analysis.volatility import add_volatility_features

from src.analysis.summary_metrics import get_summary_metrics
from src.fetch.fetch_realtime import run as fetch_realtime


st.set_page_config(
    page_title="Crypto Market Dashboard",
    layout="wide"
)

st.title("📊 Bitcoin Live Market Dashboard")

timeframe = st.selectbox(
    "⏱ Timeframe",
    ["1H", "6H", "24H", "7D", "30D"],
    index=2
)


# ======================
# REFRESH BUTTON
# ======================
if st.button("🔄 Refresh Data"):
    fetch_realtime()   # insert realtime row
    st.rerun()


def filter_timeframe(df, timeframe):
    now = df["timestamp"].max()

    if timeframe == "1H":
        return df[df["timestamp"] >= now - timedelta(hours=1)]
    if timeframe == "6H":
        return df[df["timestamp"] >= now - timedelta(hours=6)]
    if timeframe == "24H":
        return df[df["timestamp"] >= now - timedelta(days=1)]
    if timeframe == "7D":
        return df[df["timestamp"] >= now - timedelta(days=7)]
    if timeframe == "30D":
        return df[df["timestamp"] >= now - timedelta(days=30)]

    return df

# ======================
# LOAD & ANALYZE DATA
# ======================
df = load_price_history()
df = add_moving_averages(df)
df = add_support_resistance(df)
df = add_volatility_features(df)

df = filter_timeframe(df, timeframe)

signal = generate_market_signal(df)
summary = get_summary_metrics(df)

# ======================
# METRICS
# ======================
col1, col2, col3, col4 = st.columns(4)

col1.metric("💰 Price", f"${summary['current_price']:,.2f}")
col2.metric("📈 % Change", f"{summary['pct_change']:.2f}%")
col3.metric("🌪 Volatility", f"{summary['volatility']:.2f}")
col4.metric("🚦 Signal", signal)

# ======================
# PRICE CHART
# ======================
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=df["timestamp"],
    y=df["price"],
    name="Price",
    line=dict(color="white")
))

fig.add_trace(go.Scatter(
    x=df["timestamp"],
    y=df["sma_5"],
    name="SMA 5",
))

fig.add_trace(go.Scatter(
    x=df["timestamp"],
    y=df["sma_20"],
    name="SMA 20",
))

fig.add_trace(go.Scatter(
    x=df["timestamp"],
    y=df["support"],
    name="Support",
    line=dict(dash="dot")
))

fig.add_trace(go.Scatter(
    x=df["timestamp"],
    y=df["resistance"],
    name="Resistance",
    line=dict(dash="dot")
))

fig.update_layout(
    height=600,
    xaxis_title="Time",
    yaxis_title="Price (USD)",
    template="plotly_dark"
)

st.plotly_chart(fig, use_container_width=True)
