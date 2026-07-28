import pandas as pd
import os
from datetime import datetime


TRADE_DATABASE = (
    "data/trade_database.csv"
)

PERFORMANCE_FILE = (
    "data/models/model_predictions.csv"
)

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



    completed = df[
        df["Result"].notna()
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



    report = {

        "Evaluation_Date":
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),


        "Completed_Trades":
            len(completed),


        "Winning_Trades":
            len(
                completed[
                    completed["Return_%"] > 0
                ]
            ),


        "Win_Rate":

            round(
                (
                    len(
                        completed[
                            completed["Return_%"] > 0
                        ]
                    )
                    /
                    len(completed)
                )
                *
                100,

                2
            ),


        "Average_Return":

            round(
                completed["Return_%"]
                .mean(),

                2
            )

    }



    output = pd.DataFrame(
        [report]
    )



    if os.path.exists(
        OUTPUT_FILE
    ):

        old = pd.read_csv(
            OUTPUT_FILE
        )

        output = pd.concat(
            [
                old,
                output
            ],
            ignore_index=True
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



if __name__ == "__main__":

    update_model_feedback()
