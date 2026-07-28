import pandas as pd
from datetime import datetime
from pathlib import Path


REPORT_DIR = Path("data/reports")

RESEARCH_FILE = Path(
    "data/analysis/research_ranked.csv"
)

SECTOR_FILE = Path(
    "data/analysis/strategy_sector_results.csv"
)

MARKET_FILE = Path(
    "data/cache/market_snapshot.csv"
)

OUTPUT_FILE = REPORT_DIR / "daily_dashboard.html"



def create_dashboard():

    REPORT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )


    # Load data

    research_df = pd.read_csv(
        RESEARCH_FILE
    )


    sector_df = pd.read_csv(
        SECTOR_FILE
    )


    market_df = pd.read_csv(
        MARKET_FILE
    )


    # Sort research candidates

    top_candidates = (
        research_df
        .sort_values(
            by="Research_Score",
            ascending=False
        )
        .head(10)
    )


    # Sector analysis

    sector_summary = (
        sector_df
        .groupby("Sector")
        ["Return_%"]
        .mean()
        .sort_values(
            ascending=False
        )
        .head(5)
    )


    # Strategy distribution

    strategy_counts = (
        research_df["Strategy"]
        .value_counts()
    )


    # Market statistics

    stocks_scanned = len(
        market_df
    )


    avg_change = round(
        market_df["Change_%"].mean(),
        2
    )


    html = f"""

<!DOCTYPE html>

<html>

<head>

<title>
AI Trading Research Dashboard
</title>


<style>

body {{
font-family: Arial;
margin:40px;
background:#f4f4f4;
}}


.card {{
background:white;
padding:20px;
margin-bottom:20px;
border-radius:10px;
}}


h1 {{
color:#222;
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


<div class="card">

<h2>
Market Overview
</h2>


<p>
Generated:
{datetime.now()}
</p>


<p>
Stocks Scanned:
{stocks_scanned}
</p>


<p>
Average Market Change:
{avg_change}%
</p>


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
{round(value, 2)}%
</td>

</tr>

"""

    html += """

</table>

<br>

<img
src="../charts/sector_performance.png"
width="700">

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

<br>

<img
src="../charts/strategy_distribution.png"
width="700">

</div>



<div class="card">

<h2>
Top AI Research Picks
</h2>


<table>


<tr>

<th>
Symbol
</th>

<th>
Strategy
</th>

<th>
Research Score
</th>

<th>
Risk Reward
</th>

</tr>

"""


    for _, row in top_candidates.iterrows():

        html += f"""

<tr>

<td>
{row['Symbol']}
</td>

<td>
{row['Strategy']}
</td>

<td>
{row['Research_Score']}
</td>

<td>
{row['Risk_Reward']}
</td>


</tr>

"""


    html += """

</table>

<br>

<img
src="../charts/research_scores.png"
width="700">

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
