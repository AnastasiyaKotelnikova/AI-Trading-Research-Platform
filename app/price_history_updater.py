"""
Price History Incremental Updater

Updates existing OHLCV history files
without downloading everything again.
"""

import os
import pandas as pd

from app.providers.yahoo import get_history


INPUT_FILE = "data/cache/market_snapshot.csv"

HISTORY_DIR = "data/price_history"



def update_price_history():

    os.makedirs(
        HISTORY_DIR,
        exist_ok=True
    )


    stocks = pd.read_csv(
        INPUT_FILE
    )


    print(
        f"Updating {len(stocks)} stocks"
    )


    for _, row in stocks.iterrows():

        symbol = row["Symbol"]

        filename = (
            f"{HISTORY_DIR}/{symbol}_prices.csv"
        )


        try:

            new_data = get_history(
                symbol,
                period="5y"
            )


            if new_data is None or new_data.empty:

                print(
                    symbol,
                    "no data"
                )

                continue



            if os.path.exists(filename):

                old_data = pd.read_csv(
                    filename
                )


                combined = pd.concat(
                    [
                        old_data,
                        new_data
                    ],
                    ignore_index=True
                )


                # Normalize date format
                combined["Date"] = pd.to_datetime(
                    combined["Date"]
                )


                combined = combined.drop_duplicates(
                    subset=["Date"]
                )


                combined = combined.sort_values(
                    "Date"
                )
                
                
                combined["Date"] = combined["Date"].dt.strftime("%Y-%m-%d")

            else:

                combined = new_data



            combined.to_csv(
                filename,
                index=False
            )


            print(
                symbol,
                "updated",
                len(combined),
                "days"
            )


        except Exception as e:

            print(
                symbol,
                "ERROR:",
                e
            )


    print(
        "\nPrice history update complete"
    )



if __name__ == "__main__":

    update_price_history()
