import pandas as pd
import os


METRICS_FILE = "data/models/model_metrics.csv"

CHAMPION_FILE = "data/models/champion_model.pkl"



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


    def safe_float(value):

        if pd.isna(value):
            return 0.0

        return float(value)


    return {

        "F1":
            safe_float(
                champion.get("F1",0)
            ),

        "ROC_AUC":
            safe_float(
                champion.get("ROC_AUC",0)
            ),

        "Average_Return":
            safe_float(
                champion.get("Average_Return",0)
            ),

        "Win_Rate":
            safe_float(
                champion.get("Win_Rate",0)
            )

    }



def calculate_model_score(
    f1,
    roc_auc,
    average_return,
    win_rate
):

    return (

        (f1 * 0.20)

        +

        (roc_auc * 0.30)

        +

        (average_return * 0.30)

        +

        ((win_rate / 100) * 0.20)

    )



def evaluate_new_model(
    model_name,
    f1_score,
    average_return=None,
    win_rate=None,
    roc_auc=None
):


    champion = get_champion_metrics()


    if champion is None:

        print(
            "\nNo Champion Found"
        )

        return True



    if roc_auc is None:
        roc_auc = 0


    if average_return is None:
        average_return = 0


    if win_rate is None:
        win_rate = 0



    new_score = calculate_model_score(

        f1_score,

        roc_auc,

        average_return,

        win_rate

    )



    champion_score = calculate_model_score(

        champion["F1"],

        champion["ROC_AUC"],

        champion["Average_Return"],

        champion["Win_Rate"]

    )



    print(
        "\n===== MODEL COMPARISON ====="
    )


    print(
        "Champion Score:",
        round(champion_score,3)
    )


    print(
        "New Model Score:",
        round(new_score,3)
    )


    print(
        "\nChampion Metrics:"
    )

    print(champion)



    print(
        "\nNew Model Metrics:"
    )

    print({

        "F1": f1_score,

        "ROC_AUC": roc_auc,

        "Average_Return": average_return,

        "Win_Rate": win_rate

    })



    if new_score > champion_score:


        print(
            "\nNEW MODEL ACCEPTED"
        )

        return True



    else:


        print(
            "\nMODEL REJECTED"
        )

        return False