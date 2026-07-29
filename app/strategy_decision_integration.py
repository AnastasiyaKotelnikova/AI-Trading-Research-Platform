"""
Strategy Decision Integration v1.4 Step 3

Purpose:
---------
Integrates learned strategy performance into final AI trade decisions.

Input:
    data/results/strategy_adjusted_rankings.csv

Output:
    data/analysis/final_strategy_ai_decisions.csv


Learning sources:
    - Strategy performance
    - Strategy adjusted score
    - ML probability
    - AI confidence
    - Risk reward

"""

import os
import pandas as pd
from datetime import datetime


INPUT_FILE = "data/results/strategy_adjusted_rankings.csv"

OUTPUT_FILE = (
    "data/analysis/final_strategy_ai_decisions.csv"
)


def calculate_strategy_decision(row):

    score = row["Strategy_Adjusted_Score"]

    confidence = row.get(
        "AI_Confidence",
        0
    )

    risk_reward = row.get(
        "Risk_Reward",
        0
    )

    strategy_status = row.get(
        "Strategy_Intelligence_Status",
        "UNKNOWN"
    )


    # High conviction
    if (
        score >= 80
        and confidence >= 60
        and risk_reward >= 2
    ):

        return "HIGH CONVICTION"


    # Approved trade
    elif (
        score >= 70
        and risk_reward >= 2
    ):

        return "APPROVED WATCH"


    # Monitor
    elif score >= 60:

        return "MONITOR"


    else:

        return "PASS"



def calculate_confidence(row):

    score = row["Strategy_Adjusted_Score"]


    if score >= 80:
        return "HIGH"

    elif score >= 70:
        return "MEDIUM"

    elif score >= 60:
        return "LOW"

    else:
        return "VERY LOW"



def create_reason(row):

    reasons = []


    if row["Strategy_Intelligence_Status"] == "LEARNED":
        reasons.append(
            "Strategy has historical performance data"
        )


    if row["Strategy_Adjustment"] > 0:
        reasons.append(
            "Historical strategy boost applied"
        )


    if row["ML_Probability"] >= 50:
        reasons.append(
            "ML confirmation positive"
        )


    if row["Risk_Reward"] >= 2:
        reasons.append(
            "Positive risk reward"
        )


    if not reasons:
        reasons.append(
            "Insufficient historical confirmation"
        )


    return " | ".join(reasons)



def main():

    print("\n==============================")
    print("Strategy Decision Integration v1.4")
    print("==============================\n")


    print("Loading strategy rankings...")


    df = pd.read_csv(
        INPUT_FILE,
        low_memory=False
    )


    print(
        f"Loaded trades: {len(df)}"
    )


    print(
        "Applying learned strategy decisions..."
    )


    df["Strategy_Decision"] = (
        df.apply(
            calculate_strategy_decision,
            axis=1
        )
    )


    df["Strategy_Confidence"] = (
        df.apply(
            calculate_confidence,
            axis=1
        )
    )


    df["Strategy_Decision_Reason"] = (
        df.apply(
            create_reason,
            axis=1
        )
    )


    # Final AI action

    def final_action(row):

        if row["Strategy_Decision"] == "HIGH CONVICTION":
            return "BUY"

        elif row["Strategy_Decision"] == "APPROVED WATCH":
            return "WATCH"

        elif row["Strategy_Decision"] == "MONITOR":
            return "MONITOR"

        else:
            return "AVOID"


    df["Strategy_Final_Action"] = (
        df.apply(
            final_action,
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


    print("\n===== STRATEGY AI RESULTS =====")


    display_cols = [
        "Symbol",
        "Strategy",
        "Strategy_Adjusted_Score",
        "Strategy_Decision",
        "Strategy_Confidence",
        "Strategy_Final_Action"
    ]


    print(
        df[display_cols]
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