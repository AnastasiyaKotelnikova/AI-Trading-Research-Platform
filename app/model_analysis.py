import pandas as pd


DATA_FILE = "data/historical_ml_dataset.csv"


df = pd.read_csv(DATA_FILE)


print("\n===== FEATURE CORRELATION WITH SUCCESS =====\n")


features = [
    "Return_5D",
    "Return_10D",
    "Return_20D",
    "RSI",
    "SMA_Gap",
    "ATR",
    "ATR_Percent",
    "Volatility_20D",
    "RVOL",
    "Volume_Trend",
    "Distance_From_52W_High"
]


corr = (
    df[features + ["Successful_Trade"]]
    .corr()["Successful_Trade"]
    .sort_values(
        ascending=False
    )
)


print(corr)
