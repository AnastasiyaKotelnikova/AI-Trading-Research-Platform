import os
import pandas as pd


PERFORMANCE_FOLDER = "data/performance_history"


def load_history():

    files = [
        os.path.join(PERFORMANCE_FOLDER, f)
        for f in os.listdir(PERFORMANCE_FOLDER)
        if f.endswith("_performance.csv")
    ]

    if not files:
        raise FileNotFoundError(
            "No performance history found."
        )

    dfs = [
        pd.read_csv(f)
        for f in files
    ]

    return pd.concat(
        dfs,
        ignore_index=True
    )


def run():

    df = load_history()

    print("\n===== STRATEGY PERFORMANCE =====\n")

    strategy = (
        df.groupby("Strategy")
        .agg(
            Trades=("Symbol", "count"),
            Avg_Return=("Return_%", "mean")
        )
        .sort_values(
            "Avg_Return",
            ascending=False
        )
    )

    print(strategy)


    print("\n===== SECTOR PERFORMANCE =====\n")

    sector = (
        df.groupby("Sector")
        .agg(
            Trades=("Symbol", "count"),
            Avg_Return=("Return_%", "mean")
        )
        .sort_values(
            "Avg_Return",
            ascending=False
        )
    )

    print(sector)


    print("\n===== CONFIDENCE SCORE =====\n")

    confidence = (
        df.groupby("Confidence_Score")
        .agg(
            Trades=("Symbol", "count"),
            Avg_Return=("Return_%", "mean")
        )
        .sort_values(
            "Confidence_Score",
            ascending=False
        )
    )

    print(confidence)


if __name__ == "__main__":

    run()
