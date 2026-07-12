import pandas as pd


def calculate_scores(df):

    df = df.copy()

    df["Scanner_Score"] = 0

    # -------------------------
    # Price Change (0-30)
    # -------------------------
    df.loc[df["Change_%"] >= 10, "Scanner_Score"] += 30
    df.loc[
        (df["Change_%"] >= 5) &
        (df["Change_%"] < 10),
        "Scanner_Score"
    ] += 20

    df.loc[
        (df["Change_%"] >= 2) &
        (df["Change_%"] < 5),
        "Scanner_Score"
    ] += 10

    # -------------------------
    # Relative Volume (0-30)
    # -------------------------
    df.loc[df["RVOL"] >= 5, "Scanner_Score"] += 30

    df.loc[
        (df["RVOL"] >= 3) &
        (df["RVOL"] < 5),
        "Scanner_Score"
    ] += 20

    df.loc[
        (df["RVOL"] >= 2) &
        (df["RVOL"] < 3),
        "Scanner_Score"
    ] += 10

    # -------------------------
    # Average Dollar Volume (0-20)
    # -------------------------
    df.loc[df["Avg_Dollar_Volume"] >= 100_000_000,
       "Scanner_Score"] += 20

    df.loc[
        (df["Avg_Dollar_Volume"] >= 25_000_000) &
        (df["Avg_Dollar_Volume"] < 100_000_000),
        "Scanner_Score"
    ] += 10

        # -------------------------
    # Price Filter (0-10)
    # -------------------------
    df.loc[df["Price"] >= 5,
           "Scanner_Score"] += 10


    # -------------------------
    # Liquidity (0-10)
    # -------------------------
    df.loc[df["Volume"] >= 1_000_000,
           "Scanner_Score"] += 10


    # -------------------------
    # Breakout Quality (0-15)
    # -------------------------

    # True breakout
    df.loc[
        df["Breakout"] == True,
        "Scanner_Score"
    ] += 10


    # Near breakout level
    df.loc[
        df["Distance_From_High_%"] <= 5,
        "Scanner_Score"
    ] += 5

    # -------------------------
    # Trend Alignment (0-10)
    # -------------------------

    df.loc[
        df["Above_SMA20"] == True,
        "Scanner_Score"
    ] += 5


    df.loc[
        df["Above_SMA50"] == True,
        "Scanner_Score"
    ] += 5

        # -------------------------
    # Extended Move Penalty
    # -------------------------

    # Penalize stocks too far below recent highs
    df.loc[
        df["Distance_From_High_%"] > 40,
        "Scanner_Score"
    ] -= 5

    # -------------------------
    # Relative Strength vs SPY (0-10)
    # -------------------------

    df.loc[
        df["Relative_Strength"] >= 10,
        "Scanner_Score"
    ] += 10

    df.loc[
        (df["Relative_Strength"] >= 5) &
        (df["Relative_Strength"] < 10),
        "Scanner_Score"
    ] += 5


    return df