import pandas as pd


def add_ai_decisions(df):

    df = df.copy()


    def evaluate(row):

        score = row.get(
            "AI_Final_Score_Adjusted",
            0
        )

        confidence = row.get(
            "AI_Confidence",
            0
        )

        ml = row.get(
            "ML_Probability",
            0
        )

        historical_ml = row.get(
            "Historical_ML_Probability",
            0
        )

        rr = row.get(
            "Risk_Reward",
            0
        )

        regime = row.get(
            "Market_Regime",
            ""
        )

        ai_rating = row.get(
            "AI_Rating",
            ""
        )


        reasons = []


        # ---------------------------------
        # Explanation Builder
        # ---------------------------------

        if row.get("Rank_Score", 0) >= 60:

            reasons.append(
                "Strong technical ranking"
            )


        if ml >= 50:

            reasons.append(
                "Strong current ML confirmation"
            )

        elif ml >= 30:

            reasons.append(
                "Moderate current ML confirmation"
            )

        else:

            reasons.append(
                "Weak current ML confirmation"
            )


        if historical_ml >= 60:

            reasons.append(
                "Historical patterns support setup"
            )


        if regime == "Bearish":

            reasons.append(
                "Bearish market environment"
            )


        if rr >= 2:

            reasons.append(
                "Positive risk/reward"
            )


        # ---------------------------------
        # AI Rating Safety Gate
        # Final quality veto
        # ---------------------------------

        if ai_rating == "PASS":

            reasons.append(
                "AI Rating rejected setup"
            )

            return pd.Series(
                [
                    "PASS",
                    ". ".join(reasons)
                ]
            )


        # ---------------------------------
        # ML Safety Gate
        # ---------------------------------

        if ml < 20:

            reasons.append(
                "ML probability below minimum threshold"
            )

            return pd.Series(
                [
                    "PASS",
                    ". ".join(reasons)
                ]
            )


        # ---------------------------------
        # AI Rating Safety Gate
        # ---------------------------------

        if ai_rating == "PASS":

            decision = "PASS"

            reasons.append(
                "AI Rating rejected setup"
            )

            return pd.Series(
                [
                    decision,
                    ". ".join(reasons)
                ]
            )


        # ---------------------------------
        # Decision Engine
        # ---------------------------------

        if (

            score >= 75
            and confidence >= 70
            and ml >= 70
            and rr >= 2
            and regime != "Bearish"

        ):

            decision = "HIGH CONVICTION"


        elif (

            score >= 60
            and confidence >= 45
            and ml >= 30
            and rr >= 2

        ):

            decision = "STRONG CANDIDATE"


        elif (

            score >= 60
            and confidence >= 40
            and historical_ml >= 60
            and rr >= 2

        ):

            decision = "CANDIDATE"

            reasons.append(
                "Strong historical edge despite weaker current ML"
            )


        elif (

            score >= 50
            and confidence >= 35

        ):

            decision = "CANDIDATE"


        elif score >= 30:

            decision = "WATCHLIST"


        else:

            decision = "PASS"


        return pd.Series(
            [
                decision,
                ". ".join(reasons)
            ]
        )


    df[
        [
            "AI_Decision",
            "AI_Decision_Reason"
        ]
    ] = df.apply(
        evaluate,
        axis=1
    )


    return df