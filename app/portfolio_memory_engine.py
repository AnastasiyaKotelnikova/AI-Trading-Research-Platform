"""
Portfolio Memory Engine v1.6 Step 3

Purpose:
---------
Stores historical AI portfolio decisions.

Input:
    data/analysis/rebalanced_portfolio.csv

Outputs:
    data/memory/portfolio_memory.csv
    data/results/portfolio_memory_report.csv

Features:
    - Decision history storage
    - Portfolio snapshot creation
    - Historical comparison
    - Learning foundation
"""


import os
import pandas as pd
from datetime import datetime



INPUT_FILE = (
    "data/analysis/rebalanced_portfolio.csv"
)


MEMORY_FILE = (
    "data/memory/portfolio_memory.csv"
)


REPORT_FILE = (
    "data/results/portfolio_memory_report.csv"
)



def load_current_portfolio():

    print("\nLoading current portfolio...")

    df = pd.read_csv(
        INPUT_FILE,
        low_memory=False
    )

    print(
        f"Current positions: {len(df)}"
    )

    return df



def create_snapshot(df):

    print(
        "\nCreating portfolio snapshot..."
    )


    snapshot = pd.DataFrame()


    columns = [

        "Symbol",
        "Sector",
        "Strategy",
        "Rebalanced_Score",
        "Rebalanced_Rank",
        "Rebalanced_Allocation_%",
        "Rebalance_Action",
        "Final_Action"

    ]


    for col in columns:

        if col in df.columns:

            snapshot[col] = df[col]


    snapshot["Snapshot_Date"] = (
        datetime.now()
    )


    return snapshot



def load_memory():

    if os.path.exists(
        MEMORY_FILE
    ):

        print(
            "\nLoading portfolio memory..."
        )

        return pd.read_csv(
            MEMORY_FILE,
            low_memory=False
        )


    print(
        "\nNo previous memory found."
    )


    return pd.DataFrame()



def update_memory(
    old_memory,
    snapshot
):

    print(
        "\nUpdating portfolio memory..."
    )


    memory = pd.concat(
        [
            old_memory,
            snapshot
        ],
        ignore_index=True
    )


    return memory



def analyze_memory(memory):

    print(
        "\nAnalyzing portfolio history..."
    )


    report = []


    grouped = memory.groupby(
        "Strategy"
    )


    for strategy, group in grouped:


        report.append(

            {

                "Strategy":
                    strategy,

                "Memory_Count":
                    len(group),

                "Average_Score":
                    round(
                        group[
                            "Rebalanced_Score"
                        ]
                        .mean(),
                        2
                    ),

                "Average_Allocation":
                    round(
                        group[
                            "Rebalanced_Allocation_%"
                        ]
                        .mean(),
                        2
                    )

            }

        )


    return pd.DataFrame(report)



def main():

    print(
        "\n=============================="
    )

    print(
        "Portfolio Memory Engine v1.6"
    )

    print(
        "==============================\n"
    )


    os.makedirs(
        "data/memory",
        exist_ok=True
    )


    os.makedirs(
        "data/results",
        exist_ok=True
    )


    current = load_current_portfolio()


    snapshot = create_snapshot(
        current
    )


    memory = load_memory()


    memory = update_memory(
        memory,
        snapshot
    )


    memory.to_csv(
        MEMORY_FILE,
        index=False
    )


    report = analyze_memory(
        memory
    )


    report.to_csv(
        REPORT_FILE,
        index=False
    )


    print(
        "\n===== MEMORY REPORT ====="
    )


    print(
        report
        .to_string(index=False)
    )


    print(
        "\nSaved:",
        MEMORY_FILE
    )


    print(
        "Saved:",
        REPORT_FILE
    )


    print(
        "\nCompleted:",
        datetime.now()
    )



if __name__ == "__main__":
    main()