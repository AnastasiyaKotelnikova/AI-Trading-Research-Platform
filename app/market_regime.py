import pandas as pd
import ta


def get_market_regime(history):

    df = history.copy()

    df["Close"] = pd.to_numeric(
        df["Close"],
        errors="coerce"
    )


    sma50 = ta.trend.SMAIndicator(
        close=df["Close"],
        window=50
    ).sma_indicator()


    sma200 = ta.trend.SMAIndicator(
        close=df["Close"],
        window=200
    ).sma_indicator()


    close = df["Close"].iloc[-1]

    sma50_value = sma50.iloc[-1]

    sma200_value = sma200.iloc[-1]


    if close > sma50_value and close > sma200_value:

        return {
            "Regime": "Bullish",
            "Score": 2
        }


    elif close > sma50_value:

        return {
            "Regime": "Neutral",
            "Score": 1
        }


    else:

        return {
            "Regime": "Bearish",
            "Score": 0
        }
