import pandas as pd


df = pd.read_csv(
    "data/historical_ml_dataset.csv"
)


df["Volatility_Group"] = pd.qcut(
    df["ATR_Percent"],
    5,
    labels=[
        "Very Low",
        "Low",
        "Medium",
        "High",
        "Very High"
    ]
)


result = (
    df.groupby("Volatility_Group",
               observed=True)["Successful_Trade"]
    .mean()
    * 100
)


print("\nSuccess Rate by Volatility\n")
print(result)
