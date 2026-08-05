from app.model_loader import get_best_model_info
import pandas as pd

METRICS_FILE = "data/models/model_metrics.csv"


def get_current_model_info():

    champion = get_best_model_info()

    metrics = pd.read_csv(METRICS_FILE)

    row = metrics[
        metrics["Model"] == champion["Model"]
    ]

    if not row.empty:

        row = row.iloc[0]

        champion["Accuracy"] = round(
            row["Accuracy"] * 100,
            2
        )

        champion["F1"] = round(
            row["F1"] * 100,
            2
        )

        champion["Precision"] = round(
            row["Precision"] * 100,
            2
        )

        champion["Recall"] = round(
            row["Recall"] * 100,
            2
        )

        champion["ROC_AUC"] = round(
            row["ROC_AUC"] * 100,
            2
        )

        champion["Training_Date"] = row["Date"]

    return champion