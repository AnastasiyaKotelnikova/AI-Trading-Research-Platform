def generate_signal_explanation(row):

    reasons = []


    if row["Rank_Score"] >= 90:
        reasons.append(
            "Excellent overall ranking score"
        )


    if row["Risk_Reward"] >= 2:
        reasons.append(
            "Strong risk/reward setup"
        )


    if row["Above_SMA20"]:
        reasons.append(
            "Price above 20-day moving average"
        )


    if row["Above_SMA50"]:
        reasons.append(
            "Price above 50-day moving average"
        )


    if row["RVOL"] >= 3:
        reasons.append(
            "High relative volume confirmation"
        )


    if row["Relative_Strength"] > 5:
        reasons.append(
            "Outperforming the market"
        )


    return reasons
