import os
import pandas as pd
from app.signal_history import save_signal_history


def get_latest_history_file():

    return "data/analysis/confidence_scores.csv"



def analyze_signals():

    input_file = get_latest_history_file()

    df = pd.read_csv(input_file)


    print("\n===== SIGNAL SUMMARY =====\n")

    print(
        df["Signal"]
        .value_counts()
    )


    print("\n===== AVERAGE RANK BY SIGNAL =====\n")

    print(
        df.groupby("Signal")["Rank_Score"]
        .mean()
        .sort_values(
            ascending=False
        )
    )


    print("\n===== SECTOR SIGNALS =====\n")

    print(
        df.groupby("Sector")["Signal"]
        .count()
        .sort_values(
            ascending=False
        )
        .head(10)
    )


    print("\n===== TOP BUY CANDIDATES =====\n")

    print(
        df[
            df["Signal"] == "BUY"
        ]
        .sort_values(
            "Rank_Score",
            ascending=False
        )
        [
            [
                "Symbol",
                "Sector",
                "Rank_Score",
                "Return_20D",
                "Risk_Reward"
            ]
        ]
        .head(20)
    )


    # Save enriched signal history
    save_signal_history(df)



if __name__ == "__main__":

    analyze_signals()
