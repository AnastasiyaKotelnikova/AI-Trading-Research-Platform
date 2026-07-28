import os
import pandas as pd
import joblib

from datetime import datetime


MODEL_FOLDER = "data/models"

METRICS_FILE = (
    "data/models/model_metrics.csv"
)



# =====================================================
# GET NEXT MODEL VERSION
# =====================================================

def get_next_version():

    os.makedirs(
        MODEL_FOLDER,
        exist_ok=True
    )


    files = [

        f

        for f in os.listdir(MODEL_FOLDER)

        if f.startswith("model_v")
        and f.endswith(".pkl")

    ]


    if not files:
        return 1


    versions = []


    for f in files:

        number = (
            f.replace(
                "model_v",
                ""
            )
            .replace(
                ".pkl",
                ""
            )
        )


        versions.append(
            int(number)
        )


    return max(versions) + 1





# =====================================================
# CURRENT CHAMPION F1
# =====================================================

def get_current_champion_f1():


    if not os.path.exists(
        METRICS_FILE
    ):

        return 0



    df = pd.read_csv(
        METRICS_FILE
    )


    if "Status" not in df.columns:

        return 0



    champions = df[
        df["Status"]
        ==
        "Champion"
    ]



    if champions.empty:

        return 0



    return champions["F1"].max()





# =====================================================
# SAVE VERSIONED MODEL
# =====================================================

def save_versioned_model(
    model,
    accuracy,
    precision,
    recall,
    f1,
    records,
    features=None,
    parameters=None
):


    version = get_next_version()



    model_name = (
        f"model_v{version}"
    )


    filename = (

        MODEL_FOLDER
        +
        f"/{model_name}.pkl"

    )


    joblib.dump(
        model,
        filename
    )



    champion_f1 = (
        get_current_champion_f1()
    )



    # New Champion requires improvement

    if f1 > champion_f1 + 0.002:


        status = "Champion"


        print(
            "\nNew Champion model!"
        )


    else:


        status = "Candidate"


        print(
            "\nCandidate model saved."
        )





    record = {


        "Date":
            datetime.now(),


        "Model":
            model_name,


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
            status,


        "Training_Records":
            records

    }





    if os.path.exists(
        METRICS_FILE
    ):


        df = pd.read_csv(
            METRICS_FILE
        )


    else:


        df = pd.DataFrame()





    # Archive old champion

    if status == "Champion" and not df.empty:


        df.loc[

            df["Status"]
            ==
            "Champion",

            "Status"

        ] = "Archived"






    df = pd.concat(

        [

            df,

            pd.DataFrame(
                [record]
            )

        ],

        ignore_index=True

    )




    df.to_csv(

        METRICS_FILE,

        index=False

    )




    print(
        "\nSaved:"
    )


    print(
        filename
    )



    print(
        "Status:",
        status
    )