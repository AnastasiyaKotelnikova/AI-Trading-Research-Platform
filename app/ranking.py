import pandas as pd


def calculate_rank_score(df):

    df = df.copy()


    # -------------------------
    # Momentum Score (30)
    # -------------------------

    df["Momentum_Score"] = 0


    # Healthy momentum
    # Best historical zone

    df.loc[
        (df["Return_20D"] >= 10) &
        (df["Return_20D"] < 30),
        "Momentum_Score"
    ] += 20


    # Strong momentum
    # Higher risk

    df.loc[
        (df["Return_20D"] >= 30) &
        (df["Return_20D"] < 50),
        "Momentum_Score"
    ] += 10


    # Late-stage momentum
    # No reward

    df.loc[
        (df["Return_20D"] >= 50) &
        (df["Return_20D"] < 80),
        "Momentum_Score"
    ] += 0


    # Short-term confirmation

    df.loc[
        (df["Return_5D"] >= 3) &
        (df["Return_5D"] < 10),
        "Momentum_Score"
    ] += 5


    # Extreme move penalty

    df.loc[
        df["Return_20D"] >= 80,
        "Momentum_Score"
    ] -= 10


    # Overbought penalty

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


    # Best historical zone

    df.loc[
        (df["Relative_Strength"] >= 10) &
        (df["Relative_Strength"] < 20),
        "Relative_Strength_Score"
    ] = 15


    # Good zone

    df.loc[
        (df["Relative_Strength"] >= 20) &
        (df["Relative_Strength"] < 30),
        "Relative_Strength_Score"
    ] = 10


    # Extended

    df.loc[
        df["Relative_Strength"] >= 30,
        "Relative_Strength_Score"
    ] = 5



    # -------------------------
    # Setup Quality (20)
    # -------------------------

    df["Setup_Score"] = (
        df["Setup_Quality"] / 5
    )



    # -------------------------
    # Risk Score
    # -------------------------

    df["Risk_Score"] = 0


    df.loc[
        df["Risk_Reward"] >= 2.5,
        "Risk_Score"
    ] += 5


    df.loc[
        (df["Risk_Reward"] >= 1.5) &
        (df["Risk_Reward"] < 2.5),
        "Risk_Score"
    ] += 3


    df.loc[
        df["Risk_Reward"] < 1,
        "Risk_Score"
    ] -= 5


    df.loc[
        df["RSI"] >= 85,
        "Risk_Score"
    ] -= 10


    df.loc[
        df["Overextended"] == True,
        "Risk_Score"
    ] -= 10



    # -------------------------
    # Market Regime Adjustment
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
    # Risk Reward Score
    # -------------------------

    df["Risk_Reward_Score"] = 0


    df.loc[
        df["Risk_Reward"] >= 3,
        "Risk_Reward_Score"
    ] = 10


    df.loc[
        (df["Risk_Reward"] >= 2) &
        (df["Risk_Reward"] < 3),
        "Risk_Reward_Score"
    ] = 7


    df.loc[
        (df["Risk_Reward"] >= 1.5) &
        (df["Risk_Reward"] < 2),
        "Risk_Reward_Score"
    ] = 3


    df.loc[
        df["Risk_Reward"] < 1,
        "Risk_Reward_Score"
    ] = -5



    # -------------------------
    # Final Rank Score
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
        +
        df["Risk_Reward_Score"]
    )

    print(
        df[
            [
                "Symbol",
                "Return_20D",
                "Return_5D",
                "RSI",
                "Momentum_Score",
            ]
        ]
        .sort_values("Momentum_Score", ascending=False)
        .head(20)
    )

    return df
