import yfinance as yf



def calculate_relative_strength(df):

    df = df.copy()

    try:

        spy = yf.download(
            "SPY",
            period="3mo",
            interval="1d",
            progress=False,
            auto_adjust=False
        )


        if spy.empty:
            df["Relative_Strength"] = 0
            return df


        # Handle Yahoo MultiIndex columns
        if hasattr(spy.columns, "levels"):

            spy_close = spy["Close"]["SPY"]

        else:

            spy_close = spy["Close"]


        if len(spy_close) < 21:
            df["Relative_Strength"] = 0
            return df


        spy_return = (
            (spy_close.iloc[-1] -
             spy_close.iloc[-21])
            /
            spy_close.iloc[-21]
            * 100
        )


        df["Relative_Strength"] = (
            df["Return_20D"]
            -
            spy_return
        )


    except Exception as e:

        print("Relative Strength Error:", e)

        df["Relative_Strength"] = 0


    return df
