import pandas as pd
import os


METRICS_FILE = (
    "data/models/model_metrics.csv"
)



def get_current_model_info():


    if not os.path.exists(METRICS_FILE):

        return {
            "Model": "Unknown",
            "Accuracy": None,
            "F1": None,
            "Date": None,
            "Status": "Missing"
        }



    df = pd.read_csv(
        METRICS_FILE
    )



    # =================================================
    # CLEAN DATA
    # =================================================

    df["Accuracy"] = pd.to_numeric(
        df["Accuracy"],
        errors="coerce"
    )


    df["F1"] = pd.to_numeric(
        df["F1"],
        errors="coerce"
    )


    df["Date"] = pd.to_datetime(
        df["Date"],
        errors="coerce"
    )



    # Remove invalid rows

    df = df.dropna(
        subset=[
            "Accuracy",
            "F1",
            "Date"
        ]
    )



    # =================================================
    # SELECT VALID MODELS
    # Champion + Candidate only
    # =================================================

    valid = df[
        df["Status"].isin(
            [
                "Champion",
                "Candidate"
            ]
        )
    ].copy()



    if len(valid) == 0:

        return {
            "Model": "Unknown",
            "Accuracy": None,
            "F1": None,
            "Date": None,
            "Status": "No Valid Model"
        }



    # =================================================
    # MODEL SELECTION
    #
    # Priority:
    # 1. Highest F1
    # 2. Highest Accuracy
    # 3. Newest training date
    # =================================================

    valid = valid.sort_values(

        [
            "F1",
            "Accuracy",
            "Date"
        ],

        ascending=[
            False,
            False,
            False
        ]

    )



    best = valid.iloc[0]



    return {


        "Model":
            best["Model"],


        "Accuracy":
            round(
                best["Accuracy"] * 100,
                2
            ),


        "F1":
            round(
                best["F1"] * 100,
                2
            ),


        "Date":
            best["Date"],


        "Status":
            best["Status"]

    }