import pandas as pd
import os
from datetime import datetime


TRADE_DATABASE = "data/trade_history.csv"

OUTPUT_FILE = (
    "data/models/model_feedback_report.csv"
)



def update_model_feedback():

    print("\n========== MODEL FEEDBACK LOOP ==========\n")


    if not os.path.exists(TRADE_DATABASE):

        print(
            "Trade database missing"
        )

        return



    df = pd.read_csv(
        TRADE_DATABASE,
        low_memory=False
    )



    # Only completed trades
    completed = df[
        df["Status"] == "CLOSED"
    ].copy()



    if "Model_Name" not in completed.columns:
        completed["Model_Name"] = "UNKNOWN"



    # Remove missing model names
    completed = completed[
        completed["Model_Name"].notna()
    ]



    # Convert Return to numeric
    completed["Return_%"] = pd.to_numeric(
        completed["Return_%"],
        errors="coerce"
    )



    completed = completed[
        completed["Return_%"].notna()
    ]



    print(
        "Completed Trades:"
    )

    print(
        len(completed)
    )



    if len(completed) == 0:

        print(
            "No completed trades yet"
        )

        return



    reports = []



    for model, trades in completed.groupby(
        "Model_Name",
        dropna=False
    ):


        wins = trades[
            trades["Return_%"] > 0
        ]



        losses = trades[
            trades["Return_%"] <= 0
        ]



        report = {


            "Evaluation_Date":
                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),



            "Model":
                model,



            "Completed_Trades":
                len(trades),



            "Winning_Trades":
                len(wins),



            "Losing_Trades":
                len(losses),



            "Win_Rate":
                round(
                    len(wins)
                    /
                    len(trades)
                    *
                    100,

                    2
                ),



            "Average_Return":
                round(
                    trades["Return_%"]
                    .mean(),

                    2
                ),



            "Best_Trade":
                round(
                    trades["Return_%"]
                    .max(),

                    2
                ),



            "Worst_Trade":
                round(
                    trades["Return_%"]
                    .min(),

                    2
                ),



        }



        # Capture model metrics if stored
        if "Model_Accuracy" in trades.columns:

            report["Model_Accuracy"] = (
                trades["Model_Accuracy"]
                .dropna()
                .iloc[0]
                if not trades["Model_Accuracy"]
                .dropna()
                .empty
                else None
            )


        if "Model_F1" in trades.columns:

            report["Model_F1"] = (
                trades["Model_F1"]
                .dropna()
                .iloc[0]
                if not trades["Model_F1"]
                .dropna()
                .empty
                else None
            )



        reports.append(report)



    output = pd.DataFrame(
        reports
    )



    # Rank models by real trading performance
    output = output.sort_values(
        by=[
            "Average_Return",
            "Win_Rate"
        ],
        ascending=False
    )



    output.to_csv(
        OUTPUT_FILE,
        index=False
    )



    print(
        "\nFeedback report saved:"
    )

    print(
        OUTPUT_FILE
    )


    print(
        "\nModel Performance:"
    )

    print(
        output.to_string(
            index=False
        )
    )



if __name__ == "__main__":

    update_model_feedback()