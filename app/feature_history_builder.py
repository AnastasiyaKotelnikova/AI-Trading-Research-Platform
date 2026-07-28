"""
Feature History Builder

Creates historical ML-ready feature datasets
from stored price history.
"""


import os
import pandas as pd

from app.features import build_features

PRICE_DIR = "data/price_history"
FEATURE_DIR = "data/feature_history"



def create_feature_database():


    os.makedirs(
        FEATURE_DIR,
        exist_ok=True
    )


    files = os.listdir(
        PRICE_DIR
    )


    print(
        "Processing",
        len(files),
        "stocks"
    )


    for file in files:


        if not file.endswith("_prices.csv"):
            continue


        symbol = file.replace(
            "_prices.csv",
            ""
        )


        try:


            path = os.path.join(
                PRICE_DIR,
                file
            )


            history = pd.read_csv(
                path
            )


            # Generate full historical features
            features = build_features(
                history
            )


            output = os.path.join(
                FEATURE_DIR,
                f"{symbol}_features.csv"
            )


            features.to_csv(
                output,
                index=False
            )


            print(
                symbol,
                "saved"
            )


        except Exception as e:


            print(
                symbol,
                "ERROR:",
                e
            )


    print(
        "\nFeature database complete"
    )



if __name__ == "__main__":

    create_feature_database()
