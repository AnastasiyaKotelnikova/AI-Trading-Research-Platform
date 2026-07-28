import pandas as pd
import os
import datetime


PREDICTIONS_FILE = "data/models/model_predictions.csv"


OUTPUT_FILE = "data/models/prediction_evaluation_report.csv"



def load_predictions():

    if not os.path.exists(PREDICTIONS_FILE):

        raise FileNotFoundError(
            "Prediction file not found"
        )


    df = pd.read_csv(
        PREDICTIONS_FILE
    )


    return df



def evaluate_predictions(df):


    print("\n")
    print("=" * 60)
    print("PREDICTION EVALUATOR")
    print("=" * 60)



    print("\nPrediction Records:")
    print(len(df))



    completed = df[
        df["Return_20D"].notna()
    ].copy()



    if len(completed) == 0:

        print("\nNo completed predictions yet")
        return None



    print("\nCompleted Predictions:")
    print(len(completed))



    def classify(row):

        if row["Return_20D"] >= 5:

            return "SUCCESS"


        elif row["Return_20D"] <= -5:

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



def create_summary(df):


    summary = {


        "Evaluation_Date":
            datetime.datetime.now(),


        "Total_Evaluated":
            len(df),


        "Successful":
            len(
                df[
                    df["Prediction_Result"]
                    ==
                    "SUCCESS"
                ]
            ),


        "Failed":
            len(
                df[
                    df["Prediction_Result"]
                    ==
                    "FAILED"
                ]
            ),


        "Neutral":
            len(
                df[
                    df["Prediction_Result"]
                    ==
                    "NEUTRAL"
                ]
            )

    }



    if summary["Total_Evaluated"] > 0:

        summary["Accuracy_%"] = round(

            (
                summary["Successful"]
                /
                summary["Total_Evaluated"]

            )
            *
            100,

            2
        )


    else:

        summary["Accuracy_%"] = 0



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


    summary_file = (
        "data/models/prediction_summary.csv"
    )


    pd.DataFrame(
        [summary]
    ).to_csv(
        summary_file,
        index=False
    )



    print("\nEvaluation Saved:")
    print(
        OUTPUT_FILE
    )


    print("\nSummary Saved:")
    print(
        summary_file
    )



def run_evaluator():


    predictions = load_predictions()


    evaluated = evaluate_predictions(
        predictions
    )


    if evaluated is None:

        return



    summary = create_summary(
        evaluated
    )


    print("\n===== SUMMARY =====")


    for k,v in summary.items():

        print(
            k,
            ":",
            v
        )


    save_report(
        evaluated,
        summary
    )



if __name__ == "__main__":

    run_evaluator()