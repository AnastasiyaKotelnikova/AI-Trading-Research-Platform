import pandas as pd
import os
import glob


PREDICTIONS_FILE = "data/models/model_predictions.csv"

FORWARD_TEST_FOLDER = "data/backtest_results"

OUTPUT_FILE = "data/models/ml_reality_report.csv"



def reality_check():

    print("\n")
    print("=" * 60)
    print("ML REALITY CHECK")
    print("=" * 60)



    predictions = pd.read_csv(
        PREDICTIONS_FILE,
        low_memory=False
    )



    files = glob.glob(
        FORWARD_TEST_FOLDER + "/forward_test_*.csv"
    )


    if len(files) == 0:

        print(
            "No forward tests found"
        )

        return



    latest_forward = max(
        files,
        key=os.path.getmtime
    )



    forward = pd.read_csv(
        latest_forward,
        low_memory=False
    )



    print("\nPrediction Records:")
    print(len(predictions))


    print("\nForward Test:")
    print(latest_forward)


    print(
        "\nForward Records:"
    )

    print(
        len(forward)
    )



    latest_date = predictions["Date"].max()


    latest_predictions = predictions[
        predictions["Date"] == latest_date
    ].copy()



    merged = latest_predictions.merge(
        forward,
        on="Symbol",
        how="inner"
    )



    print("\nMatched Predictions:")
    print(len(merged))



    if len(merged)==0:

        print(
            "No matches yet"
        )

        return



    report = merged[
        [
            "Symbol",
            "ML_Probability",
            "AI_Final_Score",
            "Return_%",
            "Result"
        ]
    ].copy()



    print("\nReality Results:")

    print(
        report
    )



    print("\nProbability Groups:")


    report["Probability_Group"] = pd.cut(
        report["ML_Probability"],
        bins=[
            0,
            10,
            20,
            30,
            100
        ],
        labels=[
            "0-10",
            "10-20",
            "20-30",
            "30+"
        ]
    )



    summary = report.groupby(
        "Probability_Group",
        observed=False
    )["Return_%"].agg(
        [
            "count",
            "mean"
        ]
    )


    print(summary)



    report.to_csv(
        OUTPUT_FILE,
        index=False
    )


    print("\nSaved:")
    print(
        OUTPUT_FILE
    )



if __name__ == "__main__":

    reality_check()