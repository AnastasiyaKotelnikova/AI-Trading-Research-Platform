import pandas as pd


def add_risk_management(
    df,
    account_size=10000
):

    risk_levels = []
    risk_grades = []
    risk_percentages = []
    trade_status = []


    for _, row in df.iterrows():


        # =====================================
        # INPUT VALUES
        # =====================================

        portfolio_risk = row.get(
            "Portfolio_Risk_$",
            0
        )

        allocation = row.get(
            "Portfolio_Allocation_%",
            0
        )

        conviction = row.get(
            "Final_Conviction_Score",
            0
        )

        reward_risk = row.get(
            "Reward_Risk",
            0
        )

        expected_value = row.get(
            "Expected_Value",
            0
        )

        approved = row.get(
            "Portfolio_Approved",
            False
        )


        # =====================================
        # SAFETY CLEANING
        # =====================================

        values = [
            portfolio_risk,
            allocation,
            conviction,
            reward_risk,
            expected_value
        ]


        values = [
            0 if pd.isna(x) else x
            for x in values
        ]


        (
            portfolio_risk,
            allocation,
            conviction,
            reward_risk,
            expected_value
        ) = values



        # =====================================
        # BASE RISK CALCULATION
        # =====================================

        stop_loss_risk_percent = (

            portfolio_risk /
            account_size

        ) * 100



        risk_score = 0



        # -------------------------------------
        # Position concentration
        # -------------------------------------

        if allocation > 25:

            risk_score += 3

        elif allocation > 15:

            risk_score += 2

        elif allocation > 10:

            risk_score += 1



        # -------------------------------------
        # Stop-loss exposure
        # -------------------------------------

        if stop_loss_risk_percent > 3:

            risk_score += 3

        elif stop_loss_risk_percent > 2:

            risk_score += 2

        elif stop_loss_risk_percent > 1:

            risk_score += 1



        # -------------------------------------
        # Reward/Risk quality
        # -------------------------------------

        if reward_risk < 1:

            risk_score += 3

        elif reward_risk < 1.5:

            risk_score += 2



        # -------------------------------------
        # Expected value
        # -------------------------------------

        if expected_value < 0:

            risk_score += 2



        # -------------------------------------
        # Conviction penalty
        # -------------------------------------

        if conviction < 35:

            risk_score += 2



        # =====================================
        # FINAL RISK %
        # =====================================

        final_risk_percent = round(

            stop_loss_risk_percent +
            (risk_score * 0.5),

            2
        )


        risk_percentages.append(
            final_risk_percent
        )



        # =====================================
        # RISK GRADE
        # =====================================

        if risk_score <= 1:

            level = "LOW"
            grade = "A"


        elif risk_score <= 3:

            level = "MODERATE"
            grade = "B"


        elif risk_score <= 5:

            level = "HIGH"
            grade = "C"


        else:

            level = "EXTREME"
            grade = "D"



        risk_levels.append(level)

        risk_grades.append(grade)



        # =====================================
        # TRADE STATUS
        # =====================================

        if (
            approved
            and
            grade in ["A", "B"]
            and
            conviction >= 45
            and
            expected_value >= 0
        ):

            status = "RISK APPROVED"



        elif (
            approved
            and
            grade in ["A", "B"]
        ):

            status = "REVIEW RISK"



        elif approved:

            status = "HIGH RISK REVIEW"



        else:

            status = "NOT APPROVED"



        trade_status.append(
            status
        )



    # =====================================
    # OUTPUT COLUMNS
    # =====================================

    df["Risk_Level"] = risk_levels

    df["Risk_Grade"] = risk_grades

    df["Risk_Percentage"] = risk_percentages

    df["Trade_Status"] = trade_status


    return df