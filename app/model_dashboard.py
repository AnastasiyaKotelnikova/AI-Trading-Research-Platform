import os
import pandas as pd
from datetime import datetime


MODEL_METRICS = "data/models/model_metrics.csv"
MODEL_MONITORING = "data/models/model_monitoring.csv"
MODEL_PERFORMANCE = "data/models/model_predictions.csv"
DRIFT_REPORT = "data/models/data_drift_report.csv"



def load_csv(path):

    if os.path.exists(path):
        return pd.read_csv(path)

    return None



def champion_status():

    print("\n==================================================")
    print("CHAMPION MODEL")
    print("==================================================")


    df = load_csv(MODEL_METRICS)


    if df is None:
        print("No model metrics available")
        return


    champion = df[
        df["Status"] == "Champion"
    ]


    if len(champion) == 0:
        print("No champion model found")
        return


    row = champion.iloc[-1]


    print(
        "Model:",
        row["Model"]
    )

    print(
        "Accuracy:",
        round(row["Accuracy"],3)
    )

    print(
        "F1:",
        round(row["F1"],3)
    )

    print(
        "Precision:",
        row.get("Precision","N/A")
    )

    print(
        "Recall:",
        row.get("Recall","N/A")
    )



def live_predictions():

    print("\n==================================================")
    print("LIVE PREDICTIONS")
    print("==================================================")


    df = load_csv(
        MODEL_PERFORMANCE
    )


    if df is None:

        print(
            "No prediction data"
        )

        return


    total = len(df)


    completed = (
        df["Prediction_Result"]
        .notna()
        .sum()
    )


    pending = total - completed


    print(
        "Total Predictions:",
        total
    )


    print(
        "Completed:",
        completed
    )


    print(
        "Pending:",
        pending
    )


    if completed > 0:

        successful = (
            df[
                df["Prediction_Result"]
                ==
                "Successful"
            ]
        )


        win_rate = (
            len(successful)
            /
            completed
            *
            100
        )


        print(
            "Win Rate:",
            round(win_rate,2),
            "%"
        )

    else:

        print(
            "Win Rate: Pending"
        )



def latest_run():

    print("\n==================================================")
    print("LATEST MODEL RUN")
    print("==================================================")


    df = load_csv(
        MODEL_MONITORING
    )


    if df is None:

        print(
            "No monitoring data"
        )

        return


    row = df.iloc[-1]


    for col in [
        "Date",
        "Model",
        "Market_Regime",
        "Stocks_Scanned",
        "Average_ML_Probability",
        "Highest_ML_Probability"
    ]:

        if col in df.columns:

            print(
                col + ":",
                row[col]
            )



def drift_status():

    print("\n==================================================")
    print("DATA DRIFT")
    print("==================================================")


    df = load_csv(
        DRIFT_REPORT
    )


    if df is None:

        print(
            "No drift report"
        )

        return


    print(df)



def system_status():

    print("\n==================================================")
    print("SYSTEM HEALTH")
    print("==================================================")


    print(
        "STATUS: ONLINE"
    )


    print(
        """
Monitoring:
- Champion model
- Live predictions
- Performance tracking
- Data drift
- Retraining readiness
"""
    )


def main():

    print("\n==================================================")
    print("AI TRADING MODEL DASHBOARD")
    print("Generated:")
    print(datetime.now())
    print("==================================================")


    champion_status()

    live_predictions()

    latest_run()

    drift_status()

    system_status()



if __name__ == "__main__":

    main()
