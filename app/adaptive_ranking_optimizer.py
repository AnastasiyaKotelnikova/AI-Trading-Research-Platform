"""
Adaptive Ranking Optimizer v1.7 Step 2

Purpose:
---------
Uses self-learning weights to optimize AI ranking.

Input:
    data/results/adaptive_rankings.csv
    data/models/self_optimization_weights.json

Output:
    data/results/optimized_adaptive_rankings.csv


Features:
    - Self learning strategy boost
    - Dynamic ranking adjustment
    - Optimization confidence
    - Final adaptive score
"""


import os
import json
import pandas as pd
from datetime import datetime



INPUT_FILE = (
    "data/results/adaptive_rankings.csv"
)


WEIGHTS_FILE = (
    "data/models/self_optimization_weights.json"
)


OUTPUT_FILE = (
    "data/results/optimized_adaptive_rankings.csv"
)



OPTIMIZATION_SCALE = 15



def load_weights():

    print(
        "\nLoading optimization weights..."
    )


    with open(
        WEIGHTS_FILE,
        "r"
    ) as f:

        data = json.load(f)


    weights = (
        data[
            "Strategy_Optimization_Weights"
        ]
    )


    print(
        "\nOptimization weights:"
    )


    for key,value in weights.items():

        print(
            key,
            "=>",
            value
        )


    return weights



def load_rankings():

    print(
        "\nLoading adaptive rankings..."
    )


    df = pd.read_csv(
        INPUT_FILE,
        low_memory=False
    )


    print(
        f"Stocks loaded: {len(df)}"
    )


    return df



def apply_optimization(
        df,
        weights
):

    print(
        "\nApplying optimization intelligence..."
    )


    df["Optimization_Weight"] = (

        df["Strategy"]
        .map(weights)
        .fillna(0.1)

    )


    df["Optimization_Boost"] = (

        df["Optimization_Weight"]

        *

        OPTIMIZATION_SCALE

    )


    df["Optimized_Final_Score"] = (

        df["Adaptive_Final_Score"]

        +

        df["Optimization_Boost"]

    )


    df["Optimization_Confidence"] = (

        df["Optimization_Weight"]
        *
        100

    )


    return df



def rank(df):

    print(
        "\nRanking optimized candidates..."
    )


    df = df.sort_values(
        by="Optimized_Final_Score",
        ascending=False
    )


    df["Optimized_Rank"] = range(
        1,
        len(df)+1
    )


    return df



def create_action(row):


    score = row[
        "Optimized_Final_Score"
    ]


    if score >= 90:

        return "HIGH CONVICTION"


    elif score >= 75:

        return "APPROVED"


    elif score >= 60:

        return "WATCH"


    else:

        return "PASS"



def main():

    print(
        "\n=============================="
    )

    print(
        "Adaptive Ranking Optimizer v1.7"
    )

    print(
        "==============================\n"
    )


    df = load_rankings()


    weights = load_weights()


    df = apply_optimization(
        df,
        weights
    )


    df = rank(
        df
    )


    df["Optimization_Action"] = (
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
        "\n===== OPTIMIZED RANKING RESULTS ====="
    )


    print(
        df[
            [
                "Symbol",
                "Strategy",
                "Adaptive_Final_Score",
                "Optimization_Boost",
                "Optimized_Final_Score",
                "Optimized_Rank",
                "Optimization_Action"
            ]
        ]
        .head(15)
        .to_string(index=False)
    )


    print(
        "\nSaved:",
        OUTPUT_FILE
    )


    print(
        "Completed:",
        datetime.now()
    )



if __name__ == "__main__":
    main()