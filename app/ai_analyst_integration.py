"""
AI Analyst Integration Layer v1.7

Purpose:
---------
Connect final AI decisions with AI Investment Analyst.

Input:
    data/analysis/final_ai_decision_controller.csv

Output:
    data/analysis/final_ai_investment_report.csv


Uses:
    app.ai_investment_analyst

Features:
    - Generates trade explanation
    - Strength analysis
    - Risk analysis
    - AI analyst score
    - AI rating
    - Confidence level
    - Investor summary
"""


import os
import pandas as pd
from datetime import datetime

from app.ai_investment_analyst import analyze_stocks



INPUT_FILE = (
    "data/analysis/"
    "final_ai_decision_controller.csv"
)


OUTPUT_FILE = (
    "data/analysis/"
    "final_ai_investment_report.csv"
)



def main():

    print("\n==============================")
    print("AI Analyst Integration v1.7")
    print("==============================\n")


    print(
        "Loading final AI decisions..."
    )


    df = pd.read_csv(
        INPUT_FILE,
        low_memory=False
    )


    print(
        f"Candidates loaded: {len(df)}"
    )



    print(
        "\nRunning AI Investment Analyst..."
    )


    df = analyze_stocks(
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
        "\n===== AI INVESTMENT ANALYST RESULTS ====="
    )


    cols = [

        "Symbol",

        "Final_Trade_Decision",

        "AI_Analyst_Score",

        "AI_Analyst_Rating",

        "AI_Analyst_Confidence",

        "AI_Action"

    ]


    available = [
        c for c in cols
        if c in df.columns
    ]


    print(

        df[available]
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