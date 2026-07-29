"""
AI Decision Feedback Engine v1.6 Step 4

Purpose:
---------
Evaluates previous AI decisions against actual outcomes.

Input:
    data/memory/portfolio_memory.csv
    data/trade_database.csv

Outputs:
    data/results/ai_decision_feedback_report.csv
    data/models/ai_feedback_weights.json

Features:
    - AI decision accuracy
    - Strategy feedback
    - Prediction quality
    - Learning weights
"""


import os
import json
import pandas as pd
from datetime import datetime



MEMORY_FILE = (
    "data/memory/portfolio_memory.csv"
)


TRADE_FILE = (
    "data/trade_database.csv"
)


REPORT_FILE = (
    "data/results/ai_decision_feedback_report.csv"
)


WEIGHTS_FILE = (
    "data/models/ai_feedback_weights.json"
)



def load_data():

    print("\nLoading portfolio memory...")

    memory = pd.read_csv(
        MEMORY_FILE,
        low_memory=False
    )


    print(
        f"Memory records: {len(memory)}"
    )


    print(
        "\nLoading trade history..."
    )

    trades = pd.read_csv(
        TRADE_FILE,
        low_memory=False
    )


    print(
        f"Trades loaded: {len(trades)}"
    )


    return memory, trades



def match_decisions(
    memory,
    trades
):

    print(
        "\nMatching AI decisions with outcomes..."
    )


    merged = memory.merge(
        trades[
            [
                "Symbol",
                "Strategy",
                "Result",
                "Return_%"
            ]
        ],
        on=[
            "Symbol",
            "Strategy"
        ],
        how="left"
    )


    return merged



def evaluate_decisions(df):

    print(
        "\nEvaluating AI performance..."
    )


    df["Successful"] = (

        df["Result"]
        .isin(
            [
                "TARGET HIT",
                "WIN"
            ]
        )

    )


    grouped = df.groupby(
        [
            "Strategy",
            "Rebalance_Action"
        ]
    )


    results = []


    for name, group in grouped:


        strategy, action = name


        success_rate = (

            group["Successful"]
            .mean()
            *
            100

        )


        avg_return = (

            group["Return_%"]
            .mean()

        )


        score = (

            success_rate * 0.6

            +

            avg_return * 5

        )


        results.append(

            {

                "Strategy":
                    strategy,

                "AI_Action":
                    action,

                "Trades":
                    len(group),

                "Success_Rate":
                    round(
                        success_rate,
                        2
                    ),

                "Average_Return":
                    round(
                        avg_return,
                        2
                    ),

                "Feedback_Score":
                    round(
                        score,
                        2
                    )

            }

        )


    return pd.DataFrame(results)



def create_feedback_weights(report):


    weights = {}


    for _, row in report.iterrows():


        key = (

            row["Strategy"]
            +
            "_"
            +
            row["AI_Action"]

        )


        weights[key] = round(

            row["Feedback_Score"]
            /
            100,

            3

        )


    return {

        "Created":
            str(datetime.now()),

        "Learning_Status":
            "ACTIVE",

        "Feedback_Weights":
            weights

    }



def main():

    print(
        "\n=============================="
    )

    print(
        "AI Decision Feedback Engine v1.6"
    )

    print(
        "==============================\n"
    )


    memory, trades = load_data()


    merged = match_decisions(
        memory,
        trades
    )


    report = evaluate_decisions(
        merged
    )


    os.makedirs(
        "data/results",
        exist_ok=True
    )

    os.makedirs(
        "data/models",
        exist_ok=True
    )


    report.to_csv(
        REPORT_FILE,
        index=False
    )


    weights = create_feedback_weights(
        report
    )


    with open(
        WEIGHTS_FILE,
        "w"
    ) as f:

        json.dump(
            weights,
            f,
            indent=4
        )


    print(
        "\n===== AI FEEDBACK RESULTS ====="
    )


    print(
        report
        .to_string(index=False)
    )


    print(
        "\nSaved:",
        REPORT_FILE
    )


    print(
        "Saved:",
        WEIGHTS_FILE
    )


    print(
        "\nCompleted:",
        datetime.now()
    )



if __name__ == "__main__":
    main()