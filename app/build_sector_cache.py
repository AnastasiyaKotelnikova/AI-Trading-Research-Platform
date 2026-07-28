import pandas as pd
import time

from app.sector_cache import load_sector_cache
from app.sector_provider import get_sector


INPUT_FILE = "data/cache/market_snapshot.csv"
CACHE_FILE = "data/cache/sector_cache.csv"


def build_cache():

    symbols_df = pd.read_csv(INPUT_FILE)

    cache = load_sector_cache()

    existing_symbols = set(
        cache["Symbol"]
    )

    print(
        f"Existing cached sectors: {len(existing_symbols)}"
    )

    added = 0

    for symbol in symbols_df["Symbol"]:

        if symbol in existing_symbols:
            continue

        try:

            sector = get_sector(symbol)

            new_row = pd.DataFrame(
                [{
                    "Symbol": symbol,
                    "Sector": sector
                }]
            )

            cache = pd.concat(
                [cache, new_row],
                ignore_index=True
            )

            cache.to_csv(
                CACHE_FILE,
                index=False
            )

            added += 1

            print(
                symbol,
                "->",
                sector
            )

            time.sleep(0.2)


        except Exception as e:

            print(
                symbol,
                "ERROR",
                e
            )


    print()
    print("Added sectors:", added)
    print("Cache size:", len(cache))


if __name__ == "__main__":
    build_cache()
