import os
import pandas as pd

from app.sector_provider import get_sector


CACHE_FILE = "data/cache/sector_cache.csv"


def load_sector_cache():

    if os.path.exists(CACHE_FILE):

        return pd.read_csv(CACHE_FILE)

    return pd.DataFrame(
        columns=["Symbol", "Sector"]
    )


def get_sector_cached(symbol):

    cache = load_sector_cache()

    existing = cache[
        cache["Symbol"] == symbol
    ]

    if not existing.empty:

        return existing.iloc[0]["Sector"]


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


    return sector
