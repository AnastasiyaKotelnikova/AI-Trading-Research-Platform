import pandas as pd
from datetime import datetime
from pathlib import Path


REPORT_DIR = Path("data/reports")


RESEARCH_FILE = Path(
    "data/analysis/research_ranked.csv"
)

CONFIDENCE_FILE = Path(
    "data/analysis/confidence_scores.csv"
)

SECTOR_FILE = Path(
    "data/analysis/strategy_sector_results.csv"
)

MARKET_FILE = Path(
    "data/cache/market_snapshot.csv"
)

CONFIDENCE_FILE = Path(
    "data/analysis/confidence_scores.csv"
)

OUTPUT_FILE = REPORT_DIR / "daily_dashboard.html"



def create_dashboard():

    REPORT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )


    research_df = pd.read_csv(
        RESEARCH_FILE
    )
 
    
    confidence_df = pd.read_csv(
        CONFIDENCE_FILE
    )

    sector_df = pd.read_csv(
        SECTOR_FILE
    )

    market_df = pd.read_csv(
        MARKET_FILE
    )


    top_candidates = (
        confidence_df
        .sort_values(
            by="Confidence_Score",
            ascending=False
        )
        .head(10)
    )


    sector_summary = (
        sector_df
        .groupby("Sector")["Return_%"]
        .mean()
        .sort_values(
            ascending=False
        )
        .head(5)
    )


    strategy_counts = (
        research_df["Strategy"]
        .value_counts()
    )


    stocks_scanned = len(
        market_df
    )


    avg_change = round(
        market_df["Change_%"].mean(),
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


        if row["Risk_Reward"] >= 3:
            reasons.append(
                "Strong risk/reward profile"
            )


        if row["RSI"] < 40:
            reasons.append(
                "RSI indicates pullback opportunity"
            )


        if row["Sector"] in sector_summary.index[:3]:
            reasons.append(
                "Strong sector momentum"
            )


        if row["Strategy"] in [
            "STRONG PULLBACK",
            "QUALITY SETUP"
        ]:
            reasons.append(
                "Historically favorable setup"
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
Stocks Scanned
</div>
<div class="metric-value">
{stocks_scanned}
</div>
</div>


<div class="metric">
<div class="metric-title">
Market Change
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
Average Return %
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
{round(value,2)}%
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
Top AI Research Picks
</h2>

"""


    for _, row in top_candidates.iterrows():

        reasons = generate_reason(row)

        confidence = row["Confidence_Score"]

        if confidence >= 90:
            confidence_label = "🟢 HIGH CONFIDENCE"

        elif confidence >= 70:
            confidence_label = "🟡 GOOD SETUP"

        else:
            confidence_label = "🔴 WATCH"


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
<b>Strategy:</b>
{row['Strategy']}
</p>


<p>

<b>Sector:</b>
{row['Sector']}
</p>


<p>
<b>Research Score:</b>
{row['Research_Score']}
</p>

<p>

<b>AI Confidence:</b>

{row['Confidence_Score']}/100

</p>

<p>

<b>AI Rating:</b>

{confidence_label}

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
