import pandas as pd


DATABASE = "data/trade_database.csv"


def run():

    df = pd.read_csv(DATABASE)


    print("\n===== DATABASE SUMMARY =====\n")

    print("Total Trades:")
    print(len(df))


    closed = df[
        df["Result"] != "OPEN"
    ]


    print("\nClosed Trades:")
    print(len(closed))


    wins = closed[
        closed["Result"].str.contains("TARGET")
    ]


    losses = closed[
        closed["Result"] == "STOP HIT"
    ]


    print("\n===== OVERALL PERFORMANCE =====")


    print("\nWin Rate:")

    print(
        round(
            len(wins) / len(closed) * 100,
            2
        ),
        "%"
    )


    print("\nAverage Return:")

    print(
        round(
            closed["Return_%"].mean(),
            2
        ),
        "%"
    )


    print("\n===== RESULT DISTRIBUTION =====")

    print(
        df["Result"]
        .value_counts()
    )


    print("\n===== BEST TRADES =====")

    print(
        df.sort_values(
            "Return_%",
            ascending=False
        )
        [
            [
                "Symbol",
                "Return_%",
                "Result"
            ]
        ]
        .head(10)
    )


    print("\n===== WORST TRADES =====")

    print(
        df.sort_values(
            "Return_%"
        )
        [
            [
                "Symbol",
                "Return_%",
                "Result"
            ]
        ]
        .head(10)
    )



if __name__ == "__main__":

    run()
