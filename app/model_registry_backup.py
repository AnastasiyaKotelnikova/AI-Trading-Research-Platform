import pandas as pd
import os


METRICS_FILE = "data/models/model_metrics.csv"

CHAMPION_FILE = "data/models/champion_model.pkl"



def get_champion_score():

    if not os.path.exists(CHAMPION_FILE):
        return 0

    if not os.path.exists(METRICS_FILE):
        return 0


    df = pd.read_csv(
        METRICS_FILE
    )


    champions = df[
        df["Status"] == "Champion"
    ]


    if len(champions) == 0:
        return 0


    champions = champions[
        champions["F1"] < 0.95
    ]


    if len(champions) == 0:
        return 0


    champion = champions.iloc[-1]


    return float(
        champion["F1"]
    )



def get_champion_metrics():

    if not os.path.exists(METRICS_FILE):
        return None


    df = pd.read_csv(
        METRICS_FILE
    )


    champions = df[
        df["Status"] == "Champion"
    ]


    if len(champions) == 0:
        return None


    champion = champions.iloc[-1]


    return {

        "F1": champion["F1"],

        "Average_Return":
            champion.get(
                "Average_Return",
                0
            ),

        "Win_Rate":
            champion.get(
                "Win_Rate",
                0
            )
    }




def evaluate_new_model(
    model_name,
    f1_score,
    average_return=None,
    win_rate=None
):


    champion = get_champion_metrics()


    if champion is None:

        print(
            "\nNo Champion Found"
        )

        return True



    print(
        "\n===== MODEL COMPARISON ====="
    )


    print(
        "Champion F1:",
        round(float(champion["F1"]),3)
    )


    print(
        "New Model F1:",
        round(f1_score,3)
    )


    if average_return is not None:

        print(
            "Champion Avg Return:",
            round(
                float(champion["Average_Return"]),
                3
            )
        )

        print(
            "New Model Avg Return:",
            round(
                average_return,
                3
            )
        )



    # Phase 3.5 acceptance logic

    f1_improved = (
        f1_score > champion["F1"]
    )


    trading_improved = True


    if average_return is not None:

        trading_improved = (
            average_return >= champion["Average_Return"]
        )



    if f1_improved and trading_improved:


        print(
            "\nNEW MODEL ACCEPTED"
        )


        return True



    else:


        print(
            "\nMODEL REJECTED"
        )


        return False