import os
import pandas as pd


METRICS_FILE = (
    "data/models/model_metrics.csv"
)

PERFORMANCE_FILE = (
    "data/models/model_predictions.csv"
)


MIN_COMPLETED_TRADES = 20


MIN_WIN_RATE = 70


def evaluate_live_performance(model):


    if not os.path.exists(
        PERFORMANCE_FILE
    ):
        return None



    df = pd.read_csv(
        PERFORMANCE_FILE
    )



    df = df[
        df["Model"] == model
    ]



    if df.empty:
        return None



    completed = df[
        df["Prediction_Result"].isin(
            [
                "SUCCESS",
                "FAILED"
            ]
        )
    ]



    if len(completed) == 0:

        return {

            "Trades":0,

            "Win_Rate":0,

            "Average_Return":0

        }



    wins = completed[
        completed["Prediction_Result"]
        ==
        "SUCCESS"
    ]



    avg_return = None


    if "Return_5D" in completed.columns:

        avg_return = round(
            completed["Return_5D"]
            .mean(),
            2
        )



    return {


        "Trades":
            len(completed),


        "Win_Rate":
            round(
                len(wins)
                /
                len(completed)
                *
                100,
                2
            ),


        "Average_Return_5D":
            avg_return

    }





def get_current_champion():


    if not os.path.exists(
        METRICS_FILE
    ):
        return None



    df = pd.read_csv(
        METRICS_FILE
    )



    champions = df[
        df["Status"]
        ==
        "Champion"
    ]



    if champions.empty:

        return None



    return champions.iloc[-1]





def evaluate_champion():



    print()

    print("=" * 50)

    print(
        "MODEL RETRAINING DECISION SYSTEM"
    )

    print("=" * 50)



    champion = get_current_champion()



    if champion is None:

        print(
            "No champion model found"
        )

        return



    model_name = champion["Model"]



    print()

    print(
        "Current Champion:",
        model_name
    )


    print(
        "Validation F1:",
        champion["F1"]
    )



    live = evaluate_live_performance(
        model_name
    )



    if live is None:

        print(
            "No live performance data"
        )

        return



    print()

    print(
        "Live Performance:"
    )

    print(
        live
    )



    print()

    print(
        "Retraining Decision:"
    )



    if live["Trades"] < MIN_COMPLETED_TRADES:


        print(
            "WAIT - Not enough trades"
        )


    elif live["Win_Rate"] < MIN_WIN_RATE:


        print(
            "RETRAIN RECOMMENDED"
        )

        print(
            "Reason: Live performance dropped"
        )


    else:


        print(
            "KEEP CURRENT CHAMPION"
        )

        print(
            "Model performance is acceptable"
        )





if __name__ == "__main__":

    evaluate_champion()