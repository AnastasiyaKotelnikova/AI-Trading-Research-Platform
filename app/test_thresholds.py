import pandas as pd

from app.ml_backtester import run_ml_backtest


df = pd.read_csv(
    "data/price_history/META_prices.csv"
)


for threshold in [
    0.50,
    0.55,
    0.60,
    0.65,
    0.70,
    0.75
]:

    print("\n====================")
    print("Threshold:", threshold)

    results = run_ml_backtest(
        df,
        probability_threshold=threshold
    )
