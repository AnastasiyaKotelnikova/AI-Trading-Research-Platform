"""
AI Portfolio Rebalancer v1.6 Step 2

Purpose:
---------
Adaptive portfolio allocation using learned strategy performance.

Input:
    data/analysis/ai_portfolio_analysis.csv
    data/models/portfolio_learning_weights.json

Output:
    data/analysis/rebalanced_portfolio.csv

Features:
    - Strategy learning adjustment
    - Dynamic allocation
    - Portfolio rebalance decision
    - Adaptive confidence scoring
"""


import os
import json
import pandas as pd
from datetime import datetime



PORTFOLIO_FILE = (
    "data/analysis/ai_portfolio_analysis.csv"
)


WEIGHTS_FILE = (
    "data/models/portfolio_learning_weights.json"
)


OUTPUT_FILE = (
    "data/analysis/rebalanced_portfolio.csv"
)



MAX_POSITIONS = 10



def load_portfolio():

    print("\nLoading AI portfolio...")

    df = pd.read_csv(
        PORTFOLIO_FILE,
        low_memory=False
    )

    print(
        f"Positions loaded: {len(df)}"
    )

    return df



def load_weights():

    print(
        "\nLoading learning weights..."
    )

    with open(
        WEIGHTS_FILE,
        "r"
    ) as f:

        data = json.load(f)


    weights = data["Strategies"]


    print(
        "\nStrategy weights:"
    )

    for k,v in weights.items():

        print(
            k,
            "=>",
            v
        )


    return weights



def apply_learning_adjustment(
    df,
    weights
):

    print(
        "\nApplying strategy intelligence..."
    )


    df["Learning_Weight"] = (

        df["Strategy"]
        .map(weights)
        .fillna(0.2)

    )


    df["Learning_Adjustment"] = (

        df["Learning_Weight"]
        *
        10

    )


    df["Rebalanced_Score"] = (

        df["AI_Portfolio_Score"]

        +

        df["Learning_Adjustment"]

    )


    return df



def rank_portfolio(df):

    print(
        "\nRanking rebalanced portfolio..."
    )


    df = df.sort_values(
        "Rebalanced_Score",
        ascending=False
    )


    df["Rebalanced_Rank"] = range(
        1,
        len(df)+1
    )


    return df



def allocate_portfolio(df):

    print(
        "\nCalculating new allocation..."
    )


    df["Rebalanced_Allocation_%"] = 0


    active = min(
        MAX_POSITIONS,
        len(df)
    )


    allocation = round(
        100 / active,
        2
    )


    df.loc[
        df["Rebalanced_Rank"] <= active,
        "Rebalanced_Allocation_%"
    ] = allocation


    return df



def create_action(row):


    if row["Rebalanced_Rank"] <= MAX_POSITIONS:


        if row["Final_Action"] == "BUY":

            return "INCREASE"


        elif row["Final_Action"] == "WATCH":

            return "HOLD"


    return "REDUCE"



def main():

    print(
        "\n=============================="
    )

    print(
        "AI Portfolio Rebalancer v1.6"
    )

    print(
        "==============================\n"
    )


    df = load_portfolio()


    weights = load_weights()


    df = apply_learning_adjustment(
        df,
        weights
    )


    df = rank_portfolio(
        df
    )


    df = allocate_portfolio(
        df
    )


    df["Rebalance_Action"] = (
        df.apply(
            create_action,
            axis=1
        )
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
        "\n===== REBALANCED PORTFOLIO ====="
    )


    print(
        df[
            [
                "Symbol",
                "Strategy",
                "Rebalanced_Score",
                "Rebalanced_Rank",
                "Rebalanced_Allocation_%",
                "Rebalance_Action"
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