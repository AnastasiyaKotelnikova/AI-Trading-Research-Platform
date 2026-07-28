def generate_trade_reason(row):

    reasons = []
    warnings = []


    # Momentum
    if row["Return_20D"] > 20:
        reasons.append(
            f"Strong 20D momentum (+{row['Return_20D']:.1f}%)"
        )

    elif row["Return_20D"] > 10:
        reasons.append(
            f"Positive 20D momentum (+{row['Return_20D']:.1f}%)"
        )


    # Relative Strength
    if row["Relative_Strength"] > 10:
        reasons.append(
            f"Outperforming SPY (+{row['Relative_Strength']:.1f}%)"
        )


    # Trend
    if row["Above_SMA20"]:
        reasons.append(
            "Above SMA20"
        )

    if row["Above_SMA50"]:
        reasons.append(
            "Above SMA50"
        )


    # Volume
    if row["RVOL"] > 1.5:
        reasons.append(
            f"High volume (RVOL {row['RVOL']})"
        )


    # Setup quality
    if row["Setup_Quality"] >= 85:
        reasons.append(
            "High quality technical setup"
        )


    # Warnings

    if row["RSI"] > 70:
        warnings.append(
            f"RSI elevated ({row['RSI']:.1f})"
        )


    if row["Overextended"]:
        warnings.append(
            "Price extended from recent base"
        )


    if row["Risk_Score"] < 0:
        warnings.append(
            "Higher risk setup"
        )


    result = ""


    if reasons:
        result += "✓ " + "\n✓ ".join(reasons)


    if warnings:
        result += "\n\n⚠ " + "\n⚠ ".join(warnings)


    return result
