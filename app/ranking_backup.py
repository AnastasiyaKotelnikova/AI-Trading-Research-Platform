import pandas as pd


def calculate_rank_score(df):

    df = df.copy()


    # -------------------------
    # Momentum Score (30)
    # -------------------------

    df["Momentum_Score"] = 0


    # Strong but not extreme momentum

    df.loc[
        (df["Return_20D"] >= 15) &
        (df["Return_20D"] < 50),
        "Momentum_Score"
    ] += 20


    # Exceptional momentum

    df.loc[
        (df["Return_20D"] >= 50) &
        (df["Return_20D"] < 80),
        "Momentum_Score"
    ] += 25


    # Short term confirmation

    df.loc[
        df["Return_5D"] >= 5,
        "Momentum_Score"
    ] += 5


    # Penalize extreme moves

    df.loc[
        df["Return_20D"] >= 80,
        "Momentum_Score"
    ] -= 10


    df.loc[
        df["RSI"] >= 80,
        "Momentum_Score"
    ] -= 10


    # -------------------------
    # Trend Score (20)
    # -------------------------

    df["Trend_Score"] = 0

    df.loc[
        df["Above_SMA20"] == True,
        "Trend_Score"
    ] += 10


    df.loc[
        df["Above_SMA50"] == True,
        "Trend_Score"
    ] += 10



    # -------------------------
    # Volume Score (15)
    # -------------------------

    df["Volume_Score"] = 0


    df.loc[
        df["RVOL"] >= 3,
        "Volume_Score"
    ] += 15


    df.loc[
        (df["RVOL"] >= 2) &
        (df["RVOL"] < 3),
        "Volume_Score"
    ] += 10


    df.loc[
        df["Dollar_Volume"] >= 100_000_000,
        "Volume_Score"
    ] += 5

   
    # -------------------------
    # Relative Strength Score (15)
    # -------------------------

    df["Relative_Strength_Score"] = 0

    df.loc[
        df["Relative_Strength"] >= 15,
        "Relative_Strength_Score"
    ] = 15

    df.loc[
        (df["Relative_Strength"] >= 10) &
        (df["Relative_Strength"] < 15),
        "Relative_Strength_Score"
    ] = 10

    df.loc[
        (df["Relative_Strength"] >= 5) &
        (df["Relative_Strength"] < 10),
        "Relative_Strength_Score"
    ] = 5


    ## -------------------------
    # Setup Quality (20)
    # -------------------------

    df["Setup_Score"] = (
        df["Setup_Quality"] / 5
    )

    # -------------------------
    # Risk Penalty
    # -------------------------

    df["Risk_Score"] = 0


    df.loc[
        df["RSI"] >= 85,
        "Risk_Score"
    ] -= 10


    df.loc[
        df["Overextended"] == True,
        "Risk_Score"
    ] -= 10

 
    # -------------------------
    # Market Regime Score
    # -------------------------

    df["Market_Regime_Adjustment"] = 0


    df.loc[
        df["Market_Regime"] == "Bullish",
        "Market_Regime_Adjustment"
    ] = 5


    df.loc[
        df["Market_Regime"] == "Bearish",
        "Market_Regime_Adjustment"
    ] = -10

    # -------------------------
    # Final Score
    # -------------------------

    df["Rank_Score"] = (
        df["Momentum_Score"]
        +
        df["Trend_Score"]
        +
        df["Volume_Score"]
        +
        df["Relative_Strength_Score"]
        +
        df["Setup_Score"]
        +
        df["Risk_Score"]
        +
        df["Market_Regime_Adjustment"]
    )


    return df

