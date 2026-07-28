import pandas as pd
import os


DATABASE_FILE = "data/historical_trade_database.csv"

OUTPUT_FILE = "data/ml_training_dataset.csv"



def build_training_dataset():

    if not os.path.exists(DATABASE_FILE):

        raise FileNotFoundError(
            "Historical trade database missing."
        )


    df = pd.read_csv(
        DATABASE_FILE
    )


    print("\nHistorical records:")
    print(len(df))


    # -------------------------
    # Create ML target
    # -------------------------

    def create_label(result):

        if result in [
            "TARGET 1 HIT",
            "TARGET 2 HIT",
            "WIN"
        ]:
            return 1

        else:
            return 0



    df["Target"] = (
        df["Result"]
        .apply(create_label)
    )



    # -------------------------
    # Select ML features
    # -------------------------

    features = [

        "RSI",

        "Return_5D",
        "Return_20D",

        "Distance_From_High_%",

        "Above_SMA20",
        "Above_SMA50",

        "Breakout",
        "Overextended",

        "Rank_Score",

        "Momentum_Score",
        "Trend_Score",

        "Relative_Strength",

        "Risk_Reward"

    ]


    training = df[
        [
            c for c in features
            if c in df.columns
        ]
        +
        [
            "Target"
        ]
    ]


    # remove missing rows

    training = training.dropna()



    training.to_csv(
        OUTPUT_FILE,
        index=False
    )


    print("\nTraining dataset saved:")
    print(OUTPUT_FILE)


    print("\nShape:")
    print(training.shape)


    print("\nTarget distribution:")
    print(
        training["Target"]
        .value_counts()
    )



if __name__ == "__main__":

    build_training_dataset()
