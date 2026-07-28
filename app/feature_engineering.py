import pandas as pd
import ta

from app.breakout import detect_breakout


def add_features(history):

    df = history.copy()


    # -----------------------------------
    # Data cleanup
    # -----------------------------------

    for col in [
        "Close",
        "High",
        "Low",
        "Volume"
    ]:

        df[col] = pd.to_numeric(
            df[col],
            errors="coerce"
        )


    # -----------------------------------
    # Returns
    # -----------------------------------

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



    # -----------------------------------
    # RSI
    # -----------------------------------

    df["RSI"] = ta.momentum.RSIIndicator(
        close=df["Close"],
        window=14
    ).rsi()


    df["RSI_Change"] = (
        df["RSI"]
        .diff()
    )



    # -----------------------------------
    # Moving averages
    # -----------------------------------

    df["SMA20"] = ta.trend.SMAIndicator(
        close=df["Close"],
        window=20
    ).sma_indicator()


    df["SMA50"] = ta.trend.SMAIndicator(
        close=df["Close"],
        window=50
    ).sma_indicator()


    # -----------------------------------
    # Long-term trend features
    # -----------------------------------

    df["SMA100"] = ta.trend.SMAIndicator(
        close=df["Close"],
        window=100
    ).sma_indicator()


    df["SMA200"] = ta.trend.SMAIndicator(
        close=df["Close"],
        window=200
    ).sma_indicator()


    df["Above_SMA100"] = (
        df["Close"] > df["SMA100"]
    )


    df["Above_SMA200"] = (
        df["Close"] > df["SMA200"]
    )


    df["Trend_Strength"] = (

        (df["Close"] - df["SMA200"])

        /

        df["SMA200"]

    ) * 100



    df["Above_SMA20"] = (
        df["Close"] > df["SMA20"]
    )


    df["Above_SMA50"] = (
        df["Close"] > df["SMA50"]
    )


    df["SMA_Gap"] = (

        (df["SMA20"] - df["SMA50"])

        /

        df["SMA50"]

    ) * 100



    # -----------------------------------
    # Momentum
    # -----------------------------------

    df["Momentum_Acceleration"] = (

        df["Return_5D"]

        -

        df["Return_20D"] / 4

    )



    # -----------------------------------
    # Volume
    # -----------------------------------

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


    df["Volume_Trend"] = (

        df["Volume"]
        .rolling(5)
        .mean()

        /

        df["Volume"]
        .rolling(20)
        .mean()

    )

    # -----------------------------------
    # Volume Acceleration
    # -----------------------------------

    df["Volume_Acceleration"] = (

        df["Volume"]
        .rolling(5)
        .mean()

        /

        df["Volume"]
        .rolling(50)
        .mean()

    )


    # Dollar volume needed by scanner

    df["Dollar_Volume"] = (

        df["Close"]

        *

        df["Volume"]

    )



    # -----------------------------------
    # Volatility
    # -----------------------------------

    df["Volatility_20D"] = (

        df["Close"]
        .pct_change()
        .rolling(20)
        .std()

        *

        100

    )


    # -----------------------------------
    # Risk adjusted return
    # -----------------------------------

    df["Return_to_Risk"] = (

        df["Return_20D"]

        /

        df["Volatility_20D"]

    )



    # -----------------------------------
    # ATR
    # -----------------------------------

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

    ) * 100



    # -----------------------------------
    # Range position
    # -----------------------------------

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


    # -----------------------------------
    # Drawdown features
    # -----------------------------------

    high_20 = (
        df["High"]
        .rolling(20)
        .max()
    )


    high_50 = (
        df["High"]
        .rolling(50)
        .max()
    )


    df["Drawdown_From_20D_High"] = (

        df["Close"]

        /

        high_20

        - 1

    ) * 100



    df["Drawdown_From_50D_High"] = (

        df["Close"]

        /

        high_50

        - 1

    ) * 100



    # -----------------------------------
    # 52 week high
    # -----------------------------------

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



    # -----------------------------------
    # Latest row
    # -----------------------------------

    latest = df.iloc[-1]



    # -----------------------------------
    # Overextended
    # -----------------------------------

    distance_from_sma20 = (

        latest["Close"]

        /

        latest["SMA20"]

        -

        1

    ) * 100



    overextended = (

        latest["Return_5D"] > 50

        or

        latest["RSI"] > 85

        or

        distance_from_sma20 > 20

    )



    # -----------------------------------
    # Output
    # -----------------------------------

    result = {


        "Close": round(float(latest["Close"]),2),

        "RSI": round(float(latest["RSI"]),2),

        "RSI_Change": round(float(latest["RSI_Change"]),2),

        "Return_5D": round(float(latest["Return_5D"]),2),

        "Return_10D": round(float(latest["Return_10D"]),2),

        "Return_20D": round(float(latest["Return_20D"]),2),


        "SMA20": round(float(latest["SMA20"]),2),

        "SMA50": round(float(latest["SMA50"]),2),


        "Above_SMA20": bool(latest["Above_SMA20"]),

        "Above_SMA50": bool(latest["Above_SMA50"]),


        "SMA_Gap": round(float(latest["SMA_Gap"]),2),


        "Momentum_Acceleration":
            round(float(latest["Momentum_Acceleration"]),2),


        "Volume":
            int(latest["Volume"]),


        "Average_Volume":
            round(float(latest["Average_Volume"]),2),


        "RVOL":
            round(float(latest["RVOL"]),2),


        "Dollar_Volume":
            round(float(latest["Dollar_Volume"]),2),


        "Volume_Trend":
            round(float(latest["Volume_Trend"]),2),

        "Volume_Acceleration":
            round(float(latest["Volume_Acceleration"]),2),


        "Volatility_20D":
            round(float(latest["Volatility_20D"]),2),


        "ATR":
            round(float(latest["ATR"]),2),


        "ATR_Percent":
            round(float(latest["ATR_Percent"]),2),


        "Range_Position":
            round(float(latest["Range_Position"]),2),


        "Distance_From_52W_High":
            round(float(latest["Distance_From_52W_High"]),2),


        "Overextended":
            overextended

    }



    # -----------------------------------
    # Breakout
    # -----------------------------------

    breakout = detect_breakout(history)


    if breakout:

        result["Breakout"] = breakout["Breakout"]

        result["Distance_From_High_%"] = breakout["Distance_%"]

    else:

        result["Breakout"] = False

        result["Distance_From_High_%"] = None



    return result
