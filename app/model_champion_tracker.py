import os
import pandas as pd
from datetime import datetime


FEEDBACK_FILE = (
    "data/models/model_feedback_report.csv"
)

METRICS_FILE = (
    "data/models/model_metrics.csv"
)

RECOMMENDED_MODEL_FILE = (
    "data/models/recommended_champion.txt"
)

MODEL_STATUS_FILE = (
    "data/models/model_champion_status.csv"
)



def update_champion_status():


    print(
        "\n========== MODEL CHAMPION TRACKER ==========\n"
    )


    if not os.path.exists(FEEDBACK_FILE):

        print(
            "No feedback report found"
        )

        return



    feedback = pd.read_csv(
        FEEDBACK_FILE
    )


    latest = feedback.iloc[-1]



    if not os.path.exists(METRICS_FILE):

        raise FileNotFoundError(
            f"{METRICS_FILE} not found"
        )



    metrics = pd.read_csv(
        METRICS_FILE
    )



    # =========================================
    # LOAD RECOMMENDED MODEL FROM EVALUATOR
    # =========================================


    if not os.path.exists(
        RECOMMENDED_MODEL_FILE
    ):

        raise FileNotFoundError(
            "recommended_champion.txt missing. Run model_quality_evaluator first."
        )



    with open(
        RECOMMENDED_MODEL_FILE,
        "r"
    ) as f:

        active_model = f.read().strip()



    print(
        "Recommended Champion:",
        active_model
    )



    # =========================================
    # GET MODEL METRICS
    # =========================================


    model_row = metrics[
        metrics["Model"] == active_model
    ]



    if model_row.empty:

        raise RuntimeError(
            f"{active_model} not found in model_metrics.csv"
        )



    model_row = model_row.iloc[0]



    status = pd.DataFrame([{

        "Evaluation_Date":
            datetime.now(),


        "Model":
            active_model,


        "Active_Model":
            active_model,


        "Accuracy":
            model_row["Accuracy"],


        "F1":
            model_row["F1"],


        "Completed_Trades":
            latest.get(
                "Completed_Trades",
                0
            ),


        "Win_Rate":
            latest.get(
                "Win_Rate",
                0
            ),


        "Average_Return":
            latest.get(
                "Average_Return",
                0
            ),


        "Status":
            "CHAMPION"

    }])



    status.to_csv(
        MODEL_STATUS_FILE,
        index=False
    )



    print(
        "\nChampion status saved:"
    )

    print(
        MODEL_STATUS_FILE
    )


    print(
        "\nCURRENT MODEL:"
    )

    print(
        status
    )




if __name__ == "__main__":

    update_champion_status()