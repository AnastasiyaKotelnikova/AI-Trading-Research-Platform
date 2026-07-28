import pandas as pd
import os


SIGNAL_FILE = "data/signal_history/2026-07-17_11-32_signals.csv"

TRAINING_FILE = "data/ml_training_dataset.csv"



def update_training_data():


    print("\n===== UPDATE ML TRAINING DATA =====")


    if not os.path.exists(SIGNAL_FILE):

        print("Signal file not found")
        return


    df = pd.read_csv(
        SIGNAL_FILE
    )


    print("\nSignals Loaded:")
    print(len(df))


    # Keep only completed trades

    df = df[
        df["Result"].isin(
            [
                "TARGET 1 HIT",
                "TARGET 2 HIT",
                "STOP HIT"
            ]
        )
    ]


    print("\nCompleted Trades:")
    print(len(df))


    if len(df) == 0:

        print("No completed trades")
        return



    df["Successful_Trade"] = (
        df["Result"]
        .isin(
            [
                "TARGET 1 HIT",
                "TARGET 2 HIT"
            ]
        )
        .astype(int)
    )


    columns = [

        "Symbol",
        "Strategy",
        "Sector",
        "Rank_Score",
        "Momentum_Score",
        "Trend_Score",
        "Relative_Strength",
        "Risk_Reward",
        "RSI",
        "Return_5D",
        "Return_20D",
        "Distance_From_High_%",
        "Above_SMA20",
        "Above_SMA50",
        "Breakout",
        "Overextended",
        "Confidence_Score",
        "Research_Score",
        "Return_%",
        "Successful_Trade"

    ]


    new_data = df[columns]


    existing = pd.read_csv(
        TRAINING_FILE
    )


    before = len(existing)


    combined = pd.concat(
        [
            existing,
            new_data
        ],
        ignore_index=True
    )


    combined = combined.drop_duplicates(
        subset=[
            "Symbol",
            "Return_%"
        ],
        keep="last"
    )


    after = len(combined)


    combined.to_csv(
        TRAINING_FILE,
        index=False
    )


    print("\nTraining Dataset Updated")

    print(
        "Before:",
        before
    )

    print(
        "After:",
        after
    )

    print(
        "New Records:",
        after-before
    )



if __name__ == "__main__":

    update_training_data()
