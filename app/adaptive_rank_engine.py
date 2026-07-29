"""
Adaptive Rank Engine v1.5 Step 2

Purpose:
---------
Uses learned strategy weights to adjust AI ranking.

Input:
    data/results/strategy_adjusted_rankings.csv
    data/models/adaptive_strategy_weights.json

Output:
    data/results/adaptive_rankings.csv

"""

import os
import json
import pandas as pd
from datetime import datetime


INPUT_FILE = (
    "data/results/strategy_adjusted_rankings.csv"
)

WEIGHTS_FILE = (
    "data/models/adaptive_strategy_weights.json"
)

OUTPUT_FILE = (
    "data/results/adaptive_rankings.csv"
)


ADAPTIVE_SCALE = 10



def load_weights():

    print("\nLoading adaptive strategy weights...")

    with open(WEIGHTS_FILE, "r") as f:

        data = json.load(f)


    weights = {}

    for strategy, values in data["Strategies"].items():

        weights[strategy] = values["New_Weight"]


    print("\nLearned weights:")

    for k, v in weights.items():

        print(
            f"{k}: {v}"
        )


    return weights



def apply_adaptive_score(df, weights):

    print(
        "\nApplying adaptive intelligence..."
    )


    df["Adaptive_Strategy_Weight"] = (
        df["Strategy"]
        .map(weights)
        .fillna(0)
    )


    df["Adaptive_Strategy_Boost"] = (
        df["Adaptive_Strategy_Weight"]
        *
        ADAPTIVE_SCALE
    )


    df["Adaptive_Final_Score"] = (

        df["Strategy_Adjusted_Score"]

        +

        df["Adaptive_Strategy_Boost"]

    )


    return df



def create_rank(df):

    df = df.sort_values(
        by="Adaptive_Final_Score",
        ascending=False
    )


    df["Adaptive_Rank"] = range(
        1,
        len(df)+1
    )


    return df



def create_action(row):

    score = row["Adaptive_Final_Score"]


    if score >= 85:

        return "HIGH CONVICTION"


    elif score >= 75:

        return "APPROVED"


    elif score >= 65:

        return "WATCH"


    else:

        return "PASS"



def main():

    print("\n==============================")
    print("Adaptive Rank Engine v1.5")
    print("==============================\n")


    print(
        "Loading rankings..."
    )


    df = pd.read_csv(
        INPUT_FILE,
        low_memory=False
    )


    print(
        f"Loaded rows: {len(df)}"
    )


    weights = load_weights()


    df = apply_adaptive_score(
        df,
        weights
    )


    df = create_rank(
        df
    )


    df["Adaptive_Action"] = (
        df.apply(
            create_action,
            axis=1
        )
    )


    os.makedirs(
        "data/results",
        exist_ok=True
    )


    df.to_csv(
        OUTPUT_FILE,
        index=False
    )


    print(
        "\n===== ADAPTIVE RANK RESULTS ====="
    )


    cols = [

        "Symbol",
        "Strategy",
        "Strategy_Adjusted_Score",
        "Adaptive_Strategy_Boost",
        "Adaptive_Final_Score",
        "Adaptive_Rank",
        "Adaptive_Action"

    ]


    print(

        df[cols]
        .head(15)
        .to_string(index=False)

    )


    print(
        f"\nSaved: {OUTPUT_FILE}"
    )


    print(
        "Completed:",
        datetime.now()
    )



if __name__ == "__main__":
    main()