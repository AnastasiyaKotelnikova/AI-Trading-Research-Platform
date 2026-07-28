def calculate_setup_quality(row):

    score = 0


    # Good RSI zone
    if 50 <= row["RSI"] <= 75:
        score += 20


    # Strong but not exhausted momentum
    if row["Return_5D"] > 5 and row["Return_5D"] < 40:
        score += 20


    # Trend confirmation
    if row["Above_SMA20"]:
        score += 15


    if row["Above_SMA50"]:
        score += 15


    # Volume confirmation
    if row["RVOL"] >= 1.5:
        score += 15


    # Avoid chasing
    if not row["Overextended"]:
        score += 15


    return score
