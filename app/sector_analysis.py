import pandas as pd


DATABASE_FILE = "data/trade_database.csv"


def sector_analysis():

    df = pd.read_csv(DATABASE_FILE)


    print("\n===== SECTOR PERFORMANCE =====\n")


    results = (
        df.groupby("Sector")
        .agg(
            Trades=("Symbol","count"),
            Win_Rate=("Return_%", lambda x: (x > 0).mean() * 100),
            Avg_Return=("Return_%","mean")
        )
        .sort_values(
            "Avg_Return",
            ascending=False
        )
    )


    print(results.round(2))


if __name__ == "__main__":

    sector_analysis()
