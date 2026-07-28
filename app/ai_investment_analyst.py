import pandas as pd



# =====================================================
# TRADE REASON
# =====================================================

def generate_trade_reason(row):

    reasons = []


    if row.get("Above_SMA20", False):
        reasons.append(
            "Price above SMA20 trend"
        )


    if row.get("Above_SMA50", False):
        reasons.append(
            "Price above SMA50 trend"
        )


    if row.get("RVOL",0) >= 1.5:
        reasons.append(
            "High relative volume"
        )


    if row.get("Momentum_Acceleration",0) > 0:
        reasons.append(
            "Positive momentum acceleration"
        )


    if row.get("Reward_Risk",0) >= 2:
        reasons.append(
            "Strong reward/risk ratio"
        )


    if row.get("Expected_Value",0) > 0:
        reasons.append(
            "Positive expected value"
        )


    if not reasons:

        return (
            "No major technical advantages detected"
        )


    return ", ".join(reasons)




# =====================================================
# STRENGTH ANALYSIS
# =====================================================

def generate_strengths(row):

    strengths=[]


    if row.get(
        "Final_Conviction_Score",
        0
    ) >= 50:

        strengths.append(
            "High conviction score"
        )


    if row.get(
        "Reward_Risk",
        0
    ) >= 2:

        strengths.append(
            "Strong reward/risk profile"
        )


    if row.get(
        "Expected_Value",
        0
    ) > 0:

        strengths.append(
            "Positive expected value"
        )


    if row.get(
        "Risk_Grade"
    ) in ["A","B"]:

        strengths.append(
            "Controlled risk profile"
        )


    if row.get(
        "Historical_ML_Probability",
        0
    ) >= 60:

        strengths.append(
            "ML historical confirmation"
        )


    if not strengths:

        strengths.append(
            "No major strengths detected"
        )


    return strengths




# =====================================================
# RISK ANALYSIS
# =====================================================

def generate_risks(row):

    risks=[]


    if row.get(
        "Risk_Grade",
        "D"
    ) in ["C","D"]:

        risks.append(
            "Higher portfolio risk"
        )


    if row.get(
        "Expected_Value",
        0
    ) < 0:

        risks.append(
            "Negative expected value"
        )


    if row.get(
        "Final_Conviction_Score",
        0
    ) < 40:

        risks.append(
            "Low conviction score"
        )


    if row.get(
        "Trade_Status"
    ) == "NOT APPROVED":

        risks.append(
            "Risk engine did not approve entry"
        )


    if not risks:

        risks.append(
            "No major risks identified"
        )


    return risks




# =====================================================
# AI ACTION
# =====================================================

def generate_action(row):


    decision = row.get(
        "Final_Trade_Decision",
        "NO TRADE"
    )


    actions={


        "APPROVED TRADE":
        "Execute candidate trade with risk controls",


        "REVIEW":
        "Review before possible entry",


        "WATCH":
        "Monitor for confirmation",


        "NO TRADE":
        "Avoid current setup"

    }


    return actions.get(
        decision,
        "Monitor"
    )




# =====================================================
# AI ANALYST SCORE
# =====================================================

def generate_ai_score(row):


    score = (

        row.get(
            "Final_Conviction_Score",
            0
        )

    )


    # reward/risk

    if row.get(
        "Reward_Risk",
        0
    ) >= 2:

        score += 10



    # expected value

    if row.get(
        "Expected_Value",
        0
    ) > 0:

        score += 10



    # risk grade

    grade=row.get(
        "Risk_Grade",
        "D"
    )


    if grade=="A":

        score += 10


    elif grade=="B":

        score += 5


    elif grade in ["C","D"]:

        score -= 10



    # final decision

    decision=row.get(
        "Final_Trade_Decision",
        ""
    )


    if decision=="APPROVED TRADE":

        score += 15


    elif decision=="NO TRADE":

        score -= 15



    return round(
        max(
            0,
            min(score,100)
        ),
        2
    )




# =====================================================
# RATING
# =====================================================

def generate_rating(score):


    if score >= 75:

        return "BUY CANDIDATE"


    elif score >=60:

        return "WATCHLIST"


    elif score >=40:

        return "WEAK"


    else:

        return "AVOID"




# =====================================================
# CONFIDENCE
# =====================================================

def generate_confidence(row):


    if (
        row.get("Final_Trade_Decision")
        ==
        "APPROVED TRADE"
        and
        row.get("Risk_Grade")
        in ["A","B"]
    ):

        return "HIGH"



    if row.get(
        "Final_Trade_Decision"
    )=="WATCH":

        return "MEDIUM"



    return "LOW"




# =====================================================
# SUMMARY
# =====================================================

def generate_summary(row):


    strengths=", ".join(
        row["Strengths"]
    )


    risks=", ".join(
        row["Risks"]
    )


    return (

        f"{row['Symbol']} | "

        f"Decision: {row.get('Final_Trade_Decision')} | "

        f"Analyst Score: "
        f"{row.get('AI_Analyst_Score',0):.1f} | "

        f"Rating: "
        f"{row.get('AI_Analyst_Rating')} | "

        f"Confidence: "
        f"{row.get('AI_Analyst_Confidence')} | "

        f"Strengths: {strengths} | "

        f"Risks: {risks}"

    )




# =====================================================
# MAIN ANALYST ENGINE
# =====================================================

def analyze_stocks(df):


    df=df.copy()



    df["Trade_Reason"] = df.apply(
        generate_trade_reason,
        axis=1
    )


    df["Strengths"] = df.apply(
        generate_strengths,
        axis=1
    )


    df["Risks"] = df.apply(
        generate_risks,
        axis=1
    )


    df["AI_Action"] = df.apply(
        generate_action,
        axis=1
    )


    df["AI_Analyst_Score"] = df.apply(
        generate_ai_score,
        axis=1
    )


    df["AI_Analyst_Rating"] = df[
        "AI_Analyst_Score"
    ].apply(
        generate_rating
    )


    df["AI_Analyst_Confidence"] = df.apply(
        generate_confidence,
        axis=1
    )


    df["AI_Summary"] = df.apply(
        generate_summary,
        axis=1
    )


    return df