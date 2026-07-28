def calculate_position_size(
    entry,
    stop_loss,
    trade_score,
    base_risk=100
):

    risk_per_share = entry - stop_loss

    if risk_per_share <= 0:
        return None


    # AI confidence adjustment
    if trade_score >= 90:
        risk_multiplier = 1.50

    elif trade_score >= 80:
        risk_multiplier = 1.25

    elif trade_score >= 70:
        risk_multiplier = 1.00

    elif trade_score >= 60:
        risk_multiplier = 0.75

    else:
        risk_multiplier = 0.50


    adjusted_risk = base_risk * risk_multiplier


    shares = int(adjusted_risk / risk_per_share)

    capital_required = round(shares * entry, 2)


    return {

        "Risk_Per_Share": round(risk_per_share, 2),

        "Risk_Multiplier": risk_multiplier,

        "Adjusted_Risk": round(adjusted_risk, 2),

        "Shares": shares,

        "Capital_Required": capital_required

    }
