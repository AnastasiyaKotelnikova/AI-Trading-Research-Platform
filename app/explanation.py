def build_explanation(row):

    reasons = []
    risks = []

    # Momentum
    if row["Change_%"] >= 10:
        reasons.append(f"Strong momentum (+{row['Change_%']:.2f}%)")
    elif row["Change_%"] >= 5:
        reasons.append(f"Good momentum (+{row['Change_%']:.2f}%)")

    # Relative Volume
    if row["RVOL"] >= 5:
        reasons.append(f"Very high RVOL ({row['RVOL']:.2f})")
    elif row["RVOL"] >= 2:
        reasons.append(f"High RVOL ({row['RVOL']:.2f})")

    # Liquidity
    if row["Avg_Dollar_Volume"] >= 100_000_000:
        reasons.append("Excellent liquidity")
    elif row["Avg_Dollar_Volume"] >= 25_000_000:
        reasons.append("Good liquidity")

    # Breakout
    if row["Breakout"]:
        reasons.append("20-day breakout")

    # Trend
    if row["Above_SMA20"]:
        reasons.append("Above SMA20")

    if row["Above_SMA50"]:
        reasons.append("Above SMA50")

    # Relative Strength
    if row["Relative_Strength"] >= 10:
        reasons.append("Outperforming SPY")

    # Risks
    if row["Distance_From_High_%"] > 20:
        risks.append("Far below recent high")

    if row["Change_%"] > 30:
        risks.append("Very large one-day move")

    return {
        "Reasons": reasons,
        "Risks": risks
    }
