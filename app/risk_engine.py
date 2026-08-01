import pandas as pd



def add_risk_management(
    df,
    account_size=10000,
    max_risk_percent=1
):

    df = df.copy()


    trade_status = []
    risk_scores = []
    risk_reasons = []



    for _, row in df.iterrows():


        portfolio_action = row.get(
            "Portfolio_Action",
            "REJECT"
        )


        expected_value = row.get(
            "Expected_Value",
            0
        )


        reward_risk = row.get(
            "Reward_Risk",
            0
        )


        conviction = row.get(
            "Final_Conviction_Score",
            0
        )


        risk_amount = row.get(
            "Portfolio_Risk_$",
            0
        )


        if pd.isna(expected_value):
            expected_value = 0


        if pd.isna(reward_risk):
            reward_risk = 0


        if pd.isna(conviction):
            conviction = 0


        if pd.isna(risk_amount):
            risk_amount = 0



        # --------------------------------
        # Risk score
        # --------------------------------

        risk_score = 100

        reasons = []



        # Expected value filter

        if expected_value < -0.25:

            risk_score -= 50

            reasons.append(
                "Negative expected value"
            )


        elif expected_value < 0:

            risk_score -= 15

            reasons.append(
                "Weak expected value"
            )



        # Reward/Risk

        if reward_risk < 1.5:

            risk_score -= 25

            reasons.append(
                "Poor reward risk ratio"
            )



        # Conviction

        if conviction < 35:

            risk_score -= 20

            reasons.append(
                "Low conviction"
            )



        # Position risk

        max_allowed_risk = (
            account_size *
            max_risk_percent /
            100
        )


        if risk_amount > max_allowed_risk:

            risk_score -= 25

            reasons.append(
                "Risk exceeds limit"
            )



        risk_score = max(
            risk_score,
            0
        )



        # --------------------------------
        # Final risk approval
        # --------------------------------

        if portfolio_action == "ALLOW ENTRY":


            if risk_score >= 70:

                status = "RISK APPROVED"


            elif risk_score >= 45:

                status = "WATCH RISK"


            else:

                status = "BLOCKED"



        elif portfolio_action == "WATCH ENTRY":

            status = "WATCH RISK"



        elif portfolio_action == "MONITOR":

            status = "MONITOR"



        else:

            status = "BLOCKED"



        trade_status.append(
            status
        )


        risk_scores.append(
            risk_score
        )


        if reasons:

            risk_reasons.append(
                "; ".join(reasons)
            )

        else:

            risk_reasons.append(
                "Risk acceptable"
            )



    df["Trade_Status"] = trade_status


    df["Risk_Score"] = risk_scores


    df["Risk_Reason"] = risk_reasons



    return df