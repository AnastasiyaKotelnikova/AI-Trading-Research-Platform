import pandas as pd
import os


DATABASE_FILE = "data/trade_database.csv"

OUTPUT_FILE = "data/ml_training_dataset.csv"



def build_dataset():

    print("\n========== ML DATASET BUILDER ==========\n")


    if not os.path.exists(DATABASE_FILE):

        raise FileNotFoundError(
            f"Database not found: {DATABASE_FILE}"
        )



    df = pd.read_csv(
        DATABASE_FILE,
        low_memory=False
    )



    print("Original Records:")
    print(len(df))



    features = [

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

        "Research_Score"

    ]



    base_columns = [

        "Symbol",

        "Strategy",

        "Sector"

    ]



    required_columns = (
        base_columns
        +
        features
        +
        [
            "Return_%"
        ]
    )



    missing = [

        col for col in required_columns

        if col not in df.columns

    ]



    if missing:

        raise ValueError(
            f"Missing columns in database: {missing}"
        )



    dataset = df[
        required_columns
    ].copy()



    dataset["Successful_Trade"] = (

        dataset["Return_%"] > 0

    ).astype(int)



    dataset = dataset.dropna()



    os.makedirs(
        "data",
        exist_ok=True
    )



    dataset.to_csv(
        OUTPUT_FILE,
        index=False
    )



    print("\nDataset Created:")
    print(
        OUTPUT_FILE
    )



    print("\nDataset Size:")
    print(
        dataset.shape
    )



    print("\nColumns:")
    print(
        dataset.columns.tolist()
    )



    print("\nSuccess Distribution:")

    print(
        dataset[
            "Successful_Trade"
        ]
        .value_counts()
    )



    print("\nPreview:")

    print(
        dataset.head()
    )



if __name__ == "__main__":

    build_dataset()
