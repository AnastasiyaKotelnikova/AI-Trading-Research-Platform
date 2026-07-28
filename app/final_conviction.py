import pandas as pd


def add_final_conviction(df):

    conviction_scores = []

    conviction_ratings = []

    actions = []


    for _, row in df.iterrows():


        # -------------------------------
        # AI SCORE
        # -------------------------------

        ai_score = row.get(
            "AI_Final_Score",
            0
        )


        if pd.isna(ai_score):

            ai_score = 0


        ai_score = min(
            ai_score,
            100
        )



        # -------------------------------
        # ML PROBABILITY
        # -------------------------------

        ml_probability = row.get(
            "Combined_ML_Probability",
            row.get(
                "ML_Probability",
                0
            )
        )


        if pd.isna(ml_probability):

            ml_probability = 0


        if ml_probability > 1:

            ml_probability = ml_probability / 100



        # -------------------------------
        # TRADE SCORE
        # -------------------------------

        trade_score = row.get(
            "Trade_Score",
            0
        )


        if pd.isna(trade_score):

            trade_score = 0



        # -------------------------------
        # RISK REWARD
        # -------------------------------

        reward_risk = row.get(
            "Reward_Risk",
            0
        )


        if pd.isna(reward_risk):

            reward_risk = 0



        # -------------------------------
        # EXPECTED VALUE
        # -------------------------------

        expected_value = row.get(
            "Expected_Value",
            0
        )


        if pd.isna(expected_value):

            expected_value = 0



        # -------------------------------
        # RISK QUALITY SCORE
        # -------------------------------

        risk_quality = 0


        if reward_risk >= 2:

            risk_quality = 100

        elif reward_risk >= 1.5:

            risk_quality = 75

        elif reward_risk >= 1:

            risk_quality = 50



        # -------------------------------
        # EXPECTED VALUE SCORE
        # -------------------------------

        ev_score = 50 + (
            expected_value * 50
        )


        ev_score = max(
            0,
            min(
                ev_score,
                100
            )
        )



        # -------------------------------
        # FINAL CONVICTION SCORE
        # -------------------------------

        score = (

            ai_score * 0.40

            +

            (ml_probability * 100) * 0.30

            +

            trade_score * 0.20

            +

            ev_score * 0.05

            +

            risk_quality * 0.05

        )


        score = round(
            score,
            2
        )


        conviction_scores.append(
            score
        )



        # -------------------------------
        # CONVICTION CLASSIFICATION
        # -------------------------------

        if score >= 70:

            rating = "VERY HIGH"

            action = "STRONG CANDIDATE"

            tier = "TIER 1"


        elif score >= 50:

            rating = "MEDIUM"

            action = "QUALIFIED SETUP"

            tier = "TIER 2"


        elif score >= 35:

            rating = "LOW"

            action = "WATCHLIST"

            tier = "TIER 3"


        else:

            rating = "VERY LOW"

            action = "NO EDGE"

            tier = "TIER 4"



        conviction_ratings.append(
            rating
        )

        actions.append(
            action
        )



    df["Final_Conviction_Score"] = conviction_scores

    df["Final_Conviction_Rating"] = conviction_ratings

    df["Final_Action"] = actions



    # -----------------------------------
    # FINAL RANKING
    # -----------------------------------

    df = df.sort_values(
        "Final_Conviction_Score",
        ascending=False
    )


    df["Conviction_Rank"] = range(
        1,
        len(df) + 1
    )


    df["Conviction_Tier"] = (

        df["Final_Action"]

        .map({

            "STRONG CANDIDATE": "TIER 1",

            "QUALIFIED SETUP": "TIER 2",

            "WATCHLIST": "TIER 3",

            "NO EDGE": "TIER 4"

        })

    )


    return df