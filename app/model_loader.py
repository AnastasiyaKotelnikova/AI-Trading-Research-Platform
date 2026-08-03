import os
import pandas as pd
import joblib


MODEL_FOLDER = "data/models"


CHAMPION_STATUS_FILE = (
    "data/models/model_champion_status.csv"
)


OPTIMIZED_MODEL = (
    "data/models/optimized_trading_model.pkl"
)



# ==================================================
# Load Active Scanner Champion Model
# ==================================================

def get_best_model():

    status = load_champion_status()


    if status is not None:


        champion = status[
            status["Status"].str.upper() == "CHAMPION"
        ]


        if not champion.empty:


            # newest champion record
            champion = champion.sort_values(
                by="Evaluation_Date",
                ascending=False
            )


            model_name = (
                champion.iloc[0]["Active_Model"]
            )


            model_file = (
                f"{MODEL_FOLDER}/{model_name}.pkl"
            )


            if os.path.exists(model_file):


                print(
                    "\nLoading Active Scanner Champion Model:"
                )

                print(
                    model_file
                )


                return joblib.load(
                    model_file
                )



    # fallback historical model

    if os.path.exists(OPTIMIZED_MODEL):


        print(
            "\nLoading Optimized Historical Model:"
        )


        return joblib.load(
            OPTIMIZED_MODEL
        )



    raise FileNotFoundError(
        "No active scanner champion model found."
    )





# ==================================================
# Get Active Model Information
# ==================================================

def get_best_model_info():


    status = load_champion_status()


    if status is not None:


        champion = status[
            status["Status"].str.upper() == "CHAMPION"
        ]


        if not champion.empty:


            champion = champion.sort_values(
                by="Evaluation_Date",
                ascending=False
            )


            row = champion.iloc[0]


            return {


                "Model":
                    row["Active_Model"],


                "Accuracy":
                    row.get(
                        "Accuracy",
                        0
                    ),


                "F1":
                    row.get(
                        "F1",
                        0
                    ),


                "Completed_Trades":
                    row.get(
                        "Completed_Trades",
                        0
                    ),


                "Win_Rate":
                    row.get(
                        "Win_Rate",
                        0
                    ),


                "Average_Return":
                    row.get(
                        "Average_Return",
                        0
                    ),


                "Status":
                    row["Status"],


                "Date":
                    row["Evaluation_Date"]

            }



    return {


        "Model":
            "Unknown",


        "Accuracy":
            0,


        "F1":
            0,


        "Completed_Trades":
            0,


        "Win_Rate":
            0,


        "Average_Return":
            0,


        "Status":
            "Missing",


        "Date":
            None

    }





# ==================================================
# Load Champion Status History
# ==================================================

def load_champion_status():


    if not os.path.exists(
        CHAMPION_STATUS_FILE
    ):

        return None



    df = pd.read_csv(
        CHAMPION_STATUS_FILE
    )


    return df