import os
import pandas as pd


from app.final_conviction import add_final_conviction
from app.portfolio_manager import add_portfolio_management
from app.trade_management import add_trade_management
from app.risk_engine import add_risk_management
from app.ai_score_engine import add_ai_analyst_score
from app.ai_investment_analyst import analyze_stocks
from app.execution_engine import add_execution_analysis



INPUT_FILE = "data/analysis/ai_ranked_signals.csv"

OUTPUT_FILE = "data/analysis/final_ai_signals.csv"



# =====================================================
# Initial AI Classification
# =====================================================

def add_ai_decisions(df):

    print("\nGenerating AI Decisions\n")

    df = df.copy()

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
            ml_prob *= 100



        if score >= 45 and ml_prob >= 10:

            decision = "HIGH CONVICTION"

            reason = (
                "Strong technical setup, "
                "AI score confirmation, "
                "ML probability support"
            )


        elif score >= 40:

            decision = "STRONG CANDIDATE"

            reason = (
                "Good technical setup "
                "with positive ranking"
            )


        elif score >= 30:

            decision = "WATCHLIST"

            reason = (
                "Promising setup but "
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



    from app.model_info import get_current_model_info


    model_info = get_current_model_info()


    df["Model_Name"] = model_info["Model"]

    df["Model_F1"] = model_info["F1"]

    df["Model_Status"] = "Champion"


    return df




# =====================================================
# Final AI Status Controller
# =====================================================

def add_final_ai_status(df):

    final_status = []
    final_reasons = []


    for _, row in df.iterrows():

        portfolio_action = row.get(
            "Portfolio_Action",
            ""
        )


        risk_status = row.get(
            "Risk_Status",
            ""
        )


        if (
            portfolio_action == "ALLOW ENTRY"
            and
            risk_status == "RISK APPROVED"
        ):

            status = "APPROVED TRADE"

            reason = (
                "High conviction setup, "
                "positive expected value, "
                "risk approved"
            )


        elif (
            portfolio_action == "WATCH ENTRY"
            and
            risk_status == "WATCH RISK"
        ):

            status = "WATCHLIST"

            reason = (
                "Promising setup but "
                "requires additional confirmation"
            )


        elif portfolio_action == "MONITOR":

            status = "MONITOR"

            reason = (
                "Valid setup but "
                "conviction or risk profile "
                "needs improvement"
            )


        else:

            status = "NO TRADE"

            reason = (
                "Rejected due to risk, "
                "low conviction, "
                "or poor expected value"
            )


        final_status.append(status)

        final_reasons.append(reason)


    df["Final_AI_Status"] = final_status

    df["Final_AI_Reason"] = final_reasons


    return df

# =====================================================
# Complete Pipeline
# =====================================================

def add_complete_ai_pipeline(df):


    # 1
    df = add_ai_decisions(df)


    # 2
    df = add_ai_analyst_score(df)


    # 3
    df = add_final_conviction(df)


    # 4
    df = add_portfolio_management(df)


    # 5
    df = add_trade_management(df)


    # 6
    df = add_risk_management(df)

    print(
    df[
        [
            "Symbol",
            "Portfolio_Action",
            "Risk_Status"
        ]
    ]
)

    # 7 Create final AI decision BEFORE execution
    df = add_final_ai_status(df)


    # 8 Execution engine
    df = add_execution_analysis(df)


    # 9 Analyst explanation
    df = analyze_stocks(df)



    if "Final_Conviction_Score" in df.columns:

        df = df.sort_values(
            "Final_Conviction_Score",
            ascending=False
        )



    return df




# =====================================================
# Generator
# =====================================================

def generate_ai_decisions(df=None):


    if df is None:

        df = pd.read_csv(
            INPUT_FILE
        )



    required_columns = [

        "Symbol",

        "AI_Final_Score"

    ]



    missing = [

        c for c in required_columns

        if c not in df.columns

    ]



    if missing:

        raise ValueError(
            f"Missing required columns: {missing}"
        )



    df = add_complete_ai_pipeline(df)



    os.makedirs(
        "data/analysis",
        exist_ok=True
    )



    df.to_csv(
        OUTPUT_FILE,
        index=False
    )



    print(
        "\nAI Decision Engine Complete"
    )


    print(
        OUTPUT_FILE
    )



    print(
        "\nAI Classification:\n"
    )


    print(
        df["AI_Decision"]
        .value_counts()
    )



    print(
        "\nFinal AI Status:\n"
    )


    print(
        df["Final_AI_Status"]
        .value_counts()
    )



    print(
        "\nTrade Summary:\n"
    )



    summary_columns = [

        "Symbol",

        "AI_Decision",

        "Final_Conviction_Score",

        "Expected_Value",

        "Portfolio_Action",

        "Trade_Status",

        "Final_AI_Status",

        "Execution_Score",

        "Execution_Grade",

        "Execution_Action",

        "Final_AI_Reason"

    ]



    existing_columns = [

        c for c in summary_columns

        if c in df.columns

    ]



    print(

        df[existing_columns]

        .head(15)

        .to_string(index=False)

    )


    return df





if __name__ == "__main__":

    generate_ai_decisions()