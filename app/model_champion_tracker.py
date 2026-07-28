import os
import pandas as pd
from datetime import datetime


FEEDBACK_FILE = (
    "data/models/model_feedback_report.csv"
)

MODEL_STATUS_FILE = (
    "data/models/model_champion_status.csv"
)



def update_champion_status():


    print(
        "\n========== MODEL CHAMPION TRACKER ==========\n"
    )


    if not os.path.exists(
        FEEDBACK_FILE
    ):

        print(
            "No feedback report found"
        )

        return



    df = pd.read_csv(
        FEEDBACK_FILE
    )


    latest = df.iloc[-1]



    status = pd.DataFrame([{

        "Evaluation_Date":
            latest["Evaluation_Date"],


        "Active_Model":
            "model_v27",


        "Completed_Trades":
            latest["Completed_Trades"],


        "Win_Rate":
            latest["Win_Rate"],


        "Average_Return":
            latest["Average_Return"],


        "Status":
            "CHAMPION"

    }])



    if os.path.exists(
        MODEL_STATUS_FILE
    ):

        old = pd.read_csv(
            MODEL_STATUS_FILE
        )


        status = pd.concat(
            [
                old,
                status
            ],
            ignore_index=True
        )



    status.to_csv(
        MODEL_STATUS_FILE,
        index=False
    )


    print(
        "Champion status saved:"
    )


    print(
        MODEL_STATUS_FILE
    )


    print(
        "\nCURRENT MODEL:"
    )


    print(
        status.tail(1)
    )




if __name__ == "__main__":

    update_champion_status()
