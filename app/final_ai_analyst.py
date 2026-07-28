import os
import pandas as pd


INPUT_FILE = "data/analysis/final_ai_signals.csv"

OUTPUT_FILE = "data/reports/ai_investment_report.txt"



def generate_ai_analyst_report():


    df = pd.read_csv(INPUT_FILE)


    os.makedirs(
        "data/reports",
        exist_ok=True
    )


    # =====================================
    # Sort by final decision quality
    # =====================================

    ranking_order = {

        "APPROVED TRADE": 1,
        "REVIEW": 2,
        "WATCH": 3,
        "NO TRADE": 4

    }


    df["Decision_Rank"] = (
        df["Final_Trade_Decision"]
        .map(ranking_order)
        .fillna(5)
    )


    df = df.sort_values(
        [
            "Decision_Rank",
            "Final_Conviction_Score"
        ],
        ascending=[
            True,
            False
        ]
    )



    best = df.iloc[0]



    # =====================================
    # Create Report
    # =====================================

    report = []


    report.append(
        "=" * 70
    )

    report.append(
        "AI INVESTMENT ANALYST REPORT"
    )

    report.append(
        "=" * 70
    )



    report.append(
        f"""
TOP OPPORTUNITY

Symbol:
{best['Symbol']}

Final Decision:
{best['Final_Trade_Decision']}

Conviction Score:
{best['Final_Conviction_Score']}

Risk Level:
{best['Risk_Level']}

Risk Grade:
{best['Risk_Grade']}

Expected Value:
{round(best['Expected_Value'],3)}

Reward/Risk:
{round(best['Reward_Risk'],2)}

Reason:
{best['AI_Reason']}
"""
    )



    report.append(
        "\n"
        + "=" * 70
    )

    report.append(
        "TOP AI RANKINGS"
    )

    report.append(
        "=" * 70
    )



    for _, row in df.head(10).iterrows():


        report.append(

f"""
{row['Symbol']}

Decision:
{row['Final_Trade_Decision']}

Conviction:
{row['Final_Conviction_Score']}

Risk:
{row['Risk_Level']} ({row['Risk_Grade']})

Expected Value:
{round(row['Expected_Value'],3)}

-------------------------
"""
        )



    report.append(
        "\n"
        + "=" * 70
    )


    report.append(
        "PORTFOLIO SUMMARY"
    )


    report.append(
        "=" * 70
    )


    report.append(

f"""
Approved Trades:
{
len(
    df[
        df["Final_Trade_Decision"]
        ==
        "APPROVED TRADE"
    ]
)
}


Watchlist:
{
len(
    df[
        df["Final_Trade_Decision"]
        ==
        "WATCH"
    ]
)
}


No Trade:
{
len(
    df[
        df["Final_Trade_Decision"]
        ==
        "NO TRADE"
    ]
)
}
"""
    )



    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(
            "\n".join(report)
        )



    print(
        "AI Analyst Report Generated"
    )


    print(
        OUTPUT_FILE
    )



if __name__ == "__main__":

    generate_ai_analyst_report()