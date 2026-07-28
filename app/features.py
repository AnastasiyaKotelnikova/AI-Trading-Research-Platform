"""
Shared Feature Engineering Module

Used by:
- Historical feature builder
- Live scanner
- ML prediction pipeline
"""

import pandas as pd
import ta


# =========================
# FEATURES USED BY ML MODEL
# =========================

FEATURE_COLUMNS = [

    "Adjusted_Close",
    "Close",
    "High",
    "Low",
    "Open",
    "Volume",

    "Return_5D",
    "Return_10D",
    "Return_20D",

    "RSI",
    "RSI_Change",

    "SMA20",
    "SMA50",

    "Above_SMA20",
    "Above_SMA50",

    "SMA_Gap",

    "Momentum_Acceleration",

    "Average_Volume",
    "RVOL",

    "Volatility_20D",

    # New professional features
    "ATR",
    "ATR_Percent",

    "Range_Position",

    "Distance_From_52W_High",

    "Volume_Trend"

    "ATR",
    "ATR_Percent",
    "Range_Position",
    "Distance_From_52W_High",
    "Volume_Trend"
]


# =========================
# BUILD FEATURES
# =========================

def build_features(df):

    df = df.copy()


    # ---------------------
    # Data preparation
    # ---------------------

    df["Date"] = pd.to_datetime(
        df["Date"]
    )


    numeric_columns = [
        "Adjusted_Close",
        "Close",
        "High",
        "Low",
        "Open",
        "Volume"
    ]


    for col in numeric_columns:

        df[col] = pd.to_numeric(
            df[col],
            errors="coerce"
        )


    df = df.sort_values(
        "Date"
    )


    # ---------------------
    # Returns
    # ---------------------

    df["Return_5D"] = (
        df["Close"]
        .pct_change(5)
        * 100
    )


    df["Return_10D"] = (
        df["Close"]
        .pct_change(10)
        * 100
    )


    df["Return_20D"] = (
        df["Close"]
        .pct_change(20)
        * 100
    )


    # ---------------------
    # RSI
    # ---------------------

    df["RSI"] = ta.momentum.RSIIndicator(
        df["Close"],
        window=14
    ).rsi()


    df["RSI_Change"] = (
        df["RSI"]
        .diff()
    )


    # ---------------------
    # Moving averages
    # ---------------------

    df["SMA20"] = ta.trend.SMAIndicator(
        df["Close"],
        window=20
    ).sma_indicator()


    df["SMA50"] = ta.trend.SMAIndicator(
        df["Close"],
        window=50
    ).sma_indicator()



    df["Above_SMA20"] = (
        df["Close"] >
        df["SMA20"]
    ).astype(int)



    df["Above_SMA50"] = (
        df["Close"] >
        df["SMA50"]
    ).astype(int)



    df["SMA_Gap"] = (

        (
            df["SMA20"]
            -
            df["SMA50"]
        )

        /

        df["SMA50"]

        *

        100

    )


    # ---------------------
    # Momentum
    # ---------------------

    df["Momentum_Acceleration"] = (

        df["Return_5D"]

        -

        df["Return_20D"]

    )


    # ---------------------
    # Volume
    # ---------------------

    df["Average_Volume"] = (

        df["Volume"]
        .rolling(20)
        .mean()

    )


    df["RVOL"] = (

        df["Volume"]

        /

        df["Average_Volume"]

    )


    # ---------------------
    # Volatility
    # ---------------------

    df["Volatility_20D"] = (

        df["Close"]
        .pct_change()
        .rolling(20)
        .std()

        *

        100

    )


    # ---------------------
    # ATR Volatility Features
    # ---------------------

    df["ATR"] = ta.volatility.AverageTrueRange(

        high=df["High"],
        low=df["Low"],
        close=df["Close"],
        window=14

    ).average_true_range()



    df["ATR_Percent"] = (

        df["ATR"]

        /

        df["Close"]

        *

        100

    )


    # ---------------------
    # Price Range Position
    # ---------------------

    rolling_high = (

        df["High"]
        .rolling(20)
        .max()

    )


    rolling_low = (

        df["Low"]
        .rolling(20)
        .min()

    )


    df["Range_Position"] = (

        (df["Close"] - rolling_low)

        /

        (rolling_high - rolling_low)

    )



    # ---------------------
    # Distance From 52 Week High
    # ---------------------

    high_52w = (

        df["High"]
        .rolling(120)
        .max()

    )


    df["Distance_From_52W_High"] = (

        df["Close"]

        /

        high_52w

        -

        1

    ) * 100



    # ---------------------
    # Volume Trend
    # ---------------------

    df["Volume_Trend"] = (

        df["Volume"]
        .rolling(5)
        .mean()

        /

        df["Volume"]
        .rolling(20)
        .mean()

    )


    # ---------------------
    # ATR Features
    # ---------------------

    df["ATR"] = ta.volatility.AverageTrueRange(
        high=df["High"],
        low=df["Low"],
        close=df["Close"],
        window=14
    ).average_true_range()


    df["ATR_Percent"] = (

        df["ATR"]

        /

        df["Close"]

        *

        100

    )


    # ---------------------
    # Price Range Position
    # ---------------------

    rolling_high = (
        df["High"]
        .rolling(20)
        .max()
    )


    rolling_low = (
        df["Low"]
        .rolling(20)
        .min()
    )


    df["Range_Position"] = (

        (df["Close"] - rolling_low)

        /

        (rolling_high - rolling_low)

    )


    # ---------------------
    # Distance From 52 Week High
    # ---------------------

    high_52w = (
        df["High"]
        .rolling(252)
        .max()
    )


    df["Distance_From_52W_High"] = (

        df["Close"]

        /

        high_52w

        -

        1

    ) * 100


    # ---------------------
    # Volume Trend
    # ---------------------

    df["Volume_Trend"] = (

        df["Volume"]
        .rolling(5)
        .mean()

        /

        df["Volume"]
        .rolling(20)
        .mean()

    )

    return df
