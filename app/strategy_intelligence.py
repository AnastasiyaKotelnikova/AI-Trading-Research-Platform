"""
Strategy Intelligence Engine v1.4

Analyzes historical trading strategy performance.

Goals:
- Rank strategies by historical reliability
- Measure consistency
- Identify strongest strategies
- Provide intelligence layer for future AI decisions

Input:
    data/trade_database.csv

Output:
    data/results/strategy_intelligence_report.csv
    data/models/strategy_weights.json
"""


import pandas as pd
import numpy as np
import json
from pathlib import Path
from datetime import datetime


INPUT_FILE = "data/trade_database.csv"

OUTPUT_DIR = Path("data/results")
MODEL_DIR = Path("data/models")

REPORT_FILE = OUTPUT_DIR / "strategy_intelligence_report.csv"
WEIGHTS_FILE = MODEL_DIR / "strategy_weights.json"


MIN_TRADES = 50
MIN_SYMBOLS = 5


def load_data():

    print("\nLoading trade database...")

    df = pd.read_csv(
        INPUT_FILE,
        low_memory=False
    )

    print(f"Total trades loaded: {len(df)}")

    return df



def calculate_strategy_metrics(df):

    print("\nAnalyzing strategies...")


    required = [
        "Strategy",
        "Result",
        "Return_%",
        "Symbol"
    ]


    for col in required:
        if col not in df.columns:
            raise Exception(
                f"Missing required column: {col}"
            )


    results = []


    grouped = df.groupby("Strategy")


    for strategy, group in grouped:


        trades = len(group)

        symbols = group["Symbol"].nunique()


        if trades < MIN_TRADES:
            continue


        if symbols < MIN_SYMBOLS:
            continue



        wins = group[
            group["Result"].isin(
                [
                    "TARGET 1 HIT",
                    "TARGET 2 HIT"
                ]
            )
        ]


        losses = group[
            group["Result"] == "STOP HIT"
        ]



        win_rate = (
            len(wins)
            /
            max(
                len(wins)+len(losses),
                1
            )
            *
            100
        )



        avg_return = (
            group["Return_%"]
            .mean()
        )


        avg_win = (
            wins["Return_%"]
            .mean()
            if len(wins)
            else 0
        )


        avg_loss = (
            losses["Return_%"]
            .mean()
            if len(losses)
            else 0
        )


        profit_factor = abs(
            (
                wins["Return_%"].sum()
                /
                losses["Return_%"].sum()
            )
        ) if len(losses) else 0



        consistency = min(
            trades / 500,
            1
        )


        reliability_score = (

            win_rate * 0.30

            +

            avg_return * 5 * 0.25

            +

            profit_factor * 10 * 0.25

            +

            consistency * 100 * 0.20

        )


        results.append({

            "Strategy": strategy,

            "Trades": trades,

            "Symbols": symbols,

            "Win_Rate": round(
                win_rate,
                2
            ),

            "Average_Return": round(
                avg_return,
                2
            ),

            "Avg_Win": round(
                avg_win,
                2
            ),

            "Avg_Loss": round(
                avg_loss,
                2
            ),

            "Profit_Factor": round(
                profit_factor,
                2
            ),

            "Reliability_Score": round(
                reliability_score,
                2
            )

        })



    report = pd.DataFrame(results)


    if len(report):

        report = report.sort_values(
            "Reliability_Score",
            ascending=False
        )


    return report




def create_strategy_weights(report):

    print("\nCreating strategy weights...")


    weights = {}


    for _, row in report.iterrows():


        score = row["Reliability_Score"]


        if score >= 80:

            rating = "HIGH"

        elif score >= 50:

            rating = "MEDIUM"

        else:

            rating = "LOW"



        weights[row["Strategy"]] = {

            "Weight": round(
                score / 100,
                3
            ),

            "Reliability": rating,

            "Trades": int(
                row["Trades"]
            ),

            "Win_Rate": row["Win_Rate"],

            "Average_Return":
                row["Average_Return"]

        }



    return weights




def save_outputs(report, weights):


    OUTPUT_DIR.mkdir(
        exist_ok=True
    )

    MODEL_DIR.mkdir(
        exist_ok=True
    )


    report.to_csv(
        REPORT_FILE,
        index=False
    )


    with open(
        WEIGHTS_FILE,
        "w"
    ) as f:

        json.dump(
            {
                "Created":
                    str(datetime.now()),

                "Strategies":
                    weights

            },
            f,
            indent=4
        )



    print(
        f"\nSaved: {REPORT_FILE}"
    )

    print(
        f"Saved: {WEIGHTS_FILE}"
    )




def main():

    df = load_data()


    report = calculate_strategy_metrics(
        df
    )


    print(
        "\n===== STRATEGY INTELLIGENCE RESULTS =====\n"
    )


    if len(report):

        print(
            report.to_string(
                index=False
            )
        )

    else:

        print(
            "No strategies passed reliability filters."
        )


    weights = create_strategy_weights(
        report
    )


    save_outputs(
        report,
        weights
    )



if __name__ == "__main__":

    main()