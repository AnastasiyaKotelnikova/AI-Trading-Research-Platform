import pandas as pd
from pathlib import Path
from datetime import datetime


RESEARCH_FILE = Path(
    "data/analysis/research_ranked.csv"
)

CONFIDENCE_FILE = Path(
    "data/analysis/confidence_scores.csv"
)

OUTPUT_DIR = Path(
    "data/reports/stocks"
)



def create_stock_reports():

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )


    df = pd.read_csv(
        CONFIDENCE_FILE
    )


    top_stocks = (
        df
        .sort_values(
            by="Research_Score",
            ascending=False
        )
        .head(10)
    )


    for _, row in top_stocks.iterrows():

        symbol = row["Symbol"]

        confidence = row["Confidence_Score"]

        if confidence >= 90:

            confidence_label = "🟢 HIGH CONFIDENCE"


        elif confidence >= 70:

            confidence_label = "🟡 GOOD SETUP"


        else:

            confidence_label = "🔴 WATCH"
        

        reasons = []


        if row["Risk_Reward"] >= 3:

            reasons.append(
                "Strong risk/reward opportunity"
            )


        if row["Sector"] == "Healthcare":

            reasons.append(
                "Sector currently showing leadership"
            )


        if row["Strategy"] in [
            "STRONG PULLBACK",
            "QUALITY SETUP"
        ]:

            reasons.append(
                "Favorable historical setup"
            )



        html = f"""

<!DOCTYPE html>

<html>

<head>

<title>

{symbol} AI Research Report

</title>


<style>

body {{

font-family: Arial;
background:#f5f7fb;
margin:40px;

}}


.card {{

background:white;
padding:25px;
margin-bottom:25px;
border-radius:15px;
box-shadow:0 4px 12px rgba(0,0,0,0.08);

}}


.title {{

font-size:32px;
font-weight:bold;

}}


.score {{

font-size:24px;
font-weight:bold;

}}


img {{

max-width:900px;
border-radius:10px;

}}

</style>


</head>


<body>


<h1>

🔥 {symbol} AI Research Report

</h1>



<div class="card">


<h2>

<h2>
📊 Technical Chart Analysis
</h2>

</h2>


<img 
src="../../charts/professional/{symbol}.png"
width="900">

</div>

<div class="card">

<h2>

AI Decision

</h2>


<p>

<b>Confidence Score:</b>

{row['Confidence_Score']}/100

</p>


<p>

<b>Rating:</b>

{confidence_label}

</p>


</div>

<div class="card">


<div class="title">

AI Summary

</div>



<p>

<b>Strategy:</b>

{row['Strategy']}

</p>



<p>

<b>Sector:</b>

{row['Sector']}

</p>



<p class="score">

Research Score:

{row['Research_Score']}

</p>



<p>

Risk Reward:

{row['Risk_Reward']}

</p>


</div>





<div class="card">


<h2>

Technical Setup

</h2>



<p>

RSI:

{row['RSI']}

</p>



<p>

5 Day Return:

{row['Return_5D']}%

</p>



<p>

20 Day Return:

{row['Return_20D']}%

</p>



<p>

Above SMA20:

{row['Above_SMA20']}

</p>



<p>

Above SMA50:

{row['Above_SMA50']}

</p>



</div>





<div class="card">


<h2>

AI Explanation

</h2>


<ul>

"""


        for reason in reasons:

            html += f"""

<li>

{reason}

</li>

"""


        html += f"""

</ul>


</div>



<div class="card">


Generated:

{datetime.now()}


</div>



</body>

</html>

"""



        output_file = (
            OUTPUT_DIR /
            f"{symbol}.html"
        )


        with open(
            output_file,
            "w",
            encoding="utf-8"
        ) as file:

            file.write(html)



    print(
        "Stock reports created:"
    )


    print(
        OUTPUT_DIR
    )



if __name__ == "__main__":

    create_stock_reports()
