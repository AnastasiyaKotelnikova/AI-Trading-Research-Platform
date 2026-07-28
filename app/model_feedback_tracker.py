import pandas as pd
import os
from datetime import datetime


PREDICTION_FILE = (
    "data/models/model_predictions.csv"
)

FEEDBACK_FILE = (
    "data/models/model_feedback.csv"
)



def update_feedback():


    if not os.path.exists(PREDICTION_FILE):

        print("No predictions found.")
        return



    df = pd.read_csv(
        PREDICTION_FILE
    )


    if "Prediction_Result" not in df.columns:

        print(
            "Missing Prediction_Result column"
        )

        return



    completed = df[

        df["Prediction_Result"].notna()

    ].copy()



    if completed.empty:

        print(
            "No completed predictions yet."
        )

        return



    # Convert result into ML evaluation

    completed["Actual_Result"] = (

        completed["Return_5D"]

        >

        0

    ).astype(int)



    completed["Predicted_Result"] = (

        completed["ML_Probability"]

        >=

        50

    ).astype(int)



    completed["Prediction_Correct"] = (

        completed["Actual_Result"]

        ==

        completed["Predicted_Result"]

    )



    completed["Evaluation_Date"] = datetime.now()



    completed.to_csv(

        FEEDBACK_FILE,

        index=False

    )



    accuracy = (

        completed["Prediction_Correct"]

        .mean()

        *

        100

    )



    print()

    print(
        "MODEL FEEDBACK COMPLETE"
    )

    print(
        "Trades evaluated:",
        len(completed)
    )

    print(
        "Prediction Accuracy:",
        round(accuracy,2),
        "%"
    )



if __name__ == "__main__":

    update_feedback()