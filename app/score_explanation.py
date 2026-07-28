def generate_score_breakdown(row):

    breakdown = []

    breakdown.append(
        f"Momentum: {row['Momentum_Score']}"
    )

    breakdown.append(
        f"Trend: {row['Trend_Score']}"
    )

    breakdown.append(
        f"Volume: {row['Volume_Score']}"
    )

    breakdown.append(
        f"Relative Strength: {row['Relative_Strength_Score']}"
    )

    breakdown.append(
        f"Setup Quality: {row['Setup_Score']:.1f}"
    )

    breakdown.append(
        f"Risk Adjustment: {row['Risk_Score']}"
    )

    breakdown.append(
        f"Risk/Reward: {row['Risk_Reward_Score']}"
    )


    return "\n".join(breakdown)
