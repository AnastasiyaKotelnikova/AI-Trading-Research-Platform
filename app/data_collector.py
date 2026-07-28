"""
Historical Market Data Collector

Stores long-term stock price history
for future analysis and ML training.
"""

import os
from datetime import datetime
import pandas as pd

from app.providers.yahoo import get_history
from app.feature_engineering import add_features


INPUT_FILE = "data/cache/market_snapshot.csv"

OUTPUT_DIR = "data/market_history"


def collect_data():

    os.makedirs(
        OUTPUT_DIR,
        exist_ok=True
    )

    stocks = pd.read_csv(
        INPUT_FILE
    )

    print(
        f"Collecting data for {len(stocks)} stocks"
    )


    for _, row in stocks.iterrows():

        symbol = row["Symbol"]


        try:

            history = get_history(
                symbol,
                period="5y"
            )


            if history is None:

                print(
                    symbol,
                    "no data"
                )

                continue


            features = add_features(history)


            # Convert dictionary output to DataFrame
            if isinstance(features, dict):

                feature_df = pd.DataFrame(
                    [features]
                )

            else:

                feature_df = features.copy()


            feature_df["Symbol"] = symbol

            feature_df["Collected_Date"] = (
                datetime.now()
                .strftime("%Y-%m-%d")
            )


            filename = (
                f"{OUTPUT_DIR}/{symbol}_history.csv"
            )


            feature_df.to_csv(
                filename,
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
        "\nHistorical collection complete"
    )



if __name__ == "__main__":

    collect_data()
