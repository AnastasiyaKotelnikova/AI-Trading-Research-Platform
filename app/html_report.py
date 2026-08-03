import pandas as pd
from pathlib import Path


REPORT_DIR = Path("data/reports")

AI_SIGNALS_FILE = Path(
    "data/analysis/final_ai_signals.csv"
)

OUTPUT_FILE = REPORT_DIR / "daily_dashboard.html"


def create_dashboard():

    REPORT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    # Load current AI signals
    ai_df = pd.read_csv(
        AI_SIGNALS_FILE
    )


    # Sort current AI opportunities
    top_candidates = (
        ai_df
        .sort_values(
            by="AI_Final_Score_Adjusted",
            ascending=False
        )
        .head(10)
    )


    # Sector summary
    sector_summary = (
        ai_df
        .groupby("Sector")["AI_Final_Score_Adjusted"]
        .mean()
        .sort_values(
            ascending=False
        )
        .head(5)
    )


    # Strategy distribution
    strategy_counts = (
        ai_df["Strategy"]
        .value_counts()
    )


    stocks_scanned = len(
        ai_df
    )


    avg_change = round(
        ai_df["Change_%"].mean(),
        2
    )


    top_sector = (
        sector_summary.index[0]
        if len(sector_summary) > 0
        else "N/A"
    )


    top_strategy = (
        strategy_counts.index[0]
        if len(strategy_counts) > 0
        else "N/A"
    )


    def generate_reason(row):

        reasons = []


        if row["Risk_Reward"] >= 2:
            reasons.append(
                "Strong risk/reward profile"
            )


        if row["RSI"] < 40:
            reasons.append(
                "RSI indicates pullback opportunity"
            )


        if row["Above_SMA20"]:
            reasons.append(
                "Price above 20-day moving average"
            )


        if row["Above_SMA50"]:
            reasons.append(
                "Price above 50-day moving average"
            )


        if row["Historical_ML_Probability"] >= 60:
            reasons.append(
                "Strong historical ML confirmation"
            )


        if len(reasons) == 0:
            reasons.append(
                "AI ranked based on combined model scoring"
            )


        return reasons



    html = f"""

<!DOCTYPE html>

<html>

<head>

<title>
AI Trading Research Dashboard
</title>


<style>

body {{
font-family: Arial, sans-serif;
margin:40px;
background:#f5f7fb;
color:#222;
}}

.metrics {{
display:flex;
gap:20px;
flex-wrap:wrap;
}}

.metric {{
background:white;
padding:20px;
width:220px;
border-radius:15px;
box-shadow:0 4px 12px rgba(0,0,0,0.08);
}}

.metric-title {{
color:#666;
}}

.metric-value {{
font-size:28px;
font-weight:bold;
}}

.card {{
background:white;
padding:25px;
margin-top:25px;
border-radius:15px;
box-shadow:0 4px 12px rgba(0,0,0,0.08);
}}

.pick-card {{
background:white;
padding:25px;
margin-bottom:20px;
border-radius:15px;
box-shadow:0 4px 12px rgba(0,0,0,0.08);
}}

.pick-title {{
font-size:26px;
font-weight:bold;
}}

.button {{
background:#222;
color:white;
padding:10px 15px;
border-radius:8px;
text-decoration:none;
display:inline-block;
margin-top:10px;
}}

table {{
width:100%;
border-collapse:collapse;
}}

th {{
background:#222;
color:white;
padding:10px;
}}

td {{
padding:10px;
border-bottom:1px solid #ddd;
}}

</style>

</head>


<body>


<h1>
AI Trading Research Dashboard
</h1>



<div class="metrics">


<div class="metric">
<div class="metric-title">
AI Candidates
</div>

<div class="metric-value">
{stocks_scanned}
</div>

</div>



<div class="metric">
<div class="metric-title">
Average Daily Change
</div>

<div class="metric-value">
{avg_change}%
</div>

</div>



<div class="metric">
<div class="metric-title">
Top Sector
</div>

<div class="metric-value">
{top_sector}
</div>

</div>



<div class="metric">
<div class="metric-title">
Top Strategy
</div>

<div class="metric-value">
{top_strategy}
</div>

</div>


</div>



<div class="card">

<h2>
Sector Leadership
</h2>


<table>

<tr>
<th>
Sector
</th>

<th>
Average AI Score
</th>

</tr>

"""


    for sector, value in sector_summary.items():

        html += f"""

<tr>

<td>
{sector}
</td>

<td>
{round(value,2)}
</td>

</tr>

"""


    html += """

</table>

</div>





<div class="card">

<h2>
Strategy Distribution
</h2>


<table>

<tr>

<th>
Strategy
</th>

<th>
Count
</th>

</tr>

"""


    for strategy, count in strategy_counts.items():

        html += f"""

<tr>

<td>
{strategy}
</td>

<td>
{count}
</td>

</tr>

"""


    html += """

</table>

</div>





<div class="card">

<h2>
Top AI Trading Candidates
</h2>

"""


    for _, row in top_candidates.iterrows():


        confidence = row["AI_Confidence"]


        if confidence >= 70:

            confidence_label = "🟢 HIGH CONFIDENCE"

        elif confidence >= 40:

            confidence_label = "🟡 MODERATE"

        else:

            confidence_label = "🔴 LOW"



        reasons = generate_reason(row)



        html += f"""

<div class="pick-card">


<div class="pick-title">

🔥 {row['Symbol']}

</div>



<a class="button"

href="stocks/{row['Symbol']}.html">

View Full Analysis

</a>



<p>

<b>Sector:</b>
{row['Sector']}

</p>



<p>

<b>Strategy:</b>
{row['Strategy']}

</p>



<p>

<b>AI Score:</b>
{round(row['AI_Final_Score_Adjusted'],2)}

</p>



<p>

<b>AI Confidence:</b>
{round(confidence,2)}/100

</p>



<p>

<b>Status:</b>
{confidence_label}

</p>



<p>

<b>Research Score:</b>
{round(row['Research_Score'],2)}

</p>



<p>

<b>Risk Reward:</b>
{row['Risk_Reward']}

</p>



<p>
<b>Why selected:</b>
</p>


<ul>

"""


        for reason in reasons:

            html += f"""

<li>
{reason}
</li>

"""


        html += """

</ul>

</div>

"""


    html += """

</div>


</body>

</html>

"""


    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(html)


    print(
        "Dashboard created:"
    )

    print(
        OUTPUT_FILE
    )



if __name__ == "__main__":

    create_dashboard()