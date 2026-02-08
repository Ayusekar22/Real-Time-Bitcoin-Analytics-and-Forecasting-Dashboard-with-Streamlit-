from src.analysis.load_data import load_price_history
from src.analysis.trend_features import add_trend_features
from src.analysis.volatility import add_volatility_features
from src.analysis.support_resistance import add_support_resistance
from src.analysis.market_signal import generate_market_signal
from src.analysis.summary_metrics import get_summary_metrics

def main():
    df = load_price_history()

    df = add_trend_features(df)
    df = add_volatility_features(df)
    df = add_support_resistance(df)

    print(df.tail(5)[[
        "price",
        "sma_5",
        "sma_20",
        "rolling_std",
        "support",
        "resistance"
    ]])

    signal = generate_market_signal(df)
    metrics = get_summary_metrics(df)

    print("\nMarket Signal:", signal)
    print("\nSummary Metrics:")
    for k, v in metrics.items():
        print(f"{k}: {v}")

if __name__ == "__main__":
    main()
