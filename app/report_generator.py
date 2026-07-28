import os
import ast
from datetime import datetime
import pandas as pd

from app.sector_strength import calculate_sector_strength
from app.market_dashboard import generate_dashboard
from app.dashboard_metrics import calculate_dashboard_metrics


def signal_class(signal):

    if signal == "STRONG BUY":
        return "strong-buy"

    elif signal == "BUY":
        return "buy"

    elif signal == "WATCH":
        return "watch"

    else:
        return "avoid"


INPUT_FILE = "data/cache/integrated_results.csv"
OUTPUT_FILE = "reports/daily_trade_report.html"


def generate_report():

    df = pd.read_csv(INPUT_FILE)

    top = df.head(20)

    market_regime = df["Market_Regime"].iloc[0]

    sector = calculate_sector_strength(df)

    dashboard = calculate_dashboard_metrics(df)

    dashboard = generate_dashboard(df)


    html = f"""
<html>

<head>

<title>
Daily Trade Report
</title>


<style>

body {{
    font-family: Arial, Helvetica, sans-serif;
    background: #f4f6f9;
    margin: 40px;
    color: #222;
}}

h1 {{
    text-align:center;
    color:#1f4e79;
}}

h2 {{
    color:#1f4e79;
    border-bottom:2px solid #1f4e79;
    padding-bottom:6px;
    margin-top:40px;
}}

h3 {{
    display:inline-block;
    background:#e8eef8;
    padding:10px 18px;
    border-radius:8px;
}}

table {{
    width:100%;
    border-collapse:collapse;
    background:white;
}}

th {{
    background:#1f4e79;
    color:white;
    padding:10px;
}}

td {{
    padding:10px;
    border:1px solid #ddd;
}}

tr:nth-child(even) {{
    background:#f7f9fc;
}}

pre {{
    white-space:pre-wrap;
}}

.summary {{
    text-align:center;
    color:#666;
}}

.card {{
    background:white;
    border-radius:12px;
    box-shadow:0 2px 10px rgba(0,0,0,.10);
    padding:20px;
}}

.score {{
    background:#1f4e79;
    color:white;
    padding:6px 12px;
    border-radius:6px;
}}

.reason-box {{
    background:#f7f9fc;
    border-left:4px solid #1f4e79;
    padding:12px;
    margin-top:15px;
}}

.dashboard {{
    display: flex;
    gap: 20px;
    flex-wrap: wrap;
    margin-top: 20px;
}}

.metric-card {{
    background: white;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0 2px 10px rgba(0,0,0,.10);
    min-width: 160px;
    text-align: center;
}}

.metric-title {{
    color: #666;
    font-size: 14px;
}}

.metric-value {{
    font-size: 30px;
    font-weight: bold;
    color: #1f4e79;
}}

.signal {{
    font-weight: bold;
    padding: 8px 14px;
    border-radius: 8px;
    display: inline-block;
}}

.strong-buy {{
    background: #d4edda;
    color: #155724;
}}

.buy {{
    background: #cce5ff;
    color: #004085;
}}

.watch {{
    background: #fff3cd;
    color: #856404;
}}

.avoid {{
    background: #f8d7da;
    color: #721c24;
}}

</style>

</head>


<body>


<h1>
Daily Trade Candidates
</h1>


<div class="summary">

Generated:

<b>
{datetime.now().strftime("%B %d, %Y %I:%M %p")}
</b>

</div>


<h2>
🌎 Market Regime
</h2>

<p>
Current Market:
<b>{market_regime}</b>
</p>


<h3>
{market_regime}
</h3>

"""
    

    html += f"""


<h2>
📊 Market Dashboard
</h2>


<div class="dashboard">


<div class="metric-card">
<div class="metric-title">
Stocks Scanned
</div>
<div class="metric-value">
{dashboard['Stocks_Scanned']}
</div>
</div>


<div class="metric-card">
<div class="metric-title">
Strong Buy
</div>
<div class="metric-value">
{dashboard['Strong_Buy']}
</div>
</div>


<div class="metric-card">
<div class="metric-title">
Buy Signals
</div>
<div class="metric-value">
{dashboard['Buy']}
</div>
</div>


<div class="metric-card">
<div class="metric-title">
Watch
</div>
<div class="metric-value">
{dashboard['Watch']}
</div>
</div>


<div class="metric-card">
<div class="metric-title">
Average Rank
</div>
<div class="metric-value">
{dashboard['Average_Rank']}
</div>
</div>


<div class="metric-card">
<div class="metric-title">
Average R/R
</div>
<div class="metric-value">
{dashboard['Average_RR']}
</div>
</div>


</div>

""" 


    html += sector[
        [
            "Sector",
            "Average_Rank",
            "Top20",
            "Stocks"
        ]
    ].to_html(index=False)



    # =========================
    # FEATURED TRADE
    # =========================

    if not top.empty:

        row = top.iloc[0]

        reasons = row["Trade_Reason"]

        score_breakdown = row["Score_Breakdown"]

        signal_reasons = ast.literal_eval(
            row["Signal_Explanation"]
        )


        html += f"""

<h2>
⭐ Featured Trade
</h2>


<div class="card">


<h2>
{row['Symbol']}
</h2>


<div class="score">

Score {int(row['Rank_Score'])}

</div>

<br>

<b>
Signal:
</b>

<span class="signal {signal_class(row['Signal'])}">
{row['Signal']}
</span>


<div class="reason-box">

<b>Why?</b>

<ul>

{"".join(
    f"<li>{x}</li>"
    for x in signal_reasons
)}

</ul>

</div>

<br>

<br>

<b>
Sector:
</b>
{row['Sector']}


<p>

Price:
${row['Price']}

<br>

Entry:
${row['Entry']}

<br>

Stop:
${row['Stop_Loss']}

<br>

Target 1:
${row['Target_1']}

<br>

Target 2:
${row['Target_2']}

<br>

Risk / Reward:
{row['Risk_Reward']}

</p>


<div class="reason-box">

<b>Trade Analysis</b>

<pre>
{reasons}
</pre>

</div>


<div class="reason-box">

<b>Score Breakdown</b>

<pre>
{score_breakdown}
</pre>

</div>


</div>

"""


    # =========================
    # TOP 20 TABLE
    # =========================


    html += """

<h2>
📈 Top 20 Ranked Stocks
</h2>


<table>

<tr>

<th>Symbol</th>
<th>Sector</th>
<th>Rank</th>
<th>Signal</th>
<th>Price</th>
<th>Entry</th>
<th>Stop</th>
<th>Target 1</th>
<th>Target 2</th>
<th>R/R</th>
<th>Reasons</th>

</tr>

"""


    for _, row in top.iterrows():

        reasons = row["Trade_Reason"]


        html += f"""

<tr>

<td>{row['Symbol']}</td>

<td>{row['Sector']}</td>

<td>{row['Rank_Score']}</td>

<td>

<span class="signal {signal_class(row['Signal'])}">
{row['Signal']}
</span>

</td>

<td>{row['Price']}</td>

<td>{row['Entry']}</td>

<td>{row['Stop_Loss']}</td>

<td>{row['Target_1']}</td>

<td>{row['Target_2']}</td>

<td>{row['Risk_Reward']}</td>

<td>
<pre>{reasons}</pre>
</td>

</tr>

"""


    html += """

</table>


</body>

</html>

"""


    os.makedirs(
        "reports",
        exist_ok=True
    )


    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(html)


    print("Saved:")
    print(OUTPUT_FILE)



if __name__ == "__main__":

    generate_report()
