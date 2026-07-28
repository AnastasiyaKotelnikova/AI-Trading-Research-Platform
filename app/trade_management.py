import pandas as pd

from app.position_sizing import calculate_position_size


def add_trade_management(df):

    trade_scores = []

    shares_list = []

    capital_list = []

    risk_per_share_list = []

    reward_risk_list = []

    expected_value_list = []

    grade_list = []


    for _, row in df.iterrows():

        probability = row.get(
            "Combined_ML_Probability",
            row.get(
                "ML_Probability",
                0
            )
        )


        # Convert percentage probability to decimal
        # Example: 31.93 -> 0.3193
        if probability > 1:

            probability = probability / 100



        confidence = row.get(
            "AI_Final_Score",
            0
        )


        entry = row.get("Entry")

        stop = row.get("Stop_Loss")

        target = row.get("Target_1")


        if pd.isna(target):

            target = row.get("Target_2")



        reward_risk = None

        expected_value = None

        position = None



        #
        # Calculate reward/risk and expected value
        #

        if (
            pd.notna(entry)
            and
            pd.notna(stop)
            and
            pd.notna(target)
        ):

            risk = entry - stop

            reward = target - entry


            if risk > 0:

                reward_risk = reward / risk


                expected_value = (

                    probability * reward

                    -

                    (1 - probability) * risk

                )



        #
        # Calculate trade score
        #

        ev_bonus = 0


        if expected_value is not None:

            ev_bonus = min(
                expected_value / 100,
                20
            )



        trade_score = round(

            probability * 60

            +

            confidence * 0.35

            +

            ev_bonus,

            2

        )



        #
        # Position sizing
        #

        if (
            pd.notna(entry)
            and
            pd.notna(stop)
        ):

            position = calculate_position_size(

                entry,

                stop,

                trade_score

            )



        #
        # Trade grade
        #

        if trade_score >= 55:

            grade = "A+"


        elif trade_score >= 45:

            grade = "A"


        elif trade_score >= 35:

            grade = "B"


        elif trade_score >= 25:

            grade = "C"


        else:

            grade = "Avoid"



        trade_scores.append(
            trade_score
        )

        reward_risk_list.append(
            reward_risk
        )

        expected_value_list.append(
            expected_value
        )

        grade_list.append(
            grade
        )



        if position:

            shares_list.append(
                position["Shares"]
            )

            capital_list.append(
                position["Capital_Required"]
            )

            risk_per_share_list.append(
                position["Risk_Per_Share"]
            )


        else:

            shares_list.append(None)

            capital_list.append(None)

            risk_per_share_list.append(None)



    df["Trade_Score"] = trade_scores

    df["Trade_Grade"] = grade_list

    df["Reward_Risk"] = reward_risk_list

    df["Expected_Value"] = expected_value_list

    df["Recommended_Shares"] = shares_list

    df["Capital_Required"] = capital_list

    df["Risk_Per_Share"] = risk_per_share_list


    return df