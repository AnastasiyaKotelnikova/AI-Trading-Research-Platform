import os
import pandas as pd
from datetime import datetime


MONITOR_FILE = (
    "data/models/model_monitoring.csv"
)


def save_model_run(
    model_info,
    results_df,
    market_regime=None
):

    os.makedirs(
        "data/models",
        exist_ok=True
    )


    record = {

        "Date":
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),


        "Model":
            model_info["Model"],


        "Accuracy":
            float(
                model_info["Accuracy"]
            ),


        "F1":
            float(
                model_info["F1"]
            ),


        "Market_Regime":
            market_regime
            if market_regime
            else "Unknown",


        "Stocks_Scanned":
            len(results_df),


        "Average_ML_Probability":
            round(
                results_df["ML_Probability"].mean(),
                2
            ),


        "Highest_ML_Probability":
            round(
                results_df["ML_Probability"].max(),
                2
            ),


        "Top_Ranked_Stock":
            results_df.iloc[0]["Symbol"]
            if len(results_df) > 0
            else None,


        "Average_AI_Score":
            round(
                results_df["AI_Final_Score"].mean(),
                2
            )

    }


    new_record = pd.DataFrame(
        [record]
    )


    if os.path.exists(
        MONITOR_FILE
    ):

        old = pd.read_csv(
            MONITOR_FILE
        )

        df = pd.concat(
            [
                old,
                new_record
            ],
            ignore_index=True
        )

    else:

        df = new_record



    df.to_csv(
        MONITOR_FILE,
        index=False
    )


    print(
        "\nModel run saved:"
    )

    print(
        MONITOR_FILE
    )
