import os
import pandas as pd
from datetime import datetime


MODEL_FOLDER = "data/models"

METRICS_FILE = (
    "data/models/model_metrics.csv"
)



def get_latest_model_version():

    if not os.path.exists(MODEL_FOLDER):

        return "unknown"


    models = [

        f for f in os.listdir(MODEL_FOLDER)

        if f.startswith("model_v")
        and f.endswith(".pkl")

    ]


    if not models:

        return "unknown"


    versions = []

    for model in models:

        try:

            number = (
                model
                .replace("model_v", "")
                .replace(".pkl", "")
            )

            versions.append(
                int(number)
            )

        except:

            pass


    if not versions:

        return "unknown"


    return f"model_v{max(versions)}"




def save_model_metrics(
    accuracy,
    precision,
    recall,
    f1,
    records
):

    os.makedirs(
        MODEL_FOLDER,
        exist_ok=True
    )


    model_version = get_latest_model_version()



    if os.path.exists(METRICS_FILE):

        old = pd.read_csv(
            METRICS_FILE
        )

    else:

        old = pd.DataFrame()



    new_record = pd.DataFrame(
        [
            {

                "Date":
                    datetime.now()
                    .strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),


                "Model":
                    model_version,


                "Accuracy":
                    round(
                        accuracy,
                        3
                    ),


                "Precision":
                    round(
                        precision,
                        3
                    ),


                "Recall":
                    round(
                        recall,
                        3
                    ),


                "F1":
                    round(
                        f1,
                        3
                    ),


                "Status":
                    "Candidate",


                "Training_Records":
                    records

            }
        ]
    )



    updated = pd.concat(
        [
            old,
            new_record
        ],
        ignore_index=True
    )


    updated.drop_duplicates(
        subset=[
            "Model",
            "Date"
        ],
        inplace=True
    )


    updated.to_csv(
        METRICS_FILE,
        index=False
    )


    print(
        "\nModel metrics saved:"
    )

    print(
        METRICS_FILE
    )




def get_best_f1():


    if not os.path.exists(
        METRICS_FILE
    ):

        return 0



    df = pd.read_csv(
        METRICS_FILE
    )


    if "F1" not in df.columns:

        return 0



    df["F1"] = pd.to_numeric(
        df["F1"],
        errors="coerce"
    )


    return (
        df["F1"]
        .max()
    )




def get_champion_model():


    if not os.path.exists(
        METRICS_FILE
    ):

        return None



    df = pd.read_csv(
        METRICS_FILE
    )


    champions = df[
        df["Status"] == "Champion"
    ]


    if len(champions) == 0:

        return None



    return (
        champions
        .sort_values(
            "F1",
            ascending=False
        )
        .iloc[0]["Model"]
    )




def compare_candidate(
    candidate_f1
):

    best = get_best_f1()


    if candidate_f1 > best:

        return "PROMOTE"


    else:

        return "KEEP_CURRENT"
