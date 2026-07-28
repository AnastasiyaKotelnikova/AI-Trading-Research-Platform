import os
import pandas as pd
from scipy.stats import ks_2samp


TRAINING_FILE = (
    "data/historical_ml_dataset.csv"
)

LIVE_FILE = (
    "data/models/model_predictions.csv"
)

REPORT_FILE = (
    "data/models/data_drift_report.csv"
)



FEATURES = [

    "Return_5D",

    "Return_20D",

    "RSI",

    "SMA20",

    "SMA50",

    "Volatility_20D",

    "ATR",

    "RVOL"

]



def calculate_drift(
    training,
    live
):

    results = []


    for feature in FEATURES:


        if (
            feature not in training.columns
            or
            feature not in live.columns
        ):

            continue



        train_values = (
            training[feature]
            .dropna()
        )


        live_values = (
            live[feature]
            .dropna()
        )



        if len(live_values) < 5:


            drift = None

            status = (
                "INSUFFICIENT_DATA"
            )


        else:


            statistic, p_value = ks_2samp(
                train_values,
                live_values
            )


            drift = round(
                statistic * 100,
                2
            )


            if p_value < 0.05:

                status = "DRIFT"

            else:

                status = "NORMAL"



        results.append({

            "Feature": feature,

            "Drift_%": drift,

            "Status": status

        })


    return pd.DataFrame(results)




def monitor_drift():


    print("\n================================")
    print("DATA DRIFT MONITOR")
    print("================================")



    if not os.path.exists(
        TRAINING_FILE
    ):

        print(
            "Training dataset missing"
        )

        return



    if not os.path.exists(
        LIVE_FILE
    ):

        print(
            "Live prediction file missing"
        )

        return



    training = pd.read_csv(
        TRAINING_FILE
    )


    live = pd.read_csv(
        LIVE_FILE
    )



    report = calculate_drift(
        training,
        live
    )



    print(report)



    os.makedirs(
        "data/models",
        exist_ok=True
    )



    report.to_csv(
        REPORT_FILE,
        index=False
    )



    print("\nSaved:")
    print(REPORT_FILE)



    if "DRIFT" in report["Status"].values:


        print("\nStatus:")
        print("WARNING")


        print(
            "\nRecommendation:"
        )

        print(
            "Investigate feature distribution changes."
        )


    else:


        print("\nStatus:")
        print("NORMAL")


        print(
            "\nRecommendation:"
        )

        print(
            "Continue monitoring."
        )





if __name__ == "__main__":

    monitor_drift()
