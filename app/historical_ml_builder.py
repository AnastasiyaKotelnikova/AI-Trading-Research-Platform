"""
Historical ML Dataset Builder

Combines historical technical feature files
into one supervised ML training dataset.

Creates:

Successful_Trade = 1
when Future_Return_5D > 3%

Successful_Trade = 0
otherwise
"""

import os
import pandas as pd


FEATURE_DIR = "data/feature_history"
OUTPUT_FILE = "data/historical_ml_dataset.csv"


REQUIRED_COLUMNS = [
    "Adjusted_Close",
    "Close",
    "High",
    "Low",
    "Open",
    "Volume",

    "Return_5D",
    "Return_10D",
    "Return_20D",

    "RSI",
    "RSI_Change",

    "SMA20",
    "SMA50",

    "Above_SMA20",
    "Above_SMA50",

    "SMA_Gap",

    "Momentum_Acceleration",

    "Average_Volume",
    "RVOL",

    "Volume_Trend",

    "Volatility_20D",


# New professional features

    "ATR",
    "ATR_Percent",

    "Range_Position",

    "Distance_From_52W_High",

    "Future_Return_5D",
    "Future_Return_20D",

    "Future_Max_Return_5D",
    "Future_Max_Drawdown_5D"
]

def build_dataset():

    print("\n===== HISTORICAL ML DATASET BUILDER =====\n")


    datasets = []


    files = sorted(
        os.listdir(FEATURE_DIR)
    )


    feature_files = [
        f for f in files
        if f.endswith("_features.csv")
    ]


    print(
        "Feature files found:",
        len(feature_files)
    )


    for file in feature_files:


        symbol = file.replace(
            "_features.csv",
            ""
        )


        try:

            path = os.path.join(
                FEATURE_DIR,
                file
            )


            df = pd.read_csv(path)


            df["Symbol"] = symbol


            datasets.append(df)


        except Exception as e:

            print(
                symbol,
                "ERROR:",
                e
            )



    if not datasets:

        print(
            "No feature files found."
        )

        return



    dataset = pd.concat(
        datasets,
        ignore_index=True
    )

    # =========================
    # CREATE FUTURE RETURNS LABELS
    # =========================

    dataset = dataset.sort_values(
        [
            "Symbol",
            "Date"
        ]
    )


    dataset["Future_Return_5D"] = (

        dataset.groupby("Symbol")["Close"]
        .shift(-5)

        /

        dataset["Close"]

        - 1

    ) * 100



    dataset["Future_Return_20D"] = (

        dataset.groupby("Symbol")["Close"]
        .shift(-20)

        /

        dataset["Close"]

        - 1

    ) * 100


    # =========================
    # FUTURE 5 DAY TRADE QUALITY
    # =========================


    dataset["Future_Max_Close_5D"] = (

        dataset.groupby("Symbol")["Close"]
        .shift(-1)
        .rolling(5)
        .max()

    )


    dataset["Future_Max_Return_5D"] = (

        dataset["Future_Max_Close_5D"]
        /
        dataset["Close"]
        -
        1

    ) * 100



    dataset["Future_Min_Close_5D"] = (

        dataset.groupby("Symbol")["Close"]
        .shift(-1)
        .rolling(5)
        .min()

    )


    dataset["Future_Max_Drawdown_5D"] = (

        dataset["Future_Min_Close_5D"]
        /
        dataset["Close"]
        -
        1

    ) * 100


    print(
        "\nRows before cleaning:"
    )

    print(
        len(dataset)
    )



    # Remove rows missing required features

    dataset = dataset.dropna(
        subset=REQUIRED_COLUMNS
    )


    # Remove corrupted market data

    dataset = dataset[
        (dataset["Close"] < 10000)
        &
        (dataset["ATR_Percent"] < 50)
    ]


    # Remove stocks with too little history

    dataset = dataset.groupby(
        "Symbol"
    ).filter(
        lambda x: len(x) >= 30
    )



    print(
        "\nRows after cleaning:"
    )

    print(
        len(dataset)
    )


    print(
        "\nRemaining NaNs:"
    )

    print(
        dataset.isna()
        .sum()
        .sum()
    )



    # Create ML target

    dataset = dataset[
        dataset["Future_Return_5D"] < 100
    ]
    
    dataset["Successful_Trade"] = (

    (dataset["Future_Return_5D"] > 3)

    &

    (dataset["Future_Max_Drawdown_5D"] > -5)

    ).astype(int)



    print(
        "\nStocks remaining:"
    )

    print(
        dataset["Symbol"]
        .nunique()
    )



    # Save dataset

    dataset.to_csv(
        OUTPUT_FILE,
        index=False
    )



    print(
        "\nDataset saved:"
    )

    print(
        OUTPUT_FILE
    )



    print(
        "\nFinal Dataset Size:"
    )

    print(
        dataset.shape
    )



    print(
        "\nColumns:"
    )

    print(
        dataset.columns.tolist()
    )



    print(
        "\nSuccess Distribution:"
    )

    print(
        dataset["Successful_Trade"]
        .value_counts()
    )



if __name__ == "__main__":

    build_dataset()
