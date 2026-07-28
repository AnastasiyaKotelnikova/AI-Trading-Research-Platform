import pandas as pd


INPUT_FILE = "data/backtest_results/portfolio_backtest.csv"

OUTPUT_FILE = "data/backtest_results/portfolio_backtest_with_dates.csv"


HOLD_DAYS = 5


df = pd.read_csv(INPUT_FILE)


df["Entry_Date"] = pd.to_datetime(
    df["Entry_Date"]
)


df = df.sort_values(
    "Entry_Date"
)


df["Exit_Date"] = (
    df["Entry_Date"]
    +
    pd.to_timedelta(
        HOLD_DAYS,
        unit="D"
    )
)


df.to_csv(
    OUTPUT_FILE,
    index=False
)


print("Saved:")
print(OUTPUT_FILE)


print()

print(df.head())
