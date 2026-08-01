import pandas as pd


def add_ai_analyst_score(df):

    analyst_scores = []
    analyst_ratings = []
    analyst_confidence = []


    for _, row in df.iterrows():

        conviction = row.get(
            "Final_Conviction_Score",
            0
        )


        ml_probability = row.get(
            "Combined_ML_Probability",
            row.get(
                "ML_Probability",
                0
            )
        )


        expected_value = row.get(
            "Expected_Value",
            0
        )


        risk_grade = row.get(
            "Risk_Grade",
            "C"
        )


        values = [
            conviction,
            ml_probability,
            expected_value
        ]


        values = [
            0 if pd.isna(x) else x
            for x in values
        ]


        conviction, ml_probability, expected_value = values



        # -------------------------------
        # ML normalization
        # -------------------------------

        if ml_probability <= 1:

            ml_probability *= 100


        ml_score = min(
            ml_probability,
            100
        )



        # -------------------------------
        # Expected value score
        # -------------------------------

        if expected_value >= 0.30:

            ev_score = 100


        elif expected_value >= 0:

            ev_score = 75


        elif expected_value >= -0.20:

            ev_score = 55


        else:

            ev_score = 25



        # -------------------------------
        # Risk score
        # -------------------------------

        risk_scores = {

            "A":100,
            "B":85,
            "C":65,
            "D":40

        }


        risk_score = risk_scores.get(
            risk_grade,
            65
        )



        # -------------------------------
        # AI Analyst Score
        # -------------------------------

        score = (

            conviction * 0.60

            +

            ml_score * 0.20

            +

            ev_score * 0.15

            +

            risk_score * 0.05

        )


        score = round(
            score,
            2
        )


        analyst_scores.append(
            score
        )



        # -------------------------------
        # Rating
        # -------------------------------

        if score >= 75:

            rating = "STRONG BUY SETUP"


        elif score >= 60:

            rating = "QUALITY SETUP"


        elif score >= 45:

            rating = "WATCH"


        else:

            rating = "AVOID"


        analyst_ratings.append(
            rating
        )



        # -------------------------------
        # Confidence
        # -------------------------------

        if score >= 75:

            confidence = "HIGH"


        elif score >= 55:

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