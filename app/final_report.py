import pandas as pd
import os
import ast

from datetime import datetime

from app.model_info import get_current_model_info



DATABASE = (
    "data/analysis/final_ai_signals.csv"
)


MONITOR_FILE = (
    "data/models/model_monitoring.csv"
)


METRICS_FILE = (
    "data/models/model_metrics.csv"
)



# =====================================================
# CLEAN CSV LIST FIELDS
# =====================================================

def clean_list(value):

    if isinstance(value, list):
        return value


    if pd.isna(value):
        return []


    try:

        return ast.literal_eval(
            value
        )


    except:

        return [
            str(value)
        ]



# =====================================================
# MODEL STATUS
# =====================================================

def model_status():

    print("\n================================")
    print("AI MODEL STATUS")
    print("================================")


    info = get_current_model_info()


    print(
        "Model:",
        info.get(
            "Model",
            "N/A"
        )
    )


    print(
        "Accuracy:",
        info.get(
            "Accuracy",
            "N/A"
        ),
        "%"
    )


    print(
        "F1 Score:",
        info.get(
            "F1",
            "N/A"
        ),
        "%"
    )


    print(
        "Trained:",
        info.get(
            "Date",
            "N/A"
        )
    )


    print("================================")




# =====================================================
# LATEST MONITORING
# =====================================================

def latest_monitoring():

    print("\n================================")
    print("LATEST MODEL RUN")
    print("================================")


    if not os.path.exists(
        MONITOR_FILE
    ):

        print(
            "No monitoring data available"
        )

        return



    df = pd.read_csv(
        MONITOR_FILE
    )


    if df.empty:

        print(
            "Monitoring file empty"
        )

        return



    latest = df.iloc[-1]


    print(
        "Date:",
        latest.get(
            "Date",
            "N/A"
        )
    )


    print(
        "Market:",
        latest.get(
            "Market_Regime",
            "N/A"
        )
    )


    print(
        "Stocks Scanned:",
        latest.get(
            "Stocks_Scanned",
            "N/A"
        )
    )


    print(
        "Average ML Probability:",
        latest.get(
            "Average_ML_Probability",
            "N/A"
        )
    )


    print(
        "Top Ranked Stock:",
        latest.get(
            "Top_Ranked_Stock",
            "N/A"
        )
    )


    print("================================")





# =====================================================
# MODEL HISTORY
# =====================================================

def model_history():

    print("\n================================")
    print("MODEL HISTORY")
    print("================================")


    if not os.path.exists(
        METRICS_FILE
    ):

        print(
            "No model history found"
        )

        return



    df = pd.read_csv(
        METRICS_FILE
    )


    columns = [
        "Model",
        "Accuracy",
        "F1",
        "Status"
    ]


    available = [
        c for c in columns
        if c in df.columns
    ]


    print(
        df[available]
        .tail(10)
    )





# =====================================================
# REPORT HEADER
# =====================================================

def market_summary(df):

    print("\n================================================")
    print("AI INVESTMENT ANALYST REPORT")
    print("================================================")


    print(
        "Generated:",
        datetime.now()
    )


    print(
        "\nTotal Candidates:",
        len(df)
    )





# =====================================================
# TOP OPPORTUNITY
# =====================================================

def top_opportunity(df):


    print("\n================================================")
    print("TOP OPPORTUNITY")
    print("================================================")


    top = (
        df.sort_values(
            "AI_Analyst_Score",
            ascending=False
        )
        .iloc[0]
    )



    print(
        "\nSymbol:",
        top.get(
            "Symbol",
            "N/A"
        )
    )


    print(
        "Final Decision:",
        top.get(
            "Final_Trade_Decision",
            "N/A"
        )
    )


    print(
        "AI Analyst Score:",
        top.get(
            "AI_Analyst_Score",
            0
        )
    )


    print(
        "Rating:",
        top.get(
            "AI_Analyst_Rating",
            "N/A"
        )
    )


    print(
        "Confidence:",
        top.get(
            "AI_Analyst_Confidence",
            "N/A"
        )
    )


    print(
        "Risk:",
        top.get(
            "Risk_Grade",
            "N/A"
        )
    )


    print(
        "Action:",
        top.get(
            "AI_Action",
            "N/A"
        )
    )



    print(
        "\nTrade Reason:"
    )


    print(
        top.get(
            "Trade_Reason",
            "N/A"
        )
    )



    print(
        "\nStrengths:"
    )


    strengths = clean_list(
        top.get(
            "Strengths",
            []
        )
    )


    for item in strengths:

        print(
            "-",
            item
        )



    print(
        "\nRisks:"
    )


    risks = clean_list(
        top.get(
            "Risks",
            []
        )
    )


    for item in risks:

        print(
            "-",
            item
        )






# =====================================================
# AI RANKINGS
# =====================================================

def ai_rankings(df):


    print("\n================================================")
    print("TOP AI ANALYST RANKINGS")
    print("================================================")


    ranked = (

        df.sort_values(
            "AI_Analyst_Score",
            ascending=False
        )

        .head(10)

    )



    print(

        ranked[
            [
                "Symbol",
                "Final_Trade_Decision",
                "AI_Analyst_Score",
                "AI_Analyst_Rating",
                "AI_Analyst_Confidence",
                "Risk_Grade"
            ]
        ]

    )






# =====================================================
# PORTFOLIO SUMMARY
# =====================================================

def portfolio_summary(df):


    print("\n================================================")
    print("PORTFOLIO SUMMARY")
    print("================================================")


    print(
        "Approved Trades:",
        len(
            df[
                df["Final_Trade_Decision"]
                ==
                "APPROVED TRADE"
            ]
        )
    )


    print(
        "Watchlist:",
        len(
            df[
                df["Final_Trade_Decision"]
                ==
                "WATCH"
            ]
        )
    )


    print(
        "No Trade:",
        len(
            df[
                df["Final_Trade_Decision"]
                ==
                "NO TRADE"
            ]
        )
    )


    print(
        "Average AI Analyst Score:",
        round(
            df["AI_Analyst_Score"]
            .mean(),
            2
        )
    )






# =====================================================
# SAVE
# =====================================================

def save(df):


    os.makedirs(
        "data/reports",
        exist_ok=True
    )


    filename = (
        "data/reports/final_ai_report.csv"
    )


    df.to_csv(
        filename,
        index=False
    )


    print(
        "\nSaved:"
    )

    print(
        filename
    )






# =====================================================
# MAIN
# =====================================================

def main():

    df = pd.read_csv(
        DATABASE
    )


    market_summary(df)

    model_status()

    latest_monitoring()

    model_history()

    top_opportunity(df)

    ai_rankings(df)

    portfolio_summary(df)

    save(df)





if __name__ == "__main__":

    main()