from src.analysis.load_data import load_price_history

def validate():
    df = load_price_history()

    print("Rows:", len(df))
    print("Time range:")
    print(df["timestamp"].min(), "→", df["timestamp"].max())

    print("\nNull check:")
    print(df.isnull().sum())

if __name__ == "__main__":
    validate()
