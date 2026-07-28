import pandas as pd


DATABASE = "data/trade_database.csv"


def run():

    df = pd.read_csv(DATABASE)


    closed = df[
        df["Result"] != "OPEN"
    ]


    print("\n===== RANK SCORE ANALYSIS =====\n")


    bins = [
        0,
        70,
        80,
        90,
        100
    ]

    labels = [
        "<70",
        "70-79",
        "80-89",
        "90+"
    ]


    closed["Rank_Group"] = pd.cut(
        closed["Rank_Score"],
        bins=bins,
        labels=labels
    )


    summary = (
        closed
        .groupby("Rank_Group", observed=True)
        .agg(
            Trades=("Return_%","count"),
            Avg_Return=("Return_%","mean")
        )
    )


    print(summary)


    print("\n===== WIN RATE BY RANK =====\n")


    closed["Win"] = (
        closed["Result"]
        .str.contains("TARGET")
    )


    win_rate = (
        closed
        .groupby(
            "Rank_Group",
            observed=True
        )
        ["Win"]
        .mean()
        *
        100
    )


    print(win_rate)



if __name__ == "__main__":

    run()
