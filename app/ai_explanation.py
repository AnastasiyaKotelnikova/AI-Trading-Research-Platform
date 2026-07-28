import pandas as pd



def add_ai_explanation(df):


    df = df.copy()



    positive = []

    negative = []



    summaries = []



    for _, row in df.iterrows():


        pos = []

        neg = []



        # -----------------------------
        # Momentum
        # -----------------------------

        if row.get("Momentum_Score",0) >= 15:

            pos.append(
                "Strong momentum"
            )

        elif row.get("Momentum_Score",0) < 5:

            neg.append(
                "Weak momentum"
            )



        # -----------------------------
        # Trend
        # -----------------------------

        if row.get("Rank_Score",0) >= 50:

            pos.append(
                "Positive technical trend"
            )

        else:

            neg.append(
                "Weak technical structure"
            )



        # -----------------------------
        # ML confidence
        # -----------------------------

        if row.get("ML_Probability",0) >= 50:

            pos.append(
                "High ML probability"
            )

        else:

            neg.append(
                "Low ML probability"
            )



        # -----------------------------
        # Historical learning
        # -----------------------------

        learned = row.get(
            "AI_Learned_Score",
            row.get("AI_Final_Score",0)
        )


        base = row.get(
            "AI_Final_Score",
            0
        )


        if learned < base:

            neg.append(
                "Historical performance reduced confidence"
            )

        elif learned > base:

            pos.append(
                "Historical performance improved confidence"
            )



        # -----------------------------
        # Market regime
        # -----------------------------

        regime = row.get(
            "Market_Regime",
            ""
        )


        if regime == "Bullish":

            pos.append(
                "Bullish market environment"
            )


        elif regime == "Bearish":

            neg.append(
                "Bearish market environment"
            )



        positive.append(
            " | ".join(pos)
        )


        negative.append(
            " | ".join(neg)
        )



        # -----------------------------
        # AI summary
        # -----------------------------

        if len(pos) > len(neg):

            summary = (
                "Technical and model factors "
                "are mostly supportive."
            )


        elif len(neg) > len(pos):

            summary = (
                "Setup has potential but "
                "contains significant risks."
            )


        else:

            summary = (
                "Mixed signals require "
                "additional confirmation."
            )



        summaries.append(summary)



    df["AI_Positive_Factors"] = positive

    df["AI_Negative_Factors"] = negative

    df["AI_Summary"] = summaries



    return df