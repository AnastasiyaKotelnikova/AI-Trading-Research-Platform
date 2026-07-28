import os
import pandas as pd

from app.trade_management import add_trade_management
from app.final_conviction import add_final_conviction
from app.portfolio_manager import add_portfolio_management
from app.risk_engine import add_risk_management
from app.ai_score_engine import add_ai_analyst_score
from app.ai_investment_analyst import analyze_stocks

INPUT_FILE = "data/analysis/ai_ranked_signals.csv"

OUTPUT_FILE = "data/analysis/final_ai_signals.csv"



def generate_ai_decisions():

    print("\nGenerating AI Decisions\n")


    df = pd.read_csv(INPUT_FILE)



    # ==========================================
    # AI DECISION LOGIC
    # ==========================================

    decisions = []

    reasons = []


    for _, row in df.iterrows():


        score = row.get(
            "AI_Final_Score",
            0
        )


        ml_prob = row.get(
            "Combined_ML_Probability",
            row.get(
                "ML_Probability",
                0
            )
        )


        if pd.isna(ml_prob):

            ml_prob = 0


        if ml_prob <= 1:

            ml_prob = ml_prob * 100



        if (
            score >= 45
            and
            ml_prob >= 10
        ):

            decision = "HIGH CONVICTION"

            reason = (
                "Strong technical setup, "
                "high AI ranking, "
                "ML confirmation"
            )


        elif score >= 40:

            decision = "STRONG CANDIDATE"

            reason = (
                "Strong technical setup, "
                "high ranking"
            )


        elif score >= 30:

            decision = "WATCHLIST"

            reason = (
                "Positive setup but "
                "requires confirmation"
            )


        else:

            decision = "PASS"

            reason = (
                "Insufficient confirmation"
            )


        decisions.append(decision)

        reasons.append(reason)



    df["AI_Decision"] = decisions

    df["AI_Reason"] = reasons



    # ==========================================
    # MODEL INFORMATION
    # ==========================================

    df["Model_Name"] = "model_v27"

    df["Model_F1"] = 96.1

    df["Model_Status"] = "Champion"



    # ==========================================
    # COMPLETE TRADE PIPELINE
    # ==========================================


    df = add_trade_management(df)


    df = add_final_conviction(df)


    df = add_portfolio_management(df)


    df = add_risk_management(df)

    df = add_ai_analyst_score(df)


    # ==========================================
    # FINAL TRADE DECISION ENGINE
    # ==========================================

    final_decisions = []


    for _, row in df.iterrows():


        portfolio_action = row.get(
            "Portfolio_Action",
            ""
        )


        trade_status = row.get(
            "Trade_Status",
            ""
        )



        if (
            portfolio_action == "ALLOW ENTRY"
            and
            trade_status == "RISK APPROVED"
        ):

            decision = "APPROVED TRADE"



        elif (
            portfolio_action == "ALLOW ENTRY"
            and
            trade_status == "REVIEW RISK"
        ):

            decision = "REVIEW"



        elif portfolio_action == "MONITOR":

            decision = "WATCH"



        else:

            decision = "NO TRADE"



        final_decisions.append(
            decision
        )



    df["Final_Trade_Decision"] = final_decisions

    df = analyze_stocks(df)



    # ==========================================
    # FINAL SORTING
    # ==========================================

    if "Final_Conviction_Score" in df.columns:

        df = df.sort_values(
            "Final_Conviction_Score",
            ascending=False
        )



    # ==========================================
    # SAVE OUTPUT
    # ==========================================

    os.makedirs(
        "data/analysis",
        exist_ok=True
    )


    df.to_csv(
        OUTPUT_FILE,
        index=False
    )



    print(
        "AI Decision Engine Complete"
    )


    print(
        OUTPUT_FILE
    )



    print("\nDecision Summary:\n")


    print(
        df["AI_Decision"]
        .value_counts()
    )



    print("\nFINAL TRADE SUMMARY:\n")


    print(

        df[
            [
                "Symbol",
                "Final_Conviction_Score",
                "Portfolio_Action",
                "Portfolio_Approved",
                "Risk_Level",
                "Risk_Grade",
                "Trade_Status",
                "Final_Trade_Decision"
            ]
        ]
        .head(15)

    )



if __name__ == "__main__":

    generate_ai_decisions()