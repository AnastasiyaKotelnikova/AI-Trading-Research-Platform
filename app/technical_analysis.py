import pandas as pd
import ta


def calculate_technical_indicators(history):

    df = history.copy()


    # Make sure Close is numeric
    df["Close"] = pd.to_numeric(
        df["Close"],
        errors="coerce"
    )


    # RSI
    df["RSI"] = ta.momentum.RSIIndicator(
        close=df["Close"],
        window=14
    ).rsi()


    # EMA
    df["EMA20"] = ta.trend.EMAIndicator(
        close=df["Close"],
        window=20
    ).ema_indicator()


    df["EMA50"] = ta.trend.EMAIndicator(
        close=df["Close"],
        window=50
    ).ema_indicator()


    # Current values

    latest = df.iloc[-1]


    result = {

        "RSI": float(
            round(
                latest["RSI"],
                2
            )
        ),

        "EMA20": float(
            round(
                latest["EMA20"],
                2
            )
        ),

        "EMA50": float(
            round(
                latest["EMA50"],
                2
            )
        ),

        "Close": float(
            round(
                latest["Close"],
                2
            )
        )

    }


    # Trend

    if (
        latest["Close"] >
        latest["EMA20"]
        and
        latest["EMA20"] >
        latest["EMA50"]
    ):

        result["Trend"] = "Bullish"

    else:

        result["Trend"] = "Neutral"


    return result