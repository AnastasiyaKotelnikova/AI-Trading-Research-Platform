import pandas as pd


DATABASE = "data/trade_database.csv"


def analyze_combinations():

    df = pd.read_csv(DATABASE)

    print("\n===== COMBINATION ANALYSIS =====\n")


    # RSI groups
    df["RSI_Group"] = pd.cut(
        df["RSI"],
        bins=[0,50,60,70,80,100],
        labels=[
            "0-50",
            "50-60",
            "60-70",
            "70-80",
            "80+"
        ]
    )


    # Risk reward groups
    df["RR_Group"] = pd.cut(
        df["Risk_Reward"],
        bins=[0,2,3,5,10,100],
        labels=[
            "<2",
            "2-3",
            "3-5",
            "5-10",
            "10+"
        ]
    )


    print("\n===== RSI PERFORMANCE =====\n")

    print(
        df.groupby("RSI_Group", observed=True)
        .agg(
            Trades=("Return_%","count"),
            Win_Rate=("Return_%",
                lambda x: round((x>0).mean()*100,2)),
            Avg_Return=("Return_%","mean")
        )
        .sort_values(
            "Avg_Return",
            ascending=False
        )
    )


    print("\n===== BEST FACTOR COMBINATIONS =====\n")


    results = (
        df.groupby(
            [
                "Momentum_Score",
                "Trend_Score",
                "RSI_Group",
                "RR_Group"
            ],
            observed=True
        )
        .agg(
            Trades=("Return_%","count"),
            Win_Rate=("Return_%",
                lambda x: round((x>0).mean()*100,2)),
            Avg_Return=("Return_%","mean")
        )
        .reset_index()
    )


    results = results[
        results["Trades"] >= 3
    ]


    print(
        results
        .sort_values(
            [
                "Avg_Return",
                "Win_Rate"
            ],
            ascending=False
        )
        .head(20)
    )


if __name__ == "__main__":

    analyze_combinations()
