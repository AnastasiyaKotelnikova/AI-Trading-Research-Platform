import pandas as pd


def add_execution_analysis(df):

    df = df.copy()

    execution_scores = []
    execution_grades = []
    execution_actions = []
    execution_reasons = []


    for _, row in df.iterrows():

        score = 0
        reasons = []


        # =====================================
        # Trend Check
        # =====================================

        close = row.get(
            "Close",
            0
        )

        sma20 = row.get(
            "SMA20",
            0
        )

        sma50 = row.get(
            "SMA50",
            0
        )


        if pd.notna(close) and pd.notna(sma20):

            if close > sma20:

                score += 20

                reasons.append(
                    "Price above SMA20"
                )

            else:

                reasons.append(
                    "Below SMA20"
                )



        if pd.notna(close) and pd.notna(sma50):

            if close > sma50:

                score += 20

                reasons.append(
                    "Above SMA50 trend"
                )



        # =====================================
        # Momentum Check
        # =====================================

        rsi = row.get(
            "RSI",
            50
        )


        if pd.isna(rsi):

            rsi = 50



        if 45 <= rsi <= 70:

            score += 20

            reasons.append(
                "Healthy RSI momentum"
            )


        elif rsi > 70:

            score -= 10

            reasons.append(
                "RSI overextended"
            )


        else:

            reasons.append(
                "Weak momentum"
            )



        # =====================================
        # Volume Confirmation
        # =====================================

        rvol = row.get(
            "RVOL",
            1
        )


        if pd.isna(rvol):

            rvol = 1



        if rvol >= 1.2:

            score += 20

            reasons.append(
                "Volume confirmation"
            )

        else:

            reasons.append(
                "No volume confirmation"
            )



        # =====================================
        # Relative Strength
        # =====================================

        rs = row.get(
            "Relative_Strength",
            0
        )


        if pd.notna(rs):

            if rs > 0:

                score += 20

                reasons.append(
                    "Outperforming market"
                )



        # Keep technical score 0-100

        score = max(
            0,
            min(score,100)
        )



        # =====================================
        # AI Decision Override
        # =====================================

        final_status = row.get(
            "Final_AI_Status",
            ""
        )


        expected_value = row.get(
            "Expected_Value",
            0
        )


        if pd.isna(expected_value):

            expected_value = 0



        # -------------------------------
        # AI rejected
        # -------------------------------

        if final_status == "NO TRADE":

            grade = "D"

            action = "BLOCKED"


            score = min(
                score,
                30
            )


            reasons.append(
                "Blocked by AI decision"
            )



        # -------------------------------
        # AI monitoring
        # -------------------------------

        elif final_status == "MONITOR":

            grade = "C"

            action = "WAIT"


            score = min(
                score,
                50
            )


            reasons.append(
                "Monitoring only"
            )



        # -------------------------------
        # AI watchlist
        # -------------------------------

        elif final_status == "WATCHLIST":

            grade = "C"

            action = "WAIT"


            score = min(
                score,
                60
            )


            reasons.append(
                "Waiting for confirmation"
            )



        # -------------------------------
        # Approved trade candidates
        # -------------------------------

        elif expected_value < -0.15:

            grade = "D"

            action = "AVOID"


            reasons.append(
                "Negative expected value"
            )



        elif score >= 80:

            grade = "A"

            action = "BUY NOW"



        elif score >= 60:

            grade = "B"

            action = "GOOD ENTRY"



        elif score >= 40:

            grade = "C"

            action = "WAIT"



        else:

            grade = "D"

            action = "AVOID"



        # =====================================
        # Save Results
        # =====================================

        execution_scores.append(
            score
        )

        execution_grades.append(
            grade
        )

        execution_actions.append(
            action
        )

        execution_reasons.append(
            "; ".join(reasons)
        )



    # =====================================
    # Output Columns
    # =====================================

    df["Execution_Score"] = execution_scores

    df["Execution_Grade"] = execution_grades

    df["Execution_Action"] = execution_actions

    df["Execution_Reason"] = execution_reasons



    return df