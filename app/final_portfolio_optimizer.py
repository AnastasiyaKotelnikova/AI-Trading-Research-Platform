"""
Final Portfolio Optimizer v1.5 Step 6

Purpose:
---------
Creates the final investable portfolio from risk-approved candidates.

Input:
    data/analysis/final_portfolio_risk_decisions.csv

Output:
    data/analysis/final_portfolio_optimizer.csv

Features:
    - Final candidate filtering
    - Capital allocation
    - Portfolio exposure calculation
    - Position sizing
    - Final portfolio ranking
"""


import os
import pandas as pd
from datetime import datetime


INPUT_FILE = (
    "data/analysis/final_portfolio_risk_decisions.csv"
)

OUTPUT_FILE = (
    "data/analysis/final_portfolio_optimizer.csv"
)


MAX_POSITIONS = 10

TOTAL_CAPITAL = 10000



def load_data():

    print("\nLoading risk decisions...")

    df = pd.read_csv(
        INPUT_FILE,
        low_memory=False
    )

    print(
        f"Loaded candidates: {len(df)}"
    )

    return df



def filter_candidates(df):

    print(
        "\nFiltering approved candidates..."
    )


    approved = df[
        df["Final_Portfolio_Decision"]
        .isin(
            [
                "APPROVED",
                "WATCH"
            ]
        )
    ].copy()


    print(
        f"Portfolio candidates: {len(approved)}"
    )


    return approved



def rank_portfolio(df):

    print(
        "\nRanking portfolio..."
    )


    df = df.sort_values(
        by=[
            "Portfolio_Score",
            "Risk_Score"
        ],
        ascending=False
    )


    df["Final_Portfolio_Rank"] = range(
        1,
        len(df)+1
    )


    return df



def assign_capital(df):

    print(
        "\nAssigning capital..."
    )


    df["Capital_Allocation_%"] = 0.0


    active_count = min(
        len(df),
        MAX_POSITIONS
    )


    allocation = (
        100 /
        active_count
    )


    df.loc[
        df["Final_Portfolio_Rank"] <= active_count,
        "Capital_Allocation_%"
    ] = allocation


    df["Capital_Allocated_$"] = (
        TOTAL_CAPITAL *
        df["Capital_Allocation_%"]
        /
        100
    )


    return df



def calculate_position_size(df):

    print(
        "\nCalculating position sizes..."
    )


    df["Estimated_Shares"] = (

        df["Capital_Allocated_$"]

        /

        df["Price"]

    ).astype(int)


    return df



def create_final_action(row):


    if row["Risk_Score"] < 50:

        return "REJECT"


    if row["Final_Portfolio_Rank"] <= MAX_POSITIONS:

        if row["Final_Portfolio_Decision"] == "APPROVED":

            return "BUY"


        else:

            return "WATCH"


    return "REJECT"



def create_portfolio_status(row):


    if row["Final_Action"] == "BUY":

        return "ACTIVE"


    elif row["Final_Action"] == "WATCH":

        return "MONITOR"


    else:

        return "REMOVED"



def main():

    print(
        "\n=============================="
    )

    print(
        "Final Portfolio Optimizer v1.5"
    )

    print(
        "==============================\n"
    )


    df = load_data()


    df = filter_candidates(
        df
    )


    df = rank_portfolio(
        df
    )


    df = assign_capital(
        df
    )


    df = calculate_position_size(
        df
    )


    df["Final_Action"] = (
        df.apply(
            create_final_action,
            axis=1
        )
    )


    df["Portfolio_Status"] = (
        df.apply(
            create_portfolio_status,
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
        "\n===== FINAL PORTFOLIO ====="
    )


    columns = [

        "Symbol",
        "Strategy",
        "Portfolio_Score",
        "Risk_Score",
        "Final_Portfolio_Rank",
        "Capital_Allocated_$",
        "Estimated_Shares",
        "Final_Action"

    ]


    print(
        df[columns]
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