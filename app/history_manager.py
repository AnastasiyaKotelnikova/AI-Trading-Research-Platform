import os
from datetime import datetime


def save_history(df):

    os.makedirs(
        "data/history",
        exist_ok=True
    )

    filename = (
        "data/history/"
        + datetime.now().strftime("%Y-%m-%d_%H-%M")
        + "_integrated_results.csv"
    )

    df.to_csv(
        filename,
        index=False
    )

    print("Historical snapshot saved:")
    print(filename)
