import os
import pandas as pd


PERFORMANCE_FILE = (
    "data/models/model_predictions.csv"
)


def generate_report():

    print("\n")
    print("=" * 50)
    print("MODEL LIVE PERFORMANCE REPORT")
    print("=" * 50)



    if not os.path.exists(
        PERFORMANCE_FILE
    ):

        print(
            "Performance file not found"
        )

        return



    df = pd.read_csv(
        PERFORMANCE_FILE
    )



    print("\nTotal Predictions:")
    print(
        len(df)
    )



    # -------------------------
    # Split completed / pending
    # -------------------------

    completed = df[
        df["Prediction_Result"].notna()
    ].copy()



    pending = df[
        df["Prediction_Result"].isna()
    ].copy()



    print("\nCompleted Predictions:")
    print(
        len(completed)
    )



    print("\nPending Predictions:")
    print(
        len(pending)
    )



    # -------------------------
    # Performance By Model
    # -------------------------

    if len(completed) > 0 and "Model" in completed.columns:


        print("\nPerformance by Model")
        print("--------------------")


        model_stats = (
            completed
            .groupby("Model")
            ["Prediction_Result"]
            .value_counts()
        )


        print(
            model_stats
        )



        print("\nModel Win Rate")
        print("----------------")


        for model in completed["Model"].unique():


            model_df = completed[
                completed["Model"] == model
            ]


            wins = len(
                model_df[
                    model_df["Prediction_Result"]
                    ==
                    "SUCCESS"
                ]
            )


            total = len(model_df)


            rate = (
                wins /
                total *
                100
            )


            print(
                model,
                ":",
                round(rate,2),
                "%"
            )



    # -------------------------
    # Overall Results
    # -------------------------

    if len(completed) > 0:


        print("\nPrediction Results")
        print("------------------")


        print(
            completed[
                "Prediction_Result"
            ]
            .value_counts()
        )



        successful = completed[
            completed["Prediction_Result"]
            ==
            "SUCCESS"
        ]


        win_rate = (

            len(successful)

            /

            len(completed)

            *

            100

        )



        print(
            "\nOverall Win Rate:"
        )


        print(
            round(win_rate,2),
            "%"
        )



        if "Return_5D" in completed.columns:

            print(
                "\nAverage 5D Return:"
        )


            print(
                round(
                    completed[
                        "Return_5D"
                    ]
                    .mean(),
                    2
                ),
                "%"
         )


    else:


        print(
            "\nNo completed predictions yet."
        )



    # -------------------------
    # Pending Predictions
    # -------------------------

    if len(pending) > 0:


        print("\nPending Predictions")
        print("-------------------")


        cols = [
            "Symbol",
            "ML_Probability",
            "AI_Final_Score"
        ]


        available = [
            c for c in cols
            if c in pending.columns
        ]


        print(
            pending[
                available
            ]
        )



    # -------------------------
    # ML Probability Analysis
    # -------------------------

    if (
        len(completed) > 0
        and "ML_Probability" in completed.columns
        and "Return_5D" in completed.columns
    ):


        print(
            "\nPerformance by ML Probability"
        )

        print(
            "-----------------------------"
        )


        print(

            completed
            .groupby(

                pd.cut(
                    completed["ML_Probability"],
                    bins=[
                        0,
                        10,
                        25,
                        50,
                        100
                    ]

                )

            )["Return_5D"]
            .mean()

        )



    # -------------------------
    # AI Score Analysis
    # -------------------------

    if (
        len(completed) > 0
        and "AI_Final_Score" in completed.columns
        and "Return_5D" in completed.columns
    ):


        print(
            "\nPerformance by AI Score"
        )

        print(
            "-----------------------"
        )


        print(

            completed
            .groupby(

                pd.cut(
                    completed["AI_Final_Score"],
                    bins=[
                        0,
                        30,
                        45,
                        60,
                        100
                    ]

                )

            )["Return_5D"]
            .mean()

        )



    print("\n")
    print("=" * 50)



if __name__ == "__main__":

    generate_report()