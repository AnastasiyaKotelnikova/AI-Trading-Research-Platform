app/trade_decision.py

def trade_decision(score):

    if score >= 90:
        return "ELITE"

    elif score >= 80:
        return "HIGH CONVICTION"

    elif score >= 70:
        return "STRONG"

    elif score >= 60:
        return "WATCH"

    return "PASS"