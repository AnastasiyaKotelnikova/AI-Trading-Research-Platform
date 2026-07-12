import yfinance as yf


def get_history(symbol, days=120):

    try:

        df = yf.download(
            symbol,
            period=f"{days}d",
            interval="1d",
            progress=False
        )


        if df.empty:
            return None


        df = df.reset_index()


        df.columns = [
            col[0] if isinstance(col, tuple) else col
            for col in df.columns
        ]


        return df


    except Exception:

        return None