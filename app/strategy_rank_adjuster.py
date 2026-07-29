"""
Strategy Rank Adjuster v1.4 Step 2

Purpose:
---------
Integrates historical strategy intelligence into AI ranking.

Reads:
    data/analysis/final_ai_signals.csv
    data/models/strategy_weights.json

Creates:
    data/results/strategy_adjusted_rankings.csv

Adds:
    Strategy_Weight
    Strategy_Adjustment
    Strategy_Adjusted_Score
    Strategy_Intelligence_Status

Author:
    AI Trading Research Platform
"""

import os
import json
import pandas as pd
from datetime import datetime


# ==============================
# Paths
# ==============================

INPUT_SIGNALS = "data/analysis/final_ai_signals.csv"
WEIGHTS_FILE = "data/models/strategy_weights.json"

OUTPUT_FILE = "data/results/strategy_adjusted_rankings.csv"


# ==============================
# Configuration
# ==============================

BASE_SCORE_COLUMN = "AI_Final_Score_Adjusted"

ADJUSTMENT_SCALE = 10
# Strategy weight of 0.638 becomes +6.38 points


# ==============================
# Load Strategy Intelligence
# ==============================

def load_strategy_weights():

    print("\nLoading strategy intelligence...")

    with open(WEIGHTS_FILE, "r") as f:
        data = json.load(f)

    strategies = data.get("Strategies", {})

    weights = {}

    for strategy, info in strategies.items():

        weights[strategy] = info.get("Weight", 0)

    print("Loaded strategies:")
    
    for k, v in weights.items():
        print(f"{k}: {v}")

    return weights


# ==============================
# Apply Strategy Adjustment
# ==============================

def apply_strategy_adjustment(df, weights):

    print("\nApplying strategy intelligence...")


    if "Strategy" not in df.columns:

        raise Exception(
            "Strategy column missing from final_ai_signals.csv"
        )


    if BASE_SCORE_COLUMN not in df.columns:

        raise Exception(
            f"{BASE_SCORE_COLUMN} missing from dataset"
        )


    df["Strategy_Weight"] = (
        df["Strategy"]
        .map(weights)
        .fillna(0)
    )


    df["Strategy_Adjustment"] = (
        df["Strategy_Weight"]
        * ADJUSTMENT_SCALE
    )


    df["Strategy_Adjusted_Score"] = (
        df[BASE_SCORE_COLUMN]
        +
        df["Strategy_Adjustment"]
    )


    df["Strategy_Intelligence_Status"] = (
        df["Strategy_Weight"]
        .apply(
            lambda x:
            "LEARNED"
            if x > 0
            else "UNKNOWN"
        )
    )


    return df


# ==============================
# Ranking
# ==============================

def rank_results(df):

    df = df.sort_values(
        by="Strategy_Adjusted_Score",
        ascending=False
    )

    df["Strategy_Rank"] = range(
        1,
        len(df) + 1
    )

    return df


# ==============================
# Main
# ==============================

def main():

    print("\n==============================")
    print("Strategy Rank Adjuster v1.4")
    print("==============================\n")


    print("Loading AI signals...")

    df = pd.read_csv(
        INPUT_SIGNALS,
        low_memory=False
    )


    print(
        f"Signals loaded: {len(df)}"
    )


    weights = load_strategy_weights()


    df = apply_strategy_adjustment(
        df,
        weights
    )


    df = rank_results(df)


    os.makedirs(
        os.path.dirname(OUTPUT_FILE),
        exist_ok=True
    )


    df.to_csv(
        OUTPUT_FILE,
        index=False
    )


    print("\n===== STRATEGY ADJUSTMENT RESULTS =====")

    cols = [
        "Symbol",
        "Strategy",
        BASE_SCORE_COLUMN,
        "Strategy_Weight",
        "Strategy_Adjustment",
        "Strategy_Adjusted_Score",
        "Strategy_Rank"
    ]


    print(
        df[cols]
        .head(10)
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