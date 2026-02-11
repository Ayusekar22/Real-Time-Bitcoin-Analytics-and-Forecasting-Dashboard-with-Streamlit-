# 📊 Live Bitcoin Market Dashboard with Trend Analysis & Price Prediction

A **real-time Bitcoin market dashboard** built with **Python & Streamlit**, featuring live price updates, technical indicators, volatility analysis, and short-term price prediction using **Linear Regression**.

---

## Quick Overview

This project is a **real-time Bitcoin market dashboard** that integrates incremental data ingestion, technical analysis, and short-term price forecasting.

It fetches Bitcoin price data at 5-minute intervals, stores it efficiently in SQLite, computes market indicators and volatility, and visualizes both historical trends and near-term predictions through an interactive Streamlit dashboard.


---

## System Flow

1. User opens the Streamlit dashboard  
2. Application loads historical Bitcoin data from SQLite  
3. On refresh:
   - Retrieves last stored timestamp
   - Fetches only missing data from CoinGecko
   - Stores new records without duplication
4. Data is processed:
   - Timeframe filtering
   - Technical indicators calculation
   - Volatility and market signal generation
5. Short-term price prediction is generated using Linear Regression
6. Results are visualized in an interactive dashboard

---

## Data Pipeline

* Fetches **Bitcoin 30 days market data** incrementally from CoinGecko 
* Stores data in **SQLite** (`price_history` table)
* Designed to avoid duplicate timestamps
* Supports frequent refresh (crypto runs 24/7)

## 📈 Market Analysis

* **Simple Moving Averages (SMA 5 & SMA 20)**
* **Support & Resistance** levels 
* **Volatility calculation** using price returns
* **Market Signal** generation (Buy / Sell / Hold / Not Enough Data)

## 🔮 Price Prediction

* Uses **Linear Regression** on resampled **5-minute data**
* Trained on rolling windows (default: last 24 hours)
* Predicts **next 1 hour (12 × 5-minute steps)**
* Prediction is **anchored to the latest actual price** to avoid unrealistic jumps

## Interactive Dashboard (Streamlit)
* Selectable timeframe: `1H`, `6H`, `24H`, `7D`, `30D`
* Live refresh button
* Plotly-based dark-themed chart
* Overlay of actual price, indicators, and prediction line

---

## Project Structure

```
Live-Cryptocurrency-Market-Dashboard-with-Trend-Analysis/
│
├── app.py                          # Streamlit dashboard
├── data/
│   └── crypto.db                   # SQLite database
│
├── src/
│   ├── fetch/
│   │   └── fetch_incremental.py    # Incremental data fetching
│   │
│   ├── analysis/ 
│   │   ├── load_data.py
│   │   ├── moving_averages.py
│   │   ├── support_resistance.py
│   │   ├── volatility.py
│   │   ├── market_signal.py
│   │   └── summary_metrics.py
│   │   └── trend_features.py
│   │   └── validate_data.py
│   │
│   ├── prediction/
│   │   └── prediction.py           # Linear regression prediction
│   │
│   └── db/
│       └── init_db.py              # Database initialization
│
└── README.md
```

## 📦 Database Schema

```sql
CREATE TABLE price_history (
    timestamp INTEGER PRIMARY KEY,
    price REAL,
    volume REAL,
    market_cap REAL
);
```

* `timestamp` stored in **Unix seconds**
* Converted to local timezone (`Asia/Jakarta`) during analysis

---

## Project Limitations

* Prediction model is **baseline (Linear Regression)**
* Designed for **short-term trend illustration**, not financial advice
* Volatility may appear low on very short timeframes
* Market signal depends on available data window

---

## Project Overview 
![Dashboard](data/BitcoinDashboard.gif)

## License

This project is licensed under the MIT License.

![License](data/License.svg)

---

## Contact

If you have any questions or feedback, feel free to reach out:
- **Email:** Ayusekar1822@gmail.com
- **LinkedIn:** https://www.linkedin.com/in/ayusekar22/
- **GitHub:** https://github.com/Ayusekar22

