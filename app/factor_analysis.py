import pandas as pd


DATABASE = "data/trade_database.csv"


def analyze():

    df = pd.read_csv(DATABASE)

    closed = df[
        df["Result"] != "OPEN"
    ].copy()


    closed["Win"] = (
        closed["Result"]
        .str.contains("TARGET")
        .astype(int)
    )


    print("\n===== FACTOR ANALYSIS =====\n")


    factors = [
        "Rank_Score",
        "Momentum_Score",
        "Trend_Score",
        "Relative_Strength",
        "Risk_Reward"
    ]


    for factor in factors:

        print("\n--------------------")
        print(factor)

        print(
            closed.groupby(
                pd.cut(
                   closed[factor],
                   bins=[
                       -1,
                       10,
                       20,
                       25,
                       30,
                       100
                   ]
                )
            )
            .agg(
                Trades=("Win","count"),
                Win_Rate=("Win","mean"),
                Avg_Return=("Return_%","mean")
            )
        )


if __name__ == "__main__":

    analyze()
