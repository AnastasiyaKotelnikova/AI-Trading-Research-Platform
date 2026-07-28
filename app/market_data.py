import pandas as pd
import time

from app.providers.finnhub import get_quote
from app.providers.yahoo import get_daily_data


INPUT_FILE = "data/universe/tradable_symbols.csv"
OUTPUT_FILE = "data/cache/market_snapshot.csv"


# Development mode
# Change to False later when we scan all stocks
TEST_MODE = False
TEST_SIZE = 50


def run_market_scan():

    df = pd.read_csv(INPUT_FILE)


    if TEST_MODE:

        symbols = df["Symbol"].head(TEST_SIZE).tolist()

    else:

        symbols = df["Symbol"].tolist()


    results = []


    print(f"Scanning {len(symbols)} symbols...")


    for i, symbol in enumerate(symbols, start=1):

        print(f"{i}/{len(symbols)} {symbol}")


        # -------------------------
        # Finnhub quote data
        # -------------------------

        quote = get_quote(symbol)


        if quote is None:
            continue



        # -------------------------
        # Yahoo historical data
        # Volume + RVOL
        # -------------------------

        daily = get_daily_data(symbol)



        if daily is not None:


            quote["Volume"] = daily["Volume"]

            quote["Average_Volume"] = daily["Average_Volume"]

            quote["RVOL"] = daily["RVOL"]

            quote["Yahoo_Close"] = daily["Yahoo_Close"]


        else:


            quote["Volume"] = None

            quote["Average_Volume"] = None

            quote["RVOL"] = None

            quote["Yahoo_Close"] = None



        # -------------------------
        # Dollar volume
        # -------------------------

        if (
            quote.get("Price") is not None
            and quote.get("Volume") is not None
        ):

            quote["Dollar_Volume"] = (
                quote["Price"] *
                quote["Volume"]
            )

        else:

            quote["Dollar_Volume"] = None



        results.append(quote)



        # Avoid API pressure

        time.sleep(0.4)



    output = pd.DataFrame(results)



    output.to_csv(
        OUTPUT_FILE,
        index=False
    )



    print("\nDONE")

    print(f"Saved: {OUTPUT_FILE}")



if __name__ == "__main__":

    run_market_scan()
