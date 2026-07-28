import pandas as pd


DATABASE_FILE = "data/trade_database.csv"



def evaluate():


    df = pd.read_csv(
        DATABASE_FILE,
        low_memory=False
    )


    # Only evaluate completed trades

    completed = df[
        df["Result"].isin(
            [
                "TARGET 1 HIT",
                "TARGET 2 HIT",
                "STOP HIT"
            ]
        )
    ]


    print("\n========== MODEL EVALUATION ==========\n")


    print("Total Samples:")
    print(len(df))


    print("\nCompleted Trades:")
    print(len(completed))


    print("\n\n===== WIN RATE =====\n")


    wins = completed[
        completed["Return_%"] > 0
    ]


    print(
        "Winning Trades:",
        len(wins)
    )


    if len(completed) > 0:

        print(
            "Win Rate:",
            round(
                len(wins) / len(completed) * 100,
                2
            ),
            "%"
        )



    print("\n\n===== STRATEGY WIN RATE =====\n")


    strategy = (
        completed.groupby("Strategy")
        ["Return_%"]
        .agg(
            [
                "count",
                "mean",
                lambda x:
                (x > 0).mean()*100
            ]
        )
    )


    strategy.columns = [
        "Trades",
        "Average Return",
        "Win Rate %"
    ]


    print(
        strategy.sort_values(
            "Average Return",
            ascending=False
        )
    )



    print("\n\n===== CONFIDENCE SCORE ANALYSIS =====\n")


    confidence = (
        completed.groupby("Confidence_Score")
        ["Return_%"]
        .agg(
            [
                "count",
                "mean",
                lambda x:
                (x > 0).mean()*100
            ]
        )
    )


    confidence.columns = [
        "Trades",
        "Average Return",
        "Win Rate %"
    ]


    print(
        confidence.sort_index(
            ascending=False
        )
    )



    print("\n\n===== FEATURE IMPORTANCE PREVIEW =====\n")


    features = [
        "Rank_Score",
        "Momentum_Score",
        "Trend_Score",
        "Relative_Strength",
        "Risk_Reward",
        "RSI",
        "Return_5D",
        "Return_20D"
    ]


    available_features = [

        f for f in features

        if f in completed.columns

    ]


    if len(available_features) > 0:

        correlation = (
            completed[
                available_features + ["Return_%"]
            ]
            .corr()["Return_%"]
            .sort_values(
                ascending=False
            )
        )


        print(
            correlation
        )

    else:

        print(
            "Feature columns not available"
        )



if __name__ == "__main__":

    evaluate()
