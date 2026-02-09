from src.prediction.prediction import (
    load_price_data,
    prepare_5m_data,
    predict_linear
)
    
df = load_price_data()
df_5m = prepare_5m_data(df)
pred = predict_linear(df_5m)

print(pred)
