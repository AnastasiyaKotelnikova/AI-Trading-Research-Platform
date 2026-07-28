def generate_trade_reason(row):

    reasons = []
    warnings = []


    # -------------------------
    # Momentum
    # -------------------------

    if row["Return_20D"] >= 50:

        reasons.append(
            f"Exceptional 20D momentum (+{row['Return_20D']:.1f}%)"
        )

    elif row["Return_20D"] >= 20:

        reasons.append(
            f"Strong 20D momentum (+{row['Return_20D']:.1f}%)"
        )

    elif row["Return_20D"] >= 10:

        reasons.append(
            f"Positive 20D momentum (+{row['Return_20D']:.1f}%)"
        )



    # -------------------------
    # Short Term Momentum
    # -------------------------

    if row["Return_5D"] >= 5:

        reasons.append(
            f"Short-term strength (+{row['Return_5D']:.1f}% 5D)"
        )


