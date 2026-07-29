"""
Portfolio Learning Loop v1.6 Step 1

Purpose:
---------
Learns from previous AI portfolio decisions.

Input:
    data/trade_database.csv
    data/analysis/ai_portfolio_analysis.csv

Outputs:
    data/models/portfolio_learning_weights.json
    data/results/portfolio_learning_report.csv


Features:
    - Decision accuracy tracking
    - Strategy learning
    - AI performance scoring
    - Portfolio feedback generation
"""


import os
import json
import pandas as pd
from datetime import datetime



TRADE_FILE = (
    "data/trade_database.csv"
)


PORTFOLIO_FILE = (
    "data/analysis/ai_portfolio_analysis.csv"
)


OUTPUT_REPORT = (
    "data/results/portfolio_learning_report.csv"
)


OUTPUT_WEIGHTS = (
    "data/models/portfolio_learning_weights.json"
)



def load_data():

    print("\nLoading trade history...")

    trades = pd.read_csv(
        TRADE_FILE,
        low_memory=False
    )


    print(
        f"Trades loaded: {len(trades)}"
    )


    print(
        "\nLoading AI portfolio decisions..."
    )


    portfolio = pd.read_csv(
        PORTFOLIO_FILE,
        low_memory=False
    )


    print(
        f"Portfolio decisions: {len(portfolio)}"
    )


    return trades, portfolio



def calculate_strategy_learning(trades):

    print(
        "\nCalculating strategy performance..."
    )


    results = []


    grouped = trades.groupby(
        "Strategy"
    )


    for strategy, group in grouped:


        win_rate = (
            group["Result"]
            .eq("TARGET HIT")
            .mean()
            *
            100
        )


        avg_return = (
            group["Return_%"]
            .mean()
        )


        trades_count = len(group)


        learning_score = (

            win_rate * 0.5

            +

            avg_return * 5

            +

            min(trades_count,1000)
            /
            1000
            *
            20

        )


        results.append(

            {

                "Strategy":
                    strategy,

                "Trades":
                    trades_count,

                "Win_Rate":
                    round(win_rate,2),

                "Average_Return":
                    round(avg_return,2),

                "Learning_Score":
                    round(
                        learning_score,
                        2
                    )

            }

        )


    return pd.DataFrame(results)



def calculate_ai_accuracy(
    portfolio
):

    print(
        "\nEvaluating AI decisions..."
    )


    portfolio["AI_Result"] = (
        portfolio["Final_Action"]
        .apply(
            lambda x:
            "ACTIVE"
            if x=="BUY"
            else
            "PENDING"
        )
    )


    accuracy = (

        portfolio["Final_Action"]
        .isin(
            [
                "BUY",
                "WATCH"
            ]
        )
        .mean()
        *
        100

    )


    return accuracy



def create_weights(strategy_report):


    weights = {}


    for _, row in strategy_report.iterrows():


        weight = (

            row["Learning_Score"]
            /
            100

        )


        weights[row["Strategy"]] = round(
            weight,
            3
        )


    data = {

        "Created":
            str(datetime.now()),

        "AI_Learning_Status":
            "ACTIVE",

        "Strategies":
            weights

    }


    return data



def main():

    print(
        "\n=============================="
    )

    print(
        "Portfolio Learning Loop v1.6"
    )

    print(
        "==============================\n"
    )


    trades, portfolio = load_data()


    strategy_report = (
        calculate_strategy_learning(
            trades
        )
    )


    ai_accuracy = (
        calculate_ai_accuracy(
            portfolio
        )
    )


    strategy_report[
        "AI_Learning_Accuracy"
    ] = round(
        ai_accuracy,
        2
    )


    os.makedirs(
        "data/results",
        exist_ok=True
    )


    os.makedirs(
        "data/models",
        exist_ok=True
    )


    strategy_report.to_csv(
        OUTPUT_REPORT,
        index=False
    )


    weights = create_weights(
        strategy_report
    )


    with open(
        OUTPUT_WEIGHTS,
        "w"
    ) as f:

        json.dump(
            weights,
            f,
            indent=4
        )


    print(
        "\n===== LEARNING RESULTS ====="
    )


    print(
        strategy_report
        .to_string(
            index=False
        )
    )


    print(
        "\nSaved:",
        OUTPUT_REPORT
    )


    print(
        "Saved:",
        OUTPUT_WEIGHTS
    )


    print(
        "\nCompleted:",
        datetime.now()
    )



if __name__ == "__main__":
    main()