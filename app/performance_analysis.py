import pandas as pd


INPUT_FILE = (
    "data/backtest_results/"
    "portfolio_backtest_with_dates.csv"
)


def main():

    df = pd.read_csv(INPUT_FILE)

    df["Entry_Date"] = pd.to_datetime(df["Entry_Date"])

    print("\n==============================")
    print(" STRATEGY PERFORMANCE ANALYSIS")
    print("==============================")

    print()

    print("Total Trades:", len(df))

    print(
        "Average Return:",
        round(df["Return_%"].mean(), 2),
        "%"
    )

    print(
        "Median Return:",
        round(df["Return_%"].median(), 2),
        "%"
    )

    print(
        "Win Rate:",
        round(
            (df["Return_%"] > 0).mean() * 100,
            2
        ),
        "%"
    )

    print("\n===== BEST SYMBOLS =====")

    symbol_stats = (
        df.groupby("Symbol")
        .agg(
            Trades=("Return_%", "count"),
            Avg_Return=("Return_%", "mean"),
            Win_Rate=("Return_%",
                      lambda x: (x > 0).mean() * 100)
        )
        .sort_values(
            "Avg_Return",
            ascending=False
        )
    )

    print(symbol_stats.head(20))

    print("\n===== PROBABILITY ANALYSIS =====")

    bins = [0.50, 0.55, 0.60, 0.65,
            0.70, 0.75, 0.80, 1.00]

    labels = [
        "0.50-0.55",
        "0.55-0.60",
        "0.60-0.65",
        "0.65-0.70",
        "0.70-0.75",
        "0.75-0.80",
        "0.80+"
    ]

    df["Probability_Range"] = pd.cut(
        df["Prediction_Probability"],
        bins=bins,
        labels=labels
    )

    probability_stats = (
        df.groupby("Probability_Range")
        .agg(
            Trades=("Return_%", "count"),
            Avg_Return=("Return_%", "mean"),
            Win_Rate=("Return_%",
                      lambda x: (x > 0).mean() * 100)
        )
    )

    print(probability_stats)

    print("\n===== MONTHLY PERFORMANCE =====")

    df["Month"] = (
        df["Entry_Date"]
        .dt.to_period("M")
    )

    monthly = (
        df.groupby("Month")
        .agg(
            Trades=("Return_%", "count"),
            Avg_Return=("Return_%", "mean"),
            Win_Rate=("Return_%",
                      lambda x: (x > 0).mean() * 100)
        )
    )

    print(monthly)


if __name__ == "__main__":
    main()
