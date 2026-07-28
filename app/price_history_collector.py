"""
Fast Historical Price Collector
"""

import os
import pandas as pd

from concurrent.futures import ThreadPoolExecutor

from app.providers.yahoo import get_history


INPUT_FILE = "data/cache/market_snapshot.csv"

OUTPUT_DIR = "data/price_history"


def download_stock(symbol):

    try:

        filename = (
            f"{OUTPUT_DIR}/{symbol}_prices.csv"
        )


        # Check existing history
        if os.path.exists(filename):

            old = pd.read_csv(filename)

            if len(old) >= 1200:

                return (
                    symbol,
                    f"SKIPPED {len(old)} rows"
                )


        # Download full history

        history = get_history(
            symbol,
            period="5y"
        )


        if history is None:

            return (
                symbol,
                "NO DATA"
            )


        history.to_csv(
            filename,
            index=False
        )


        return (
            symbol,
            f"DOWNLOADED {len(history)} rows"
        )


    except Exception as e:

        return (
            symbol,
            str(e)
        )



def collect_price_history():

    os.makedirs(
        OUTPUT_DIR,
        exist_ok=True
    )


    stocks = pd.read_csv(
        INPUT_FILE
    )


    symbols = stocks["Symbol"].tolist()


    print(
        f"Downloading {len(symbols)} stocks"
    )


    with ThreadPoolExecutor(
        max_workers=10
    ) as executor:


        results = executor.map(
            download_stock,
            symbols
        )


        for symbol, result in results:

            print(
                symbol,
                result
            )


    print(
        "\nCOMPLETE"
    )



if __name__ == "__main__":

    collect_price_history()
