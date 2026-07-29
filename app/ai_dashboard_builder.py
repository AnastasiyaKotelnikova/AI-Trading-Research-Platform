"""
AI Dashboard Builder v1.9

Purpose:
---------
Creates final AI investment research dashboard.

Inputs:
    data/analysis/final_ai_decision_controller.csv
    data/analysis/final_portfolio_risk_decisions.csv
    data/analysis/ai_trade_explanations.csv
    data/results/trade_quality_report.csv

Output:
    data/reports/AI_Trading_Dashboard.html


Features:
    - Portfolio summary
    - AI ranking table
    - Risk analysis
    - Strategy performance
    - AI explanations
    - Strengths
    - Weaknesses
    - Recommended actions
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


EXPLANATION_FILE = (
    "data/analysis/ai_trade_explanations.csv"
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


    print("\nLoading dashboard intelligence...")


    ai = pd.read_csv(
        AI_FILE,
        low_memory=False
    )


    risk = pd.read_csv(
        RISK_FILE,
        low_memory=False
    )


    explanation = pd.read_csv(
        EXPLANATION_FILE,
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


    print(
        f"Explanation records: {len(explanation)}"
    )


    return ai, risk, explanation, strategy





# =====================================================
# MERGE
# =====================================================


def merge_data(
        ai,
        explanation
):


    columns = [

        "Symbol",
        "AI_Strengths",
        "AI_Weaknesses",
        "AI_Explanation",
        "AI_Recommended_Action"

    ]


    explanation = explanation[
        columns
    ]


    df = ai.merge(

        explanation,

        on="Symbol",

        how="left"

    )


    return df





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


        "Average AI Analyst Score":
            round(
                df["AI_Analyst_Score"]
                .mean(),
                2
            )

    }




# =====================================================
# DASHBOARD HTML
# =====================================================


def build_dashboard(
        df,
        risk,
        strategy
):


    summary = create_summary(df)



    ranked = df.sort_values(
        "Final_Conviction_Score",
        ascending=False
    )



    html = f"""

<html>

<head>


<title>
AI Trading Research Dashboard v1.9
</title>


<style>


body {{

font-family: Arial;

margin:30px;

background:#f5f5f5;

}}


.card {{

background:white;

padding:20px;

margin-bottom:25px;

border-radius:12px;

}}


.grid {{

display:grid;

grid-template-columns:
repeat(3,1fr);

gap:15px;

}}


.metric {{

background:white;

padding:20px;

border-radius:10px;

text-align:center;

font-size:20px;

}}


table {{

width:100%;

border-collapse:collapse;

background:white;

}}


td,th {{

border:1px solid #ccc;

padding:8px;

text-align:center;

}}


.BUY {{

background:#b7f7b7;

}}


.WATCH {{

background:#fff1a8;

}}


.REJECT {{

background:#ffb3b3;

}}


.stock {{

border-left:6px solid #555;

padding:15px;

margin-top:15px;

background:#fafafa;

}}


</style>


</head>


<body>


<h1>
AI Trading Research Dashboard v1.9
</h1>


<p>
Generated:
{datetime.now()}
</p>




<div class="grid">

"""



    for key,value in summary.items():


        html += f"""

<div class="metric">

<b>
{key}
</b>

<br>

{value}

</div>

"""



    html += """

</div>




<div class="card">

<h2>
AI Candidate Ranking
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
            "AI_Final_Decision"
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
AI Analyst Explanations
</h2>


"""



    for _,row in ranked.iterrows():


        html += f"""

<div class="stock">


<h3>
{row['Symbol']}
-
{row['AI_Final_Decision']}
</h3>


<p>

<b>
Conviction:
</b>

{round(row.get('Final_Conviction_Score',0),2)}

</p>


<p>

<b>
AI Explanation:
</b>

<br>

{row.get('AI_Explanation','N/A')}

</p>



<p>

<b>
Strengths:
</b>

<br>

{row.get('AI_Strengths','N/A')}

</p>



<p>

<b>
Weaknesses:
</b>

<br>

{row.get('AI_Weaknesses','N/A')}

</p>



<p>

<b>
Recommended Action:
</b>

<br>

{row.get('AI_Recommended_Action','N/A')}

</p>


</div>


"""



    html += """

</div>



<div class="card">

<h2>
Portfolio Risk Overview
</h2>

"""



    html += risk.to_html(
        index=False
    )



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

        html += (
            "<p>No strategy data available</p>"
        )


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

    print(
        "AI Dashboard Builder v1.9"
    )

    print("==============================")

    print()



    ai,risk,explanation,strategy = load_data()



    df = merge_data(
        ai,
        explanation
    )



    html = build_dashboard(
        df,
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