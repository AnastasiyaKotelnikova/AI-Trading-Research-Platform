"""
Performance Analyzer

Analyzes historical trading database performance.
"""

import os
import pandas as pd


INPUT_FILE = "data/trade_database.csv"
OUTPUT_DIR = "data/reports"


def analyze_performance():

    if not os.path.exists(INPUT_FILE):

        print("Trading database not found")

        return


    df = pd.read_csv(
        INPUT_FILE,
        low_memory=False
    )


    if df.empty:

        print("No trading records")

        return


    os.makedirs(
        OUTPUT_DIR,
        exist_ok=True
    )


    print("\n===== PERFORMANCE SUMMARY =====\n")


    total_trades = len(df)

    completed = df[
        df["Result"].isin(
            [
                "TARGET 1 HIT",
                "STOP HIT"
            ]
        )
    ]


    wins = len(
        completed[
            completed["Result"] == "TARGET 1 HIT"
        ]
    )


    losses = len(
        completed[
            completed["Result"] == "STOP HIT"
        ]
    )


    if len(completed) > 0:

        win_rate = (
            wins / len(completed)
        ) * 100

    else:

        win_rate = 0


    avg_return = df["Return_%"].mean()


    print(
        f"Total Records: {total_trades}"
    )

    print(
        f"Completed Trades: {len(completed)}"
    )

    print(
        f"Wins: {wins}"
    )

    print(
        f"Losses: {losses}"
    )

    print(
        f"Win Rate: {win_rate:.2f}%"
    )

    print(
        f"Average Return: {avg_return:.2f}%"
    )


    # -------------------------
    # Strategy performance
    # -------------------------

    if "Strategy" in df.columns:

        print(
            "\n===== STRATEGY PERFORMANCE =====\n"
        )


        strategy_report = (

            df.groupby("Strategy")
            .agg(
                Trades=("Symbol","count"),
                Avg_Return=("Return_%","mean")
            )

            .sort_values(
                "Avg_Return",
                ascending=False
            )

        )


        print(strategy_report)


        strategy_report.to_csv(
            f"{OUTPUT_DIR}/strategy_performance.csv"
        )


    # -------------------------
    # Signal performance
    # -------------------------

    if "Signal" in df.columns:

        print(
            "\n===== SIGNAL PERFORMANCE =====\n"
        )


        signal_report = (

            df.groupby("Signal")
            .agg(
                Trades=("Symbol","count"),
                Avg_Return=("Return_%","mean")
            )

            .sort_values(
                "Avg_Return",
                ascending=False
            )

        )


        print(signal_report)


        signal_report.to_csv(
            f"{OUTPUT_DIR}/signal_performance.csv"
        )


    # -------------------------
    # Score analysis
    # -------------------------

    if "Rank_Score" in df.columns:

        print(
            "\n===== SCORE PERFORMANCE =====\n"
        )


        df["Score_Group"] = pd.cut(
            df["Rank_Score"],
            bins=[
                0,
                60,
                70,
                80,
                90,
                100
            ],
            labels=[
                "<60",
                "60-70",
                "70-80",
                "80-90",
                "90-100"
            ]
        )


        score_report = (

            df.groupby("Score_Group", observed=True)
            .agg(
                Trades=("Symbol","count"),
                Avg_Return=("Return_%","mean")
            )

        )


        print(score_report)


        score_report.to_csv(
            f"{OUTPUT_DIR}/score_performance.csv"
        )


    print(
        "\nPerformance reports saved:"
    )

    print(
        OUTPUT_DIR
    )



if __name__ == "__main__":

    analyze_performance()
