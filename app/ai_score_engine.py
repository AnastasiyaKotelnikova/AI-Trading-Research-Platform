import pandas as pd


def add_ai_analyst_score(df):


    analyst_scores = []
    analyst_ratings = []
    analyst_confidence = []



    for _, row in df.iterrows():


        # =====================================
        # INPUT VALUES
        # =====================================

        conviction = row.get(
            "Final_Conviction_Score",
            0
        )


        ml_probability = row.get(
            "ML_Probability",
            0
        )


        expected_value = row.get(
            "Expected_Value",
            0
        )


        risk_grade = row.get(
            "Risk_Grade",
            "D"
        )


        final_decision = row.get(
            "Final_Trade_Decision",
            "NO TRADE"
        )



        # Safety checks

        values = [
            conviction,
            ml_probability,
            expected_value
        ]


        values = [
            0 if pd.isna(x) else x
            for x in values
        ]


        (
            conviction,
            ml_probability,
            expected_value
        ) = values



        # =====================================
        # NORMALIZE ML SCORE
        # =====================================

        if ml_probability <= 1:

            ml_probability = ml_probability * 100


        ml_score = min(
            ml_probability,
            100
        )



        # =====================================
        # EXPECTED VALUE SCORE
        # =====================================

        if expected_value >= 0.5:

            ev_score = 100

        elif expected_value >= 0:

            ev_score = 70

        elif expected_value >= -0.5:

            ev_score = 40

        else:

            ev_score = 20



        # =====================================
        # RISK SCORE
        # =====================================

        risk_scores = {

            "A": 100,
            "B": 80,
            "C": 55,
            "D": 25

        }


        risk_score = risk_scores.get(
            risk_grade,
            25
        )



        # =====================================
        # FINAL AI SCORE
        # =====================================

        score = (

            conviction * 0.40
            +
            ml_score * 0.25
            +
            ev_score * 0.20
            +
            risk_score * 0.15

        )


        score = round(
            score,
            2
        )


        analyst_scores.append(
            score
        )



        # =====================================
        # RATING
        # =====================================

        if score >= 80:

            rating = "STRONG BUY SETUP"


        elif score >= 65:

            rating = "QUALITY SETUP"


        elif score >= 50:

            rating = "WATCH"


        else:

            rating = "AVOID"



        analyst_ratings.append(
            rating
        )



        # =====================================
        # CONFIDENCE
        # =====================================

        if score >= 80:

            confidence = "HIGH"


        elif score >= 60:

            confidence = "MEDIUM"


        else:

            confidence = "LOW"



        analyst_confidence.append(
            confidence
        )



    df["AI_Analyst_Score"] = analyst_scores

    df["AI_Analyst_Rating"] = analyst_ratings

    df["AI_Analyst_Confidence"] = analyst_confidence



    return df