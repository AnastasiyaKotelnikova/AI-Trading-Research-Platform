import time
import os
import pandas as pd

from app.features import build_features
from app.ml_backtester import run_ml_backtest

PRICE_FOLDER = "data/price_history"

files = [
    f
    for f in os.listdir(PRICE_FOLDER)
    if f.endswith("_prices.csv")
][:20]      # first 20 stocks only

csv_time = 0
feature_time = 0
ml_time = 0

for file in files:

    path = os.path.join(
        PRICE_FOLDER,
        file
    )

    t = time.perf_counter()
    df = pd.read_csv(path)
    csv_time += time.perf_counter() - t

    t = time.perf_counter()
    build_features(df.copy())
    feature_time += time.perf_counter() - t

    t = time.perf_counter()
    run_ml_backtest(
        df,
        verbose=False
    )
    ml_time += time.perf_counter() - t

print()
print("CSV Load:", round(csv_time,2),"sec")
print("Feature Build:", round(feature_time,2),"sec")
print("ML Backtest:", round(ml_time,2),"sec")
