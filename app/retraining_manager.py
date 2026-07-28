import os
import pandas as pd
from datetime import datetime


METRICS_FILE = (
    "data/models/model_metrics.csv"
)

CHAMPION_STATUS = (
    "data/models/model_champion_status.csv"
)


MIN_NEW_TRADES = 500

MIN_WIN_RATE = 28

MIN_AVG_RETURN = 1.0

MAX_MODEL_AGE = 30


def should_retrain():

    print(
        "\n========== RETRAINING MANAGER ==========\n"
    )

    if (
        not os.path.exists(METRICS_FILE)
        or
        not os.path.exists(CHAMPION_STATUS)
    ):

        print(
            "Required files missing."
        )

        return False


    metrics = pd.read_csv(
        METRICS_FILE
    )

    status = pd.read_csv(
        CHAMPION_STATUS
    )


    champion = metrics[
        metrics["Status"] == "Champion"
    ]


    if champion.empty:

        print(
            "No champion model."
        )

        return True


    champion = champion.iloc[0]


    latest = (
        status
        .sort_values(
            "Evaluation_Date"
        )
        .iloc[-1]
    )


    model_date = pd.to_datetime(
        champion["Date"]
    )

    age = (
        datetime.now()
        -
        model_date
    ).days


    completed = latest[
        "Completed_Trades"
    ]

    win_rate = latest[
        "Win_Rate"
    ]

    average_return = latest[
        "Average_Return"
    ]


    print(
        "Champion:",
        champion["Model"]
    )

    print(
        "Age:",
        age,
        "days"
    )

    print(
        "Completed Trades:",
        completed
    )

    print(
        "Win Rate:",
        win_rate
    )

    print(
        "Average Return:",
        average_return
    )


    retrain = False


    if completed >= MIN_NEW_TRADES:

        print(
            "\nReason: Enough new trades."
        )

        retrain = True


    if win_rate < MIN_WIN_RATE:

        print(
            "Reason: Win rate declining."
        )

        retrain = True


    if average_return < MIN_AVG_RETURN:

        print(
            "Reason: Return declining."
        )

        retrain = True


    if age >= MAX_MODEL_AGE:

        print(
            "Reason: Model is old."
        )

        retrain = True


    if retrain:

        print(
            "\n>>> RETRAIN MODEL <<<"
        )

    else:

        print(
            "\nNo retraining needed."
        )


    return retrain


if __name__ == "__main__":

    should_retrain()