"""
AI Dashboard Builder v1.8

Purpose:
---------
Creates final interactive-style HTML dashboard.

Inputs:
    data/analysis/final_ai_decision_controller.csv
    data/analysis/final_portfolio_risk_decisions.csv
    data/results/trade_quality_report.csv

Output:
    data/reports/AI_Trading_Dashboard.html


Features:
    - Portfolio overview
    - AI decision summary
    - Conviction ranking
    - Risk analysis
    - Strategy performance
    - ML confidence
"""



import os
import pandas as pd
from datetime import datetime



REPORT_FOLDER = "data/reports"



AI_FILE = (
    "data/analysis/final_ai_decision_controller.csv"
)


RISK_FILE = (
    "data/analysis/final_portfolio_risk_decisions.csv"
)


STRATEGY_FILE = (
    "data/results/trade_quality_report.csv"
)


OUTPUT_FILE = (
    "data/reports/AI_Trading_Dashboard.html"
)





# =====================================================
# LOAD DATA
# =====================================================


def load_data():

    print("\nLoading AI dashboard data...")


    ai = pd.read_csv(
        AI_FILE,
        low_memory=False
    )


    risk = pd.read_csv(
        RISK_FILE,
        low_memory=False
    )


    try:

        strategy = pd.read_csv(
            STRATEGY_FILE,
            low_memory=False
        )

    except:

        strategy = pd.DataFrame()



    print(
        f"AI records: {len(ai)}"
    )

    print(
        f"Risk records: {len(risk)}"
    )


    return ai, risk, strategy




# =====================================================
# SUMMARY
# =====================================================


def create_summary(df):


    return {


        "Total Candidates":
            len(df),


        "BUY":
            len(
                df[
                    df["AI_Final_Decision"]
                    ==
                    "BUY"
                ]
            ),


        "WATCH":
            len(
                df[
                    df["AI_Final_Decision"]
                    ==
                    "WATCH"
                ]
            ),


        "REJECT":
            len(
                df[
                    df["AI_Final_Decision"]
                    ==
                    "REJECT"
                ]
            ),


        "Average Conviction":
            round(
                df["Final_Conviction_Score"]
                .mean(),
                2
            ),


        "Average AI Score":
            round(
                df["AI_Analyst_Score"]
                .mean(),
                2
            )

    }




# =====================================================
# HTML BUILDER
# =====================================================


def build_html(
        ai,
        risk,
        strategy
):


    summary = create_summary(ai)



    ranked = ai.sort_values(
        "Final_Conviction_Score",
        ascending=False
    )



    html = f"""

<html>

<head>

<title>
AI Trading Research Dashboard
</title>


<style>


body {{

font-family: Arial;

background:#f4f4f4;

margin:30px;

}}


.card {{

background:white;

padding:20px;

margin-bottom:20px;

border-radius:10px;

}}


.grid {{

display:grid;

grid-template-columns:
repeat(3,1fr);

gap:20px;

}}


.box {{

background:white;

padding:20px;

text-align:center;

border-radius:10px;

font-size:20px;

}}


table {{

width:100%;

border-collapse:collapse;

background:white;

}}


th,td {{

padding:10px;

border:1px solid #ccc;

text-align:center;

}}


.BUY {{

background:#b7f7b7;

}}


.WATCH {{

background:#fff2a8;

}}


.REJECT {{

background:#ffb3b3;

}}



</style>


</head>


<body>


<h1>
AI Trading Research Dashboard
</h1>


<p>
Generated:
{datetime.now()}
</p>




<div class="grid">

"""



    for key,value in summary.items():

        html += f"""

<div class="box">

<b>{key}</b>

<br>

{value}

</div>

"""



    html += """

</div>


<br>



<div class="card">

<h2>
Top AI Ranked Candidates
</h2>



<table>

<tr>

<th>
Rank
</th>

<th>
Symbol
</th>

<th>
Strategy
</th>

<th>
Decision
</th>

<th>
Conviction
</th>

<th>
AI Score
</th>

<th>
Risk
</th>

</tr>


"""



    for _,row in ranked.iterrows():


        decision = row.get(
            "AI_Final_Decision",
            "N/A"
        )


        html += f"""

<tr class="{decision}">


<td>
{row.get('Decision_Rank')}
</td>


<td>
{row.get('Symbol')}
</td>


<td>
{row.get('Strategy')}
</td>


<td>
{decision}
</td>


<td>
{round(row.get('Final_Conviction_Score',0),2)}
</td>


<td>
{round(row.get('AI_Analyst_Score',0),2)}
</td>


<td>
{row.get('Risk_Grade')}
</td>


</tr>

"""



    html += """

</table>

</div>



<div class="card">


<h2>
Portfolio Risk Overview
</h2>


"""



    if len(risk) > 0:


        html += risk[
            [
                "Symbol",
                "Risk_Score",
                "Sector_Risk",
                "Final_Portfolio_Decision"
            ]
        ].to_html(
            index=False
        )


    else:


        html += "<p>No risk data available</p>"



    html += """

</div>



<div class="card">


<h2>
Strategy Performance
</h2>


"""



    if len(strategy) > 0:


        html += strategy.to_html(
            index=False
        )


    else:

        html += "<p>No strategy data available</p>"



    html += """

</div>



</body>

</html>

"""


    return html




# =====================================================
# MAIN
# =====================================================


def main():


    print()
    print("==============================")
    print("AI Dashboard Builder v1.8")
    print("==============================")
    print()



    ai,risk,strategy = load_data()



    html = build_html(
        ai,
        risk,
        strategy
    )


    os.makedirs(
        REPORT_FOLDER,
        exist_ok=True
    )



    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(html)



    print()

    print(
        "Dashboard created:"
    )

    print(
        OUTPUT_FILE
    )


    print(
        "Completed:",
        datetime.now()
    )




if __name__ == "__main__":

    main()