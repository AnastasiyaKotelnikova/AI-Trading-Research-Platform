import os
import pandas as pd
from datetime import datetime


PERFORMANCE_FILE = (
    "data/models/model_predictions.csv"
)


def save_prediction_performance(
    df,
    model_info
):

    os.makedirs(
        "data/models",
        exist_ok=True
    )


    records = []


    for _, row in df.iterrows():

        records.append({

            "Date":
                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),

            "Model":
                model_info["Model"],


            "Symbol":
                row.get(
                    "Symbol",
                    None
                ),


            "ML_Probability":
                row.get(
                    "ML_Probability",
                    None
                ),


            "AI_Final_Score":
                row.get(
                    "AI_Final_Score",
                    None
                ),


            "AI_Rating":
                row.get(
                    "AI_Rating",
                    None
                ),


            "Rank_Score":
                row.get(
                    "Rank_Score",
                    None
                ),


            "Entry_Price":
                row.get(
                    "Entry",
                    None
                ),


            "Stop_Loss":
                row.get(
                    "Stop_Loss",
                    None
                ),


            "Target_1":
                row.get(
                    "Target_1",
                    None
                ),


            "Target_2":
                row.get(
                    "Target_2",
                    None
                ),


            "Market_Regime":
                row.get(
                    "Market_Regime",
                    None
                ),


            # Future evaluation fields

            "Price_After_5D":
                None,


            "Price_After_20D":
                None,


            "Return_5D":
                None,


            "Return_20D":
                None,


            "Prediction_Result":
                None

        })



    new_df = pd.DataFrame(
        records
    )



    if os.path.exists(
        PERFORMANCE_FILE
    ):

        old_df = pd.read_csv(
            PERFORMANCE_FILE
        )


        updated = pd.concat(
            [
                old_df,
                new_df
            ],
            ignore_index=True
        )


    else:

        updated = new_df



    updated.to_csv(
        PERFORMANCE_FILE,
        index=False
    )


    print(
        "\nPerformance tracking saved:"
    )

    print(
        PERFORMANCE_FILE
    )
