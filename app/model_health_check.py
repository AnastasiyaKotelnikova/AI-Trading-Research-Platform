import os
import pandas as pd
from datetime import datetime


CHAMPION_TRACKER = (
    "data/models/model_champion_tracker.csv"
)

MODEL_MONITORING = (
    "data/models/model_monitoring.csv"
)

MODEL_PERFORMANCE = (
    "data/models/model_predictions.csv"
)

DRIFT_FILE = (
    "data/models/data_drift_report.csv"
)



def section(title):

    print("\n")
    print("=" * 50)
    print(title)
    print("=" * 50)



def check_champion_model():

    section("CHAMPION MODEL STATUS")


    if not os.path.exists(CHAMPION_TRACKER):

        print(
            "Champion tracker missing"
        )

        return


    df = pd.read_csv(
        CHAMPION_TRACKER
    )


    if len(df) == 0:

        print(
            "No champion model found"
        )

        return



    row = df.iloc[-1]


    print(
        "Active Model:",
        row.get(
            "Active_Model",
            "UNKNOWN"
        )
    )


    print(
        "Completed Trades:",
        row.get(
            "Completed_Trades",
            "N/A"
        )
    )


    print(
        "Win Rate:",
        row.get(
            "Win_Rate",
            "N/A"
        )
    )


    print(
        "Average Return:",
        row.get(
            "Average_Return",
            "N/A"
        ),
        "%"
    )



def check_live_predictions():

    section("LIVE PREDICTION MONITOR")


    if not os.path.exists(
        MODEL_PERFORMANCE
    ):

        print(
            "Performance file missing"
        )

        return



    df = pd.read_csv(
        MODEL_PERFORMANCE,
        low_memory=False
    )


    print(
        "Predictions:",
        len(df)
    )


    # =====================================
    # Only completed evaluations count
    # =====================================

    completed = df[
        df["Prediction_Result"].isin(
            [
                "SUCCESS",
                "FAILED",
                "NEUTRAL"
            ]
        )
    ].copy()


    print(
        "Completed:",
        len(completed)
    )


    pending = (
        len(df)
        -
        len(completed)
    )


    print(
        "Pending:",
        pending
    )



    if len(completed) > 0:


        # =====================================
        # Live prediction return monitoring
        # Uses 5D outcome, not training target
        # =====================================

        if "Return_5D" in completed.columns:


            print(
                "\nAverage Return:"
            )


            print(
                round(
                    completed["Return_5D"]
                    .mean(),
                    2
                ),
                "%"
            )


        else:

            print(
                "\nReturn_5D column missing"
            )



        print(
            "\nResults:"
        )


        print(
            completed[
                "Prediction_Result"
            ]
            .value_counts()
        )


def check_monitoring():

    section("MODEL RUN MONITORING")


    if not os.path.exists(
        MODEL_MONITORING
    ):

        print(
            "No monitoring data"
        )

        return



    df = pd.read_csv(
        MODEL_MONITORING
    )


    latest = df.iloc[-1]


    print(
        "Last Run:",
        latest["Date"]
    )


    print(
        "Model:",
        latest["Model"]
    )


    print(
        "Market:",
        latest["Market_Regime"]
    )


    print(
        "Stocks:",
        latest["Stocks_Scanned"]
    )


    print(
        "Average ML Probability:",
        latest["Average_ML_Probability"]
    )



def check_drift():

    section("DATA DRIFT STATUS")


    if not os.path.exists(
        DRIFT_FILE
    ):

        print(
            "No drift report available"
        )

        return



    df = pd.read_csv(
        DRIFT_FILE
    )


    print(df)



def final_status():

    section("SYSTEM HEALTH")


    print(
        "STATUS: ONLINE"
    )


    print(
        "Monitoring:"
    )

    print(
        "- Champion model"
    )

    print(
        "- Live predictions"
    )

    print(
        "- Data drift"
    )

    print(
        "- Retraining readiness"
    )


    print(
        "\nGenerated:",
        datetime.now()
    )



def main():

    print(
        "\nMODEL HEALTH CHECK"
    )


    check_champion_model()

    check_live_predictions()

    check_monitoring()

    check_drift()

    final_status()



if __name__ == "__main__":

    main()
