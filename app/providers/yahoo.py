import pandas as pd
import yfinance as yf


def clean_columns(data):

    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    return data


def get_daily_data(symbol):

    try:

        data = yf.download(
            symbol,
            period="3mo",
            interval="1d",
            progress=False,
            auto_adjust=False
        )

        if data.empty:
            return None


        data = clean_columns(data)

        data = data.dropna()


        current_volume = int(
            data["Volume"].iloc[-1]
        )


        average_volume = int(
            data["Volume"].tail(50).mean()
        )


        close = float(
            data["Close"].iloc[-1]
        )


        rvol = round(
            current_volume / average_volume,
            2
        )


        return {
            "Symbol": symbol,
            "Volume": current_volume,
            "Average_Volume": average_volume,
            "RVOL": rvol,
            "Yahoo_Close": close
        }


    except Exception as e:

        print(
            f"Yahoo daily error {symbol}: {e}"
        )

        return None



def get_history(symbol, period="6mo"):

    try:

        data = yf.download(
            symbol,
            period=period,
            interval="1d",
            progress=False,
            auto_adjust=False
        )


        if data.empty:
            return None


        data = clean_columns(data)

        data = data.reset_index()


        data = data.rename(
            columns={
                "Adj Close": "Adjusted_Close"
            }
        )


        data = data.dropna()


        return data


    except Exception as e:

        print(
            f"Yahoo history error {symbol}: {e}"
        )

        return None