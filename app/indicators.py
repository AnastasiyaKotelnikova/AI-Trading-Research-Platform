import pandas as pd
import ta


def add_indicators(df):

    df = df.copy()

    # RSI
    df["RSI"] = ta.momentum.RSIIndicator(
        close=df["Close"],
        window=14
    ).rsi()


    # EMA 20
    df["EMA20"] = ta.trend.EMAIndicator(
        close=df["Close"],
        window=20
    ).ema_indicator()


    # EMA 50
    df["EMA50"] = ta.trend.EMAIndicator(
        close=df["Close"],
        window=50
    ).ema_indicator()


    # Trend signal

    df["Trend"] = "Neutral"


    df.loc[
        (df["Close"] > df["EMA20"]) &
        (df["EMA20"] > df["EMA50"]),
        "Trend"
    ] = "Bullish"


    return df