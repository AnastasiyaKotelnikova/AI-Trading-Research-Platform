import pandas as pd


def calculate_scores(df):

    df = df.copy()

    df["Scanner_Score"] = 0


    # =========================
    # Momentum (0-25)
    # =========================

    df.loc[
        df["Change_%"] >= 10,
        "Scanner_Score"
    ] += 25

    df.loc[
        (df["Change_%"] >= 5) &
        (df["Change_%"] < 10),
        "Scanner_Score"
    ] += 15

    df.loc[
        (df["Change_%"] >= 2) &
        (df["Change_%"] < 5),
        "Scanner_Score"
    ] += 5



    # =========================
    # Relative Strength (0-20)
    # =========================

    df.loc[
        df["Relative_Strength"] >= 20,
        "Scanner_Score"
    ] += 20

    df.loc[
        (df["Relative_Strength"] >= 10) &
        (df["Relative_Strength"] < 20),
        "Scanner_Score"
    ] += 15

    df.loc[
        (df["Relative_Strength"] >= 5) &
        (df["Relative_Strength"] < 10),
        "Scanner_Score"
    ] += 10

    df.loc[
        (df["Relative_Strength"] >= 0) &
        (df["Relative_Strength"] < 5),
        "Scanner_Score"
    ] += 5



    # =========================
    # Volume Confirmation (0-15)
    # =========================

    df.loc[
        df["RVOL"] >= 5,
        "Scanner_Score"
    ] += 15

    df.loc[
        (df["RVOL"] >= 3) &
        (df["RVOL"] < 5),
        "Scanner_Score"
    ] += 10

    df.loc[
        (df["RVOL"] >= 2) &
        (df["RVOL"] < 3),
        "Scanner_Score"
    ] += 5



    # =========================
    # Trend Alignment (0-15)
    # =========================

    df.loc[
        df["Above_SMA20"] == True,
        "Scanner_Score"
    ] += 7

    df.loc[
        df["Above_SMA50"] == True,
        "Scanner_Score"
    ] += 8



    # =========================
    # Breakout Quality (0-10)
    # =========================

    df.loc[
        df["Breakout"] == True,
        "Scanner_Score"
    ] += 10

    df.loc[
        (df["Breakout"] == False) &
        (df["Distance_From_High_%"] <= 5),
        "Scanner_Score"
    ] += 5



    # =========================
    # Liquidity (0-10)
    # =========================

    df.loc[
        df["Avg_Dollar_Volume"] >= 100_000_000,
        "Scanner_Score"
    ] += 10

    df.loc[
        (df["Avg_Dollar_Volume"] >= 25_000_000) &
        (df["Avg_Dollar_Volume"] < 100_000_000),
        "Scanner_Score"
    ] += 5



    # =========================
    # Risk Adjustment (-5/+5)
    # =========================

    df.loc[
        df["Distance_From_High_%"] <= 5,
        "Scanner_Score"
    ] += 5


    df.loc[
        df["Distance_From_High_%"] > 40,
        "Scanner_Score"
    ] -= 5



    # Keep score between 0-100
    df["Scanner_Score"] = (
        df["Scanner_Score"]
        .clip(lower=0, upper=100)
    )


    return df
