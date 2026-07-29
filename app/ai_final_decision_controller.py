"""
AI Final Decision Controller v1.7 Step 3

Purpose:
---------
Final AI trade approval layer.

Input:
    data/results/optimized_adaptive_rankings.csv
    data/analysis/final_portfolio_risk_decisions.csv

Output:
    data/analysis/final_ai_decision_controller.csv


Features:
    - Multi-layer scoring
    - Risk filtering
    - Strategy intelligence integration
    - ML confidence integration
    - Final BUY/WATCH/REJECT decision
"""


import os
import pandas as pd
from datetime import datetime



RANK_FILE = (
    "data/results/optimized_adaptive_rankings.csv"
)


RISK_FILE = (
    "data/analysis/final_portfolio_risk_decisions.csv"
)


OUTPUT_FILE = (
    "data/analysis/final_ai_decision_controller.csv"
)



def load_data():

    print("\nLoading optimized rankings...")


    ranking = pd.read_csv(
        RANK_FILE,
        low_memory=False
    )


    print(
        f"Ranking candidates: {len(ranking)}"
    )


    print(
        "\nLoading risk decisions..."
    )


    risk = pd.read_csv(
        RISK_FILE,
        low_memory=False
    )


    print(
        f"Risk records: {len(risk)}"
    )


    return ranking, risk



def merge_data(ranking, risk):

    print(
        "\nCombining intelligence layers..."
    )


    # Remove duplicate columns
    duplicate_columns = [

        "Risk_Score",
        "Final_Portfolio_Decision",
        "Portfolio_Risk"

    ]


    for col in duplicate_columns:

        if col in ranking.columns:

            ranking = ranking.drop(
                columns=[col]
            )


    risk_columns = [

        "Symbol",
        "Risk_Score",
        "Final_Portfolio_Decision",
        "Portfolio_Risk"

    ]


    available_columns = [

        c for c in risk_columns

        if c in risk.columns

    ]


    df = ranking.merge(

        risk[available_columns],

        on="Symbol",

        how="left"

    )


    return df



def calculate_conviction(df):

    print(
        "\nCalculating final conviction..."
    )


    # Safety defaults

    if "Risk_Score" not in df.columns:

        df["Risk_Score"] = 75


    df["Risk_Score"] = pd.to_numeric(

        df["Risk_Score"],

        errors="coerce"

    ).fillna(75)



    if "Optimized_Final_Score" not in df.columns:

        df["Optimized_Final_Score"] = 0



    if "AI_Confidence" not in df.columns:

        df["AI_Confidence"] = 0



    if "Strategy_Weight" not in df.columns:

        df["Strategy_Weight"] = 0



    components = pd.DataFrame({

        "Risk_Component":
            df["Risk_Score"] * 0.25,


        "Ranking_Component":
            df["Optimized_Final_Score"] * 0.45,


        "ML_Component":
            df["AI_Confidence"] * 0.20,


        "Strategy_Component":
            df["Strategy_Weight"] * 10 * 0.10

    })


    df = pd.concat(

        [
            df.reset_index(drop=True),
            components
        ],

        axis=1

    )


    df["Final_Conviction_Score"] = (

        df["Risk_Component"]

        +

        df["Ranking_Component"]

        +

        df["ML_Component"]

        +

        df["Strategy_Component"]

    )


    return df



def create_decision(row):


    score = row[
        "Final_Conviction_Score"
    ]


    portfolio = row.get(
        "Final_Portfolio_Decision",
        "WATCH"
    )


    if portfolio == "REJECT":

        return "REJECT"


    if score >= 85:

        return "BUY"


    elif score >= 65:

        return "WATCH"


    else:

        return "REJECT"



def confidence_level(score):


    if score >= 85:

        return "HIGH"


    elif score >= 65:

        return "MEDIUM"


    else:

        return "LOW"



def create_reason(row):


    reasons = []


    if row["Optimized_Final_Score"] >= 70:

        reasons.append(
            "Strong optimized ranking"
        )


    if row["Risk_Score"] >= 80:

        reasons.append(
            "Strong risk profile"
        )


    if row["AI_Confidence"] >= 70:

        reasons.append(
            "Strong ML confidence"
        )


    if row["Strategy_Weight"] >= 0.6:

        reasons.append(
            "Strong historical strategy performance"
        )


    if len(reasons) == 0:

        reasons.append(
            "Insufficient supporting evidence"
        )


    return " | ".join(reasons)



def main():

    print(
        "\n=============================="
    )

    print(
        "AI Final Decision Controller v1.7"
    )

    print(
        "==============================\n"
    )


    ranking, risk = load_data()


    df = merge_data(
        ranking,
        risk
    )


    df = calculate_conviction(
        df
    )


    df["AI_Final_Decision"] = (

        df.apply(
            create_decision,
            axis=1
        )

    )


    df["AI_Confidence_Level"] = (

        df["Final_Conviction_Score"]
        .apply(
            confidence_level
        )

    )


    df["Decision_Reason"] = (

        df.apply(
            create_reason,
            axis=1
        )

    )


    df = df.sort_values(

        "Final_Conviction_Score",

        ascending=False

    )


    df["Decision_Rank"] = range(

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
        "\n===== FINAL AI DECISIONS ====="
    )


    print(

        df[

            [
                "Symbol",
                "Strategy",
                "Final_Conviction_Score",
                "AI_Final_Decision",
                "AI_Confidence_Level",
                "Decision_Rank"
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