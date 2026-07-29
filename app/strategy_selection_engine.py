"""
Strategy Selection Engine v1.5 Step 3

Purpose:
--------
Selects the best trading strategy for each stock candidate
using adaptive strategy intelligence.

Input:
------
data/results/adaptive_rankings.csv
data/models/adaptive_strategy_weights.json

Output:
-------
data/analysis/final_strategy_ai_decisions.csv

"""

import os
import json
import pandas as pd
from datetime import datetime


INPUT_FILE = (
    "data/results/adaptive_rankings.csv"
)

WEIGHTS_FILE = (
    "data/models/adaptive_strategy_weights.json"
)

OUTPUT_FILE = (
    "data/analysis/final_strategy_ai_decisions.csv"
)



def load_strategy_weights():

    print("\nLoading strategy intelligence...")

    with open(WEIGHTS_FILE, "r") as f:

        data = json.load(f)


    weights = {}

    for strategy, values in data["Strategies"].items():

        weights[strategy] = values.get(
            "New_Weight",
            values.get("Weight", 0)
        )


    print("\nStrategy weights:")

    for k, v in weights.items():

        print(
            f"{k}: {v}"
        )


    return weights



def calculate_strategy_score(row, weights):

    strategy = row["Strategy"]

    weight = weights.get(
        strategy,
        0
    )


    adaptive_score = row.get(
        "Adaptive_Final_Score",
        0
    )


    return (
        adaptive_score *
        weight
    )



def select_strategy(row):

    score = row["Strategy_AI_Score"]


    if score >= 60:

        return "PRIMARY STRATEGY"


    elif score >= 40:

        return "SECONDARY STRATEGY"


    elif score >= 20:

        return "MONITOR"


    else:

        return "REJECT"



def generate_reason(row):

    reasons = []


    if row["Adaptive_Strategy_Weight"] >= 0.6:

        reasons.append(
            "Strong historical strategy performance"
        )


    if row["Adaptive_Final_Score"] >= 70:

        reasons.append(
            "High adaptive ranking score"
        )


    if row["Strategy_AI_Score"] >= 50:

        reasons.append(
            "Strategy has strong AI preference"
        )


    if len(reasons) == 0:

        reasons.append(
            "Insufficient strategy confidence"
        )


    return " | ".join(reasons)



def main():

    print("\n==============================")
    print("Strategy Selection Engine v1.5")
    print("==============================\n")


    print(
        "Loading adaptive rankings..."
    )


    df = pd.read_csv(
        INPUT_FILE,
        low_memory=False
    )


    print(
        f"Loaded candidates: {len(df)}"
    )


    weights = load_strategy_weights()


    print(
        "\nCalculating strategy intelligence..."
    )


    df["Adaptive_Strategy_Weight"] = (

        df["Strategy"]
        .map(weights)
        .fillna(0)

    )


    df["Strategy_AI_Score"] = (

        df.apply(
            lambda row:
            calculate_strategy_score(
                row,
                weights
            ),
            axis=1
        )

    )


    df["Selected_Strategy_Action"] = (

        df.apply(
            select_strategy,
            axis=1
        )

    )


    df["Strategy_AI_Reason"] = (

        df.apply(
            generate_reason,
            axis=1
        )

    )


    df = df.sort_values(
        by="Strategy_AI_Score",
        ascending=False
    )


    df["Strategy_AI_Rank"] = range(
        1,
        len(df)+1
    )


    os.makedirs(
        "data/analysis",
        exist_ok=True
    )


    df.to_csv(
        OUTPUT_FILE,
        index=False
    )


    print(
        "\n===== STRATEGY AI DECISIONS ====="
    )


    columns = [

        "Symbol",
        "Strategy",
        "Adaptive_Final_Score",
        "Adaptive_Strategy_Weight",
        "Strategy_AI_Score",
        "Strategy_AI_Rank",
        "Selected_Strategy_Action"

    ]


    print(
        df[columns]
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