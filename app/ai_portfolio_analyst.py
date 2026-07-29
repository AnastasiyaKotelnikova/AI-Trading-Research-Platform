"""
AI Portfolio Analyst v1.5 Step 7

Purpose:
---------
Creates an AI-style portfolio analysis report.

Input:
    data/analysis/final_portfolio_optimizer.csv

Outputs:
    data/analysis/ai_portfolio_analysis.csv
    data/reports/ai_portfolio_summary.txt

Features:
    - Portfolio scoring
    - Risk analysis
    - Candidate ranking
    - AI recommendation
    - Portfolio summary
"""


import os
import pandas as pd
from datetime import datetime



INPUT_FILE = (
    "data/analysis/final_portfolio_optimizer.csv"
)


OUTPUT_FILE = (
    "data/analysis/ai_portfolio_analysis.csv"
)


REPORT_FILE = (
    "data/reports/ai_portfolio_summary.txt"
)



def load_portfolio():

    print("\nLoading optimized portfolio...")

    df = pd.read_csv(
        INPUT_FILE,
        low_memory=False
    )

    print(
        f"Loaded positions: {len(df)}"
    )

    return df



def calculate_portfolio_score(df):

    print(
        "\nCalculating portfolio intelligence..."
    )


    df["AI_Portfolio_Score"] = (

        df["Portfolio_Score"] * 0.40

        +

        df["Risk_Score"] * 0.30

        +

        df["Final_Portfolio_Rank"].apply(
            lambda x:
            max(0,100-x*5)
        ) * 0.30

    )


    return df



def create_rating(score):

    if score >= 80:
        return "EXCELLENT"

    elif score >= 65:
        return "GOOD"

    elif score >= 50:
        return "MODERATE"

    else:
        return "WEAK"



def analyze_risk(df):

    print(
        "\nAnalyzing portfolio risk..."
    )


    avg_risk = (
        df["Risk_Score"]
        .mean()
    )


    if avg_risk >= 80:

        risk_status = "LOW RISK"

    elif avg_risk >= 60:

        risk_status = "MODERATE RISK"

    else:

        risk_status = "HIGH RISK"


    return risk_status



def create_ai_action(row):


    if row["Final_Action"] == "BUY":

        return (
            "AI APPROVED: "
            "Candidate qualifies for portfolio entry"
        )


    elif row["Final_Action"] == "WATCH":

        return (
            "AI MONITOR: "
            "Wait for stronger confirmation"
        )


    else:

        return (
            "AI REJECTED: "
            "Does not meet portfolio criteria"
        )



def generate_report(df, risk_status):


    os.makedirs(
        "data/reports",
        exist_ok=True
    )


    buys = df[
        df["Final_Action"] == "BUY"
    ]


    watches = df[
        df["Final_Action"] == "WATCH"
    ]


    avg_score = round(
        df["AI_Portfolio_Score"]
        .mean(),
        2
    )


    rating = create_rating(
        avg_score
    )


    text = f"""
AI PORTFOLIO ANALYST REPORT
===========================

Generated:
{datetime.now()}


Portfolio Rating:
{rating}


Portfolio Intelligence Score:
{avg_score}


Risk Assessment:
{risk_status}


Total Candidates:
{len(df)}


Approved Buys:
{len(buys)}


Watchlist:
{len(watches)}


Top Candidates:

"""


    top = df.sort_values(
        "AI_Portfolio_Score",
        ascending=False
    ).head(5)


    for _, row in top.iterrows():

        text += (
            f"""
{row['Symbol']}
Strategy:
{row['Strategy']}

Score:
{round(row['AI_Portfolio_Score'],2)}

Action:
{row['Final_Action']}

Reason:
{row['AI_Action']}

---------------------
"""
        )


    with open(
        REPORT_FILE,
        "w"
    ) as f:

        f.write(text)



    print(
        f"\nSaved report: {REPORT_FILE}"
    )



def main():

    print(
        "\n=============================="
    )

    print(
        "AI Portfolio Analyst v1.5"
    )

    print(
        "==============================\n"
    )


    df = load_portfolio()


    df = calculate_portfolio_score(
        df
    )


    df["AI_Portfolio_Rating"] = (
        df["AI_Portfolio_Score"]
        .apply(create_rating)
    )


    df["AI_Action"] = (
        df.apply(
            create_ai_action,
            axis=1
        )
    )


    risk_status = analyze_risk(
        df
    )


    df.to_csv(
        OUTPUT_FILE,
        index=False
    )


    generate_report(
        df,
        risk_status
    )


    print(
        "\n===== AI PORTFOLIO SUMMARY ====="
    )


    print(
        df[
            [
                "Symbol",
                "AI_Portfolio_Score",
                "AI_Portfolio_Rating",
                "Final_Action"
            ]
        ]
        .sort_values(
            "AI_Portfolio_Score",
            ascending=False
        )
        .head(10)
        .to_string(index=False)
    )


    print(
        "\nCompleted:",
        datetime.now()
    )



if __name__ == "__main__":
    main()