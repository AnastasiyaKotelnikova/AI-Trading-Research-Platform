import os
import pandas as pd


METRICS_FILE = (
    "data/models/model_metrics.csv"
)


PERFORMANCE_FILE = (
    "data/models/model_predictions.csv"
)



MIN_COMPLETED_TRADES = 20



def load_metrics():

    if not os.path.exists(METRICS_FILE):

        return None


    return pd.read_csv(
        METRICS_FILE
    )



def get_champion(metrics):

    champions = metrics[
        metrics["Status"] == "Champion"
    ]


    if champions.empty:
        return None


    return champions.sort_values(
        "F1",
        ascending=False
    ).iloc[0]



def calculate_live_performance():


    if not os.path.exists(
        PERFORMANCE_FILE
    ):

        return None


    df = pd.read_csv(
        PERFORMANCE_FILE
    )


    completed = df[
        df["Prediction_Result"].notna()
    ]


    if len(completed) == 0:

        return {

            "Trades":0,

            "Win_Rate":0

        }



    wins = len(
        completed[
            completed["Prediction_Result"]
            ==
            "Successful"
        ]
    )


    return {

        "Trades":
            len(completed),

        "Win_Rate":
            round(
                wins / len(completed) * 100,
                2
            )

    }



def evaluate_models():


    print(
        "\n========== MODEL SELECTOR ==========\n"
    )


    metrics = load_metrics()


    if metrics is None:

        print(
            "No model metrics found"
        )

        return



    champion = get_champion(
        metrics
    )


    if champion is None:

        print(
            "No Champion model"
        )

        return



    print(
        "Current Champion:"
    )

    print(
        champion["Model"]
    )

    print(
        "F1:",
        champion["F1"]
    )



    live = calculate_live_performance()



    print(
        "\nLive Performance:"
    )

    print(
        live
    )



    print(
        "\nCandidates:"
    )


    candidates = metrics[
        metrics["Status"]=="Candidate"
    ]



    print(
        candidates[
            [
                "Model",
                "F1",
                "Status"
            ]
        ]
    )



    print(
        "\nSelection rule:"
    )

    print(
        "Candidate must beat Champion F1 and have enough live trades."
    )



if __name__ == "__main__":

    evaluate_models()
