import os
import pandas as pd
from datetime import datetime


METRICS_FILE = (
    "data/models/model_metrics.csv"
)

PERFORMANCE_FILE = (
    "data/models/model_predictions.csv"
)

DATASET_FILE = (
    "data/historical_ml_dataset.csv"
)


# ---------------------------------------
# Thresholds
# ---------------------------------------

MIN_WIN_RATE = 55

MIN_TRADES = 50

MAX_MODEL_AGE_DAYS = 30


# ---------------------------------------
# Live Performance
# ---------------------------------------

def check_live_performance():

    if not os.path.exists(
        PERFORMANCE_FILE
    ):

        return {
            "status": "NO_DATA"
        }

    df = pd.read_csv(
        PERFORMANCE_FILE
    )

    completed = df[
        df["Prediction_Result"].notna()
    ]

    if len(completed) < MIN_TRADES:

        return {

            "status":
                "INSUFFICIENT_DATA",

            "trades":
                len(completed)

        }

    wins = len(

        completed[
            completed["Prediction_Result"]
            ==
            "Successful"
        ]

    )

    win_rate = (

        wins
        /
        len(completed)
        *
        100

    )

    return {

        "status":

            "OK"

            if win_rate >= MIN_WIN_RATE

            else

            "RETRAIN",

        "trades":
            len(completed),

        "win_rate":
            round(
                win_rate,
                2
            )

    }


# ---------------------------------------
# Champion Model Age
# ---------------------------------------

def check_model_age():

    if not os.path.exists(
        METRICS_FILE
    ):

        return None

    df = pd.read_csv(
        METRICS_FILE
    )

    champion = df[
        df["Status"]
        ==
        "Champion"
    ]

    if champion.empty:
        return None

    date = pd.to_datetime(
        champion.iloc[-1]["Date"]
    )

    age = (

        datetime.now()
        -
        date

    ).days

    return age


# ---------------------------------------
# Dataset Size
# ---------------------------------------

def check_dataset_growth():

    if not os.path.exists(
        DATASET_FILE
    ):

        return None

    df = pd.read_csv(
        DATASET_FILE
    )

    return len(df)


# ---------------------------------------
# Evaluation
# ---------------------------------------

def evaluate_retraining():

    print(
        "\n================================"
    )

    print(
        "RETRAINING TRIGGER CHECK"
    )

    print(
        "================================"
    )

    performance = check_live_performance()

    print(
        "\nLive Performance:"
    )

    print(
        performance
    )

    age = check_model_age()

    print(
        "\nChampion Age:"
    )

    print(
        age,
        "days"
    )

    records = check_dataset_growth()

    print(
        "\nTraining Records:"
    )

    print(
        records
    )

    retrain = False

    if performance.get(
        "status"
    ) == "RETRAIN":

        retrain = True

    if age is not None:

        if age > MAX_MODEL_AGE_DAYS:

            retrain = True

    print("\nDecision:")

    if retrain:

        print(
            "RETRAIN MODEL"
        )

        return "RETRAIN"

    print(
        "KEEP CURRENT MODEL"
    )

    return "KEEP"


# ---------------------------------------
# Public API
# ---------------------------------------

def check_retraining_needed():
    """
    Used by the automatic retraining pipeline.

    Returns:
        KEEP
        RETRAIN
    """

    return evaluate_retraining()


# ---------------------------------------
# Main
# ---------------------------------------

if __name__ == "__main__":

    evaluate_retraining()
