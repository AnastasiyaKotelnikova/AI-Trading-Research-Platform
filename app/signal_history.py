import os
from datetime import datetime
from app.model_info import get_current_model_info


def save_signal_history(df):

    os.makedirs(
        "data/signal_history",
        exist_ok=True
    )


    # ===============================
    # Attach Model Lineage
    # ===============================

    model_info = get_current_model_info()


    df["Model_Name"] = (
        model_info["Model"]
    )

    df["Model_Accuracy"] = (
        model_info["Accuracy"]
    )

    df["Model_F1"] = (
        model_info["F1"]
    )

    df["Model_Date"] = (
        model_info["Date"]
    )


    filename = (
        "data/signal_history/"
        + datetime.now().strftime("%Y-%m-%d_%H-%M")
        + "_signals.csv"
    )


    df.to_csv(
        filename,
        index=False
    )


    print("\nSignal history saved:")
    print(filename)
