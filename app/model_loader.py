import os
import pandas as pd
import joblib


MODEL_FOLDER = "data/models"

METRICS_FILE = (
    "data/models/model_metrics.csv"
)


OPTIMIZED_MODEL = (
    "data/models/optimized_trading_model.pkl"
)



def get_best_model():

    # --------------------------------
    # 1. Prefer champion model system
    # --------------------------------

    if os.path.exists(METRICS_FILE):

        df = pd.read_csv(
            METRICS_FILE
        )


        if "Status" in df.columns:


            champions = df[
                df["Status"] == "Champion"
            ]


            if not champions.empty:

                best = champions.sort_values(
                    by="F1",
                    ascending=False
                ).iloc[0]


                model_file = (
                    f"{MODEL_FOLDER}/{best['Model']}.pkl"
                )


                if os.path.exists(model_file):

                    print(
                        "\nLoading Champion model:"
                    )

                    print(
                        model_file
                    )


                    return joblib.load(
                        model_file
                    )



    # --------------------------------
    # 2. Use optimized model fallback
    # --------------------------------

    if os.path.exists(OPTIMIZED_MODEL):


        print(
            "\nLoading Optimized model:"
        )

        print(
            OPTIMIZED_MODEL
        )


        return joblib.load(
            OPTIMIZED_MODEL
        )



    raise FileNotFoundError(
        "No valid trading model found."
    )





def get_best_model_info():


    # --------------------------------
    # Champion information
    # --------------------------------

    if os.path.exists(METRICS_FILE):


        df = pd.read_csv(
            METRICS_FILE
        )


        if (
            "Status" in df.columns
            and
            not df[df["Status"]=="Champion"].empty
        ):


            best = (
                df[df["Status"]=="Champion"]
                .sort_values(
                    by="F1",
                    ascending=False
                )
                .iloc[0]
            )


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

                "Status":
                    best["Status"],

                "Date":
                    best["Date"]

            }



    # --------------------------------
    # Optimized model info
    # --------------------------------


    optimization_file = (
        "data/models/model_optimization_results.csv"
    )


    if os.path.exists(optimization_file):


        df = pd.read_csv(
            optimization_file
        )


        best = df.sort_values(
            by="F1",
            ascending=False
        ).iloc[0]


        return {

            "Model":
                "optimized_trading_model",

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

            "Status":
                "Optimized",

            "Date":
                best["Date"]

        }



    return {

        "Model":
            "Unknown",

        "Accuracy":
            0,

        "F1":
            0,

        "Status":
            "Missing",

        "Date":
            None

    }