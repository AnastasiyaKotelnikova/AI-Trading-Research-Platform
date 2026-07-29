"""
Portfolio Risk Manager v1.5 Step 5

Purpose:
---------
Applies portfolio-level risk controls after
AI portfolio selection.

Input:
    data/analysis/portfolio_decisions.csv

Output:
    data/analysis/final_portfolio_risk_decisions.csv


Features:
    - Position limits
    - Allocation control
    - Risk grading
    - Reward/Risk filtering
    - Sector exposure control
"""


import os
import pandas as pd
from datetime import datetime


INPUT_FILE = (
    "data/analysis/portfolio_decisions.csv"
)

OUTPUT_FILE = (
    "data/analysis/final_portfolio_risk_decisions.csv"
)


MAX_POSITIONS = 10
MAX_SECTOR_EXPOSURE = 40
MIN_REWARD_RISK = 2.0



def load_data():

    print("\nLoading portfolio decisions...")

    df = pd.read_csv(
        INPUT_FILE,
        low_memory=False
    )

    print(
        f"Loaded positions: {len(df)}"
    )

    return df



def calculate_risk_score(df):

    print(
        "\nCalculating risk scores..."
    )


    df["Risk_Score"] = 100


    df.loc[
        df["Risk_Level"] == "MODERATE",
        "Risk_Score"
    ] -= 15


    df.loc[
        df["Risk_Level"] == "HIGH",
        "Risk_Score"
    ] -= 35


    df.loc[
        df["Risk_Reward"] < MIN_REWARD_RISK,
        "Risk_Score"
    ] -= 25


    return df



def apply_position_limit(df):

    print(
        "\nApplying position limits..."
    )


    df = df.sort_values(
        "Portfolio_Rank"
    )


    df["Position_Approved"] = False


    df.loc[
        df.index[:MAX_POSITIONS],
        "Position_Approved"
    ] = True


    return df



def check_sector_exposure(df):

    print(
        "\nChecking sector concentration..."
    )


    sector_count = (
        df.groupby("Sector")
        ["Symbol"]
        .transform("count")
    )


    df["Sector_Position_Count"] = (
        sector_count
    )


    df["Sector_Risk"] = "OK"


    df.loc[
        sector_count > 4,
        "Sector_Risk"
    ] = "HIGH"


    return df



def final_decision(row):

    if not row["Position_Approved"]:

        return "REJECT"


    if row["Risk_Score"] < 50:

        return "REJECT"


    if row["Sector_Risk"] == "HIGH":

        return "REDUCE"


    if row["Portfolio_Action"] == "PORTFOLIO BUY":

        return "APPROVED"


    return "WATCH"



def main():

    print("\n==============================")
    print("Portfolio Risk Manager v1.5")
    print("==============================\n")


    df = load_data()


    df = calculate_risk_score(
        df
    )


    df = apply_position_limit(
        df
    )


    df = check_sector_exposure(
        df
    )


    df["Final_Portfolio_Decision"] = (
        df.apply(
            final_decision,
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
        "\n===== FINAL RISK RESULTS ====="
    )


    cols = [

        "Symbol",
        "Sector",
        "Portfolio_Score",
        "Risk_Score",
        "Sector_Risk",
        "Final_Portfolio_Decision"

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