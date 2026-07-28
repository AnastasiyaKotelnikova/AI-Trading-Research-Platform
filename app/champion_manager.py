import os
import shutil
import pandas as pd


MODEL_FOLDER = "data/models"

QUALITY_FILE = (
    "data/models/model_quality_report.csv"
)

METRICS_FILE = (
    "data/models/model_metrics.csv"
)

CHAMPION_MODEL = (
    "data/models/champion_model.pkl"
)


def promote_best_model():

    print("\n========== CHAMPION MANAGER ==========\n")

    if not os.path.exists(QUALITY_FILE):

        print("No quality report found")
        return

    quality = pd.read_csv(
        QUALITY_FILE
    )

    metrics = pd.read_csv(
        METRICS_FILE
    )

    best = quality.sort_values(
        "Trading_Quality_Score",
        ascending=False
    ).iloc[0]

    best_model = best["Model"]

    print(
        "Best model:",
        best_model
    )

    current = metrics[
        metrics["Status"] == "Champion"
    ]

    if len(current) > 0:

        current_model = current.iloc[0]["Model"]

    else:

        current_model = None

    print(
        "Current champion:",
        current_model
    )

    if best_model == current_model:

        print(
            "\nChampion unchanged."
        )

        return

    metrics.loc[
        metrics["Status"] == "Champion",
        "Status"
    ] = "Archived"

    metrics.loc[
        metrics["Model"] == best_model,
        "Status"
    ] = "Champion"

    metrics.to_csv(
        METRICS_FILE,
        index=False
    )

    source = (
        f"{MODEL_FOLDER}/{best_model}.pkl"
    )

    if os.path.exists(source):

        shutil.copy2(
            source,
            CHAMPION_MODEL
        )

        print(
            "\nChampion model updated."
        )

    else:

        print(
            "\nModel file missing."
        )

    print(
        "\nNew Champion:",
        best_model
    )


if __name__ == "__main__":

    promote_best_model()