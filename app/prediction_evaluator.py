import pandas as pd
import os
import datetime


PREDICTIONS_FILE = (
    "data/models/model_predictions.csv"
)

OUTPUT_FILE = (
    "data/models/prediction_evaluation_report.csv"
)

SUMMARY_FILE = (
    "data/models/prediction_summary.csv"
)


SUCCESS_THRESHOLD = 1.0
FAILED_THRESHOLD = -1.0



def load_predictions():

    if not os.path.exists(PREDICTIONS_FILE):

        raise FileNotFoundError(
            "Prediction file not found"
        )


    df = pd.read_csv(
        PREDICTIONS_FILE,
        low_memory=False
    )


    return df




def evaluate_predictions(df):


    print()
    print("=" * 60)
    print("PREDICTION EVALUATOR")
    print("=" * 60)


    print(
        "\nPrediction Records:",
        len(df)
    )


    # -------------------------------
    # Normalize columns
    # -------------------------------

    df["Return_5D"] = pd.to_numeric(
        df["Return_5D"],
        errors="coerce"
    )


    df["Date"] = pd.to_datetime(
        df["Date"],
        errors="coerce"
    )



    completed = df[
        df["Return_5D"].notna()
    ].copy()



    if completed.empty:

        print(
            "\nNo completed predictions yet"
        )

        return None



    print(
        "\nCompleted Before Cooldown:",
        len(completed)
    )



    # -------------------------------
    # Evaluate every completed prediction
    # No trade cooldown filtering
    # -------------------------------

    completed = completed.sort_values(
        [
            "Symbol",
            "Date"
        ]
    )


    print(
        "Completed Evaluated:",
        len(completed)
    )



    # -------------------------------
    # Classify outcomes
    # -------------------------------


    def classify(row):


        if row["Return_5D"] >= SUCCESS_THRESHOLD:

            return "SUCCESS"


        elif row["Return_5D"] <= FAILED_THRESHOLD:

            return "FAILED"


        else:

            return "NEUTRAL"




    completed["Prediction_Result"] = (

        completed.apply(
            classify,
            axis=1
        )

    )



    return completed





def create_summary(df, total_predictions):


    total = len(df)


    successful = (

        df["Prediction_Result"]
        .eq("SUCCESS")
        .sum()

    )


    failed = (

        df["Prediction_Result"]
        .eq("FAILED")
        .sum()

    )


    neutral = (

        df["Prediction_Result"]
        .eq("NEUTRAL")
        .sum()

    )



    directional = (
        successful
        +
        failed
    )



    summary = {


        "Evaluation_Date":
            datetime.datetime.now(),


        "Total_Predictions":
            total_predictions,


        "Completed_Evaluated":
            total,


        "Successful":
            successful,


        "Failed":
            failed,


        "Neutral":
            neutral,


        "Accuracy_%":

            round(

                successful
                /
                directional
                *
                100,

                2

            )

            if directional > 0

            else 0,



        "Directional_Trades":
            directional,


        "Neutral_Rate_%":

            round(

                neutral
                /
                total
                *
                100,

                2

            )

            if total > 0

            else 0,



        "Average_Return_5D":

            round(

                df["Return_5D"]
                .mean(),

                3

            ),



        "Average_Winner":

            round(

                df[
                    df["Return_5D"] > 0
                ]
                ["Return_5D"]
                .mean(),

                3

            )

            if len(
                df[
                    df["Return_5D"] > 0
                ]
            )

            else 0,



        "Average_Loser":

            round(

                df[
                    df["Return_5D"] < 0
                ]
                ["Return_5D"]
                .mean(),

                3

            )

            if len(
                df[
                    df["Return_5D"] < 0
                ]
            )

            else 0

    }



    return summary





def save_report(df, summary):


    os.makedirs(
        "data/models",
        exist_ok=True
    )


    df.to_csv(
        OUTPUT_FILE,
        index=False
    )


    pd.DataFrame(
        [summary]
    ).to_csv(
        SUMMARY_FILE,
        index=False
    )



    print()

    print(
        "Evaluation Saved:"
    )

    print(
        OUTPUT_FILE
    )


    print()

    print(
        "Summary Saved:"
    )

    print(
        SUMMARY_FILE
    )





def run_evaluator():


    predictions = load_predictions()


    evaluated = evaluate_predictions(
        predictions
    )



    if evaluated is None:

        return



    summary = create_summary(
        evaluated,
        len(predictions)
    )



    print()

    print(
        "===== SUMMARY ====="
    )


    for key, value in summary.items():

        print(
            key,
            ":",
            value
        )



    save_report(
        evaluated,
        summary
    )





if __name__ == "__main__":

    run_evaluator()