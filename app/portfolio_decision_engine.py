"""
Portfolio Decision Engine v1.5 Step 4

Purpose:
---------
Combines AI strategy decisions into a portfolio-level decision.

Input:
    data/analysis/final_strategy_ai_decisions.csv

Output:
    data/analysis/portfolio_decisions.csv


Features:
    - Portfolio scoring
    - Position ranking
    - Capital allocation
    - Risk filtering
    - Final portfolio action
"""


import os
import pandas as pd
from datetime import datetime


INPUT_FILE = (
    "data/analysis/final_strategy_ai_decisions.csv"
)

OUTPUT_FILE = (
    "data/analysis/portfolio_decisions.csv"
)


# Portfolio configuration

MAX_POSITIONS = 10

MAX_ALLOCATION = 15

MIN_PORTFOLIO_SCORE = 60



def load_data():

    print("\nLoading strategy AI decisions...")

    df = pd.read_csv(
        INPUT_FILE,
        low_memory=False
    )

    print(
        f"Loaded candidates: {len(df)}"
    )

    return df



def calculate_portfolio_score(df):

    print(
        "\nCalculating portfolio score..."
    )


    df["Portfolio_Score"] = (

        df["Adaptive_Final_Score"] * 0.40

        +

        df["Strategy_Adjusted_Score"] * 0.30

        +

        df["AI_Final_Score_Adjusted"] * 0.30

    )


    return df



def rank_candidates(df):

    print(
        "\nRanking candidates..."
    )


    df = df.sort_values(
        by="Portfolio_Score",
        ascending=False
    )


    df["Portfolio_Rank"] = range(
        1,
        len(df) + 1
    )


    return df



def assign_allocation(df):

    print(
        "\nAssigning portfolio allocation..."
    )


    allocations = []


    for rank in df["Portfolio_Rank"]:


        if rank <= MAX_POSITIONS:

            allocation = (
                MAX_ALLOCATION
                -
                (rank - 1)
            )

            if allocation < 5:
                allocation = 5

        else:

            allocation = 0


        allocations.append(
            allocation
        )


    df["Portfolio_Allocation_%"] = allocations


    return df



def calculate_portfolio_risk(row):

    risk = row.get(
        "Risk_Level",
        "UNKNOWN"
    )


    if risk == "LOW":

        return "LOW"


    elif risk == "MODERATE":

        return "MEDIUM"


    else:

        return "HIGH"



def create_action(row):

    score = row["Portfolio_Score"]

    allocation = row["Portfolio_Allocation_%"]


    if (
        score >= 75
        and allocation > 0
    ):

        return "ENTER"


    elif (
        score >= MIN_PORTFOLIO_SCORE
        and allocation > 0
    ):

        return "WATCH"


    else:

        return "REJECT"



# ==================================================
# REUSABLE PORTFOLIO PIPELINE FUNCTION
# ==================================================

def add_portfolio_decisions(df):

    """
    Applies portfolio intelligence layer.

    Input:
        dataframe containing AI strategy decisions

    Output:
        dataframe with portfolio decisions
    """

    df = df.copy()

    df = calculate_portfolio_score(
        df
    )


    df = rank_candidates(
        df
    )


    df = assign_allocation(
        df
    )


    df["Portfolio_Risk"] = (
        df.apply(
            calculate_portfolio_risk,
            axis=1
        )
    )


    df["Portfolio_Action"] = (
        df.apply(
            create_action,
            axis=1
        )
    )


    df["Portfolio_Status"] = (
        df["Portfolio_Action"]
        .map(
            {
                "ENTER": "APPROVED",
                "WATCH": "MONITOR",
                "REJECT": "REJECTED"
            }
        )
    )


    return df



def main():

    print(
        "\n=============================="
    )

    print(
        "Portfolio Decision Engine v1.5"
    )

    print(
        "==============================\n"
    )


    df = load_data()


    # Use reusable pipeline

    df = add_portfolio_decisions(
        df
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
        "\n===== PORTFOLIO DECISION RESULTS ====="
    )


    display_columns = [

        "Symbol",
        "Strategy",
        "Portfolio_Score",
        "Portfolio_Rank",
        "Portfolio_Allocation_%",
        "Portfolio_Action"

    ]


    print(
        df[display_columns]
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