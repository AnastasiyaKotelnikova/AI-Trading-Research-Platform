"""
AI Report Generator v1.8

Final AI investment research reporting layer.

Input:
    data/analysis/final_ai_decision_controller.csv

Outputs:
    data/reports/AI_Report_TIMESTAMP.txt
    data/reports/AI_Report_TIMESTAMP.html
"""


import os
import pandas as pd
from datetime import datetime



REPORT_FOLDER = "data/reports"



# =====================================================
# SAFE DATA ACCESS
# =====================================================

def safe_value(row, key, default="N/A"):

    if key not in row:

        return default


    value = row[key]


    if pd.isna(value):

        return default


    return value



def safe_text(value):

    if isinstance(value, list):

        return ", ".join(value)

    return str(value)



# =====================================================
# PORTFOLIO SUMMARY
# =====================================================


def portfolio_summary(df):

    summary = {}


    summary["Generated"] = str(datetime.now())

    summary["Total Stocks"] = len(df)


    summary["BUY"] = len(
        df[
            df["AI_Final_Decision"]
            ==
            "BUY"
        ]
    )


    summary["WATCH"] = len(
        df[
            df["AI_Final_Decision"]
            ==
            "WATCH"
        ]
    )


    summary["REJECT"] = len(
        df[
            df["AI_Final_Decision"]
            ==
            "REJECT"
        ]
    )


    summary["Average Conviction"] = round(
        df["Final_Conviction_Score"]
        .mean(),
        2
    )


    summary["Average AI Analyst Score"] = round(
        df["AI_Analyst_Score"]
        .mean(),
        2
    )


    return summary



# =====================================================
# TEXT REPORT
# =====================================================


def generate_txt(df, filename):

    summary = portfolio_summary(df)


    ranked = df.sort_values(
        "Final_Conviction_Score",
        ascending=False
    )


    with open(
        filename,
        "w",
        encoding="utf-8"
    ) as f:


        f.write("="*70+"\n")
        f.write("AI STOCK INVESTMENT RESEARCH REPORT\n")
        f.write("="*70+"\n\n")


        for k,v in summary.items():

            f.write(
                f"{k}: {v}\n"
            )


        f.write("\n\nTOP AI RANKINGS\n")
        f.write("-"*50+"\n")


        for _,row in ranked.iterrows():


            f.write(

                f"{safe_value(row,'Decision_Rank')} | "

                f"{safe_value(row,'Symbol')} | "

                f"{safe_value(row,'AI_Final_Decision')} | "

                f"Conviction: "

                f"{safe_value(row,'Final_Conviction_Score')}\n"

            )



        for _,row in ranked.iterrows():


            f.write("\n")
            f.write("="*70+"\n")

            f.write(
                f"{row['Symbol']} AI ANALYSIS\n"
            )

            f.write("="*70+"\n\n")


            sections = {


                "Decision":
                "AI_Final_Decision",


                "Conviction":
                "Final_Conviction_Score",


                "AI Analyst Score":
                "AI_Analyst_Score",


                "Confidence":
                "AI_Analyst_Confidence",


                "Strategy":
                "Strategy",


                "Risk Grade":
                "Risk_Grade",


                "Risk Score":
                "Risk_Score",


                "Entry":
                "Entry",


                "Stop Loss":
                "Stop_Loss",


                "Target 1":
                "Target_1",


                "Target 2":
                "Target_2"

            }


            for name,column in sections.items():

                f.write(
                    f"{name}: "
                    f"{safe_value(row,column)}\n"
                )



            f.write("\nAI Explanation\n")
            f.write("-"*30+"\n")

            f.write(
                safe_text(
                    safe_value(
                        row,
                        "Decision_Reason"
                    )
                )
            )


            f.write("\n\nStrengths\n")
            f.write("-"*30+"\n")

            f.write(
                safe_text(
                    safe_value(row,"Strengths")
                )
            )


            f.write("\n\nRisks\n")
            f.write("-"*30+"\n")

            f.write(
                safe_text(
                    safe_value(row,"Risks")
                )
            )



# =====================================================
# HTML REPORT
# =====================================================


def generate_html(df, filename):


    summary = portfolio_summary(df)


    ranked = df.sort_values(
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

margin:40px;

background:#f5f5f5;

}}


.card {{

background:white;

padding:20px;

margin-bottom:20px;

border-radius:10px;

}}


table {{

width:100%;

border-collapse:collapse;

background:white;

}}


th,td {{

border:1px solid #ccc;

padding:10px;

text-align:center;

}}


.BUY {{

background:#90ee90;

}}


.WATCH {{

background:#fff3cd;

}}


.REJECT {{

background:#ffcccc;

}}


</style>


</head>


<body>


<h1>
AI Trading Research Dashboard
</h1>


<div class="card">

<h2>
Portfolio Summary
</h2>

"""


    for k,v in summary.items():

        html += f"<p><b>{k}</b>: {v}</p>"



    html += """

</div>


<div class="card">

<h2>
AI Rankings
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


        decision = safe_value(
            row,
            "AI_Final_Decision"
        )


        html += f"""


<tr class="{decision}">


<td>
{safe_value(row,'Decision_Rank')}
</td>


<td>
{safe_value(row,'Symbol')}
</td>


<td>
{decision}
</td>


<td>
{safe_value(row,'Final_Conviction_Score')}
</td>


<td>
{safe_value(row,'AI_Analyst_Score')}
</td>


<td>
{safe_value(row,'Risk_Grade')}
</td>


</tr>

"""



    html += """

</table>


</div>


</body>

</html>

"""


    with open(
        filename,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(html)



# =====================================================
# REPORT ENGINE
# =====================================================


def generate_ai_report(df):


    os.makedirs(
        REPORT_FOLDER,
        exist_ok=True
    )


    timestamp = datetime.now().strftime(
        "%Y-%m-%d_%H-%M"
    )


    txt_file = (
        f"{REPORT_FOLDER}/AI_Report_{timestamp}.txt"
    )


    html_file = (
        f"{REPORT_FOLDER}/AI_Report_{timestamp}.html"
    )


    generate_txt(
        df,
        txt_file
    )


    generate_html(
        df,
        html_file
    )


    print()
    print("AI Reports Generated:")
    print(txt_file)
    print(html_file)


    return {

        "txt":txt_file,

        "html":html_file

    }



# =====================================================
# DIRECT EXECUTION
# =====================================================


def main():

    print()
    print("==============================")
    print("AI Report Generator v1.8")
    print("==============================")
    print()


    input_file = (
        "data/analysis/final_ai_decision_controller.csv"
    )


    print(
        "Loading AI decisions..."
    )


    df = pd.read_csv(
        input_file,
        low_memory=False
    )


    print(
        f"Loaded stocks: {len(df)}"
    )


    generate_ai_report(df)


    print()
    print("Completed")



if __name__ == "__main__":

    main()