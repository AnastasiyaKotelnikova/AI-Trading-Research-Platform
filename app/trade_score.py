import pandas as pd


def calculate_trade_score(df):

    df = df.copy()

    score = (

        df["Success_Probability"] * 60

        +

        (df["RVOL"] / 5).clip(0, 1) * 15

        +

        (df["ATR_Percent"] / 10).clip(0, 1) * 15

        +

        (df["Range_Position"]) * 10

    )

    df["Trade_Score"] = score.round(1)

    return dfcode 
