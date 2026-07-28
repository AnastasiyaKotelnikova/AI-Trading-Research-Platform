import os
import pandas as pd
import yfinance as yf


def clean_columns(data):

    if isinstance(data.columns, pd.MultiIndex):

        data.columns = data.columns.get_level_values(0)

    return data



def get_history(symbol, period="5y"):


    safe_symbol = symbol

    # Windows reserved filename protection
    if symbol.upper() == "CON":

        safe_symbol = "_CON"


    cache_file = (
        f"data/cache/history/{safe_symbol}.csv"
    )


    try:


        # -------------------------
        # Use cache if it already
        # contains about 5 years
        # -------------------------

        if os.path.exists(cache_file):


            data = pd.read_csv(
                cache_file
            )


            data["Date"] = pd.to_datetime(
                data["Date"]
            )


            oldest = data["Date"].min()


            history_days = (
                pd.Timestamp.today()
                -
                oldest
            ).days


            if history_days >= 1700:

                return data


            print(
                f"{symbol}: Cache too short. Downloading full history..."
            )



        # -------------------------
        # Download from Yahoo
        # -------------------------

        data = yf.download(

            symbol,

            period=period,

            interval="1d",

            progress=False,

            auto_adjust=False

        )


        if data.empty:

            print(
                f"{symbol}: No data"
            )

            return None



        # Fix Yahoo multi-index columns

        data = clean_columns(
            data
        )


        data = data.reset_index()



        data = data.rename(

            columns={

                "Adj Close":
                "Adjusted_Close"

            }

        )


        data = data.dropna()



        # -------------------------
        # Save cache
        # -------------------------

        os.makedirs(

            "data/cache/history",

            exist_ok=True

        )


        data.to_csv(

            cache_file,

            index=False

        )


        print(

            f"{symbol}: downloaded {len(data)} rows"

        )


        return data



    except Exception as e:


        print(

            f"Yahoo history error {symbol}: {e}"

        )


        return None