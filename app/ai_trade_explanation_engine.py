"""
AI Trade Explanation Engine v1.8

Purpose:
---------
Transforms AI scoring outputs into human-readable investment analyst explanations.

Input:
    data/analysis/final_ai_decision_controller.csv

Output:
    data/analysis/ai_trade_explanations.csv


Features:
    - Explains BUY/WATCH/REJECT decisions
    - Identifies strengths
    - Identifies weaknesses
    - Explains ML confidence
    - Explains risk
    - Generates analyst recommendation
"""


import os
import pandas as pd
from datetime import datetime



INPUT_FILE = (
    "data/analysis/final_ai_decision_controller.csv"
)


OUTPUT_FILE = (
    "data/analysis/ai_trade_explanations.csv"
)





# =====================================================
# HELPERS
# =====================================================


def value(row, column, default=0):

    if column not in row:

        return default


    result = row[column]


    if pd.isna(result):

        return default


    return result




# =====================================================
# STRENGTH ANALYSIS
# =====================================================


def analyze_strengths(row):


    strengths = []



    if value(row,"AI_Analyst_Score") >= 70:

        strengths.append(
            "Strong AI analyst confidence"
        )



    if value(row,"Final_Conviction_Score") >= 60:

        strengths.append(
            "High conviction ranking"
        )



    if value(row,"Risk_Grade") in ["A","B"]:

        strengths.append(
            "Acceptable risk profile"
        )



    if value(row,"Reward_Risk") >= 2:

        strengths.append(
            "Favorable reward/risk setup"
        )



    if value(row,"Historical_ML_Probability") >= 60:

        strengths.append(
            "Historical ML confirmation"
        )



    if value(row,"RVOL") >= 1.5:

        strengths.append(
            "Strong trading volume activity"
        )



    if not strengths:

        strengths.append(
            "No major advantages detected"
        )


    return strengths




# =====================================================
# WEAKNESS ANALYSIS
# =====================================================


def analyze_weaknesses(row):


    weaknesses = []



    if value(row,"Final_Conviction_Score") < 65:

        weaknesses.append(
            "Conviction below entry threshold"
        )



    if value(row,"AI_Analyst_Score") < 50:

        weaknesses.append(
            "Weak AI analyst confidence"
        )



    if value(row,"Risk_Grade") == "C":

        weaknesses.append(
            "Elevated portfolio risk"
        )



    if value(row,"Reward_Risk") < 2:

        weaknesses.append(
            "Limited reward/risk advantage"
        )



    if value(row,"Expected_Value") < 0:

        weaknesses.append(
            "Negative expected value"
        )



    if not weaknesses:

        weaknesses.append(
            "No major weaknesses detected"
        )


    return weaknesses





# =====================================================
# DECISION EXPLANATION
# =====================================================


def generate_explanation(row):


    decision = value(
        row,
        "AI_Final_Decision",
        "UNKNOWN"
    )



    score = value(
        row,
        "Final_Conviction_Score"
    )



    ai_score = value(
        row,
        "AI_Analyst_Score"
    )



    if decision == "BUY":


        explanation = (

            "AI approves this candidate. "
            "Multiple intelligence layers confirm "
            "acceptable risk and strong opportunity."

        )


    elif decision == "WATCH":


        explanation = (

            "Candidate shows potential but lacks "
            "enough confirmation for immediate entry. "
            "Monitor price action and wait for stronger signals."

        )


    else:


        explanation = (

            "Candidate does not currently meet "
            "AI entry requirements. "
            "Risk/reward or conviction is insufficient."

        )



    return explanation





# =====================================================
# ACTION
# =====================================================


def recommended_action(row):


    decision = value(
        row,
        "AI_Final_Decision"
    )


    actions = {


        "BUY":
        "Consider entry with predefined risk controls",


        "WATCH":
        "Monitor for confirmation before entry",


        "REJECT":
        "Avoid until conditions improve"

    }


    return actions.get(
        decision,
        "Review manually"
    )





# =====================================================
# MAIN ENGINE
# =====================================================


def analyze_trades(df):


    df = df.copy()



    df["AI_Strengths"] = df.apply(
        lambda x:
        analyze_strengths(x),
        axis=1
    )



    df["AI_Weaknesses"] = df.apply(
        lambda x:
        analyze_weaknesses(x),
        axis=1
    )



    df["AI_Explanation"] = df.apply(
        generate_explanation,
        axis=1
    )



    df["AI_Recommended_Action"] = df.apply(
        recommended_action,
        axis=1
    )



    df["Explanation_Date"] = (
        datetime.now()
    )



    return df





# =====================================================
# MAIN
# =====================================================


def main():


    print()

    print("==============================")

    print(
        "AI Trade Explanation Engine v1.8"
    )

    print("==============================")

    print()



    print(
        "Loading AI decisions..."
    )



    df = pd.read_csv(
        INPUT_FILE,
        low_memory=False
    )



    print(
        f"Loaded trades: {len(df)}"
    )



    df = analyze_trades(
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



    print()

    print(
        "===== AI EXPLANATION RESULTS ====="
    )


    print(

        df[
            [
                "Symbol",
                "AI_Final_Decision",
                "AI_Explanation",
                "AI_Recommended_Action"
            ]
        ]
        .to_string(index=False)

    )



    print()

    print(
        "Saved:",
        OUTPUT_FILE
    )


    print(
        "Completed:",
        datetime.now()
    )





if __name__ == "__main__":

    main()