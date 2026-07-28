import os
import pandas as pd


LEARNING_FILE = (
    "data/models/trading_setup_analysis.csv"
)



def apply_learning_adjustment(df):


    """
    Adaptive AI learning adjustment.

    Purpose:
    - Learn from historical AI score performance
    - Adjust ranking slightly
    - Avoid destroying good setups

    Limits:
    Negative adjustment: -8 max
    Positive adjustment: +5 max
    """



    if not os.path.exists(LEARNING_FILE):

        df["AI_Learned_Score"] = (
            df["AI_Final_Score"]
        )

        return df



    learning = pd.read_csv(
        LEARNING_FILE
    )



    ai_rules = learning[

        learning["Category_Type"]

        ==

        "AI_SCORE"

    ]



    def adjust(score):


        if pd.isna(score):

            return score



        adjustment = 0



        for _, row in ai_rules.iterrows():


            category = row["Category"]


            try:

                low, high = (

                    category

                    .replace("(","")

                    .replace("]","")

                    .split(",")

                )


                low = float(low)

                high = float(high)


            except:

                continue



            if low <= score <= high:


                win_rate = float(
                    row["Win_Rate"]
                )


                trades = float(
                    row.get(
                        "Trades",
                        0
                    )
                )



                # -----------------------------
                # Learning confidence
                #
                # More historical examples
                # = stronger adjustment
                # -----------------------------

                confidence = min(
                    trades / 100,
                    1
                )



                # -----------------------------
                # Negative historical pattern
                # -----------------------------

                if win_rate < 50:


                    penalty = (

                        (50 - win_rate)

                        /

                        50

                        *

                        8

                    )


                    adjustment -= (

                        penalty

                        *

                        confidence

                    )



                # -----------------------------
                # Positive historical pattern
                # -----------------------------

                else:


                    bonus = (

                        (win_rate - 50)

                        /

                        50

                        *

                        3

                    )


                    adjustment += (

                        bonus

                        *

                        confidence

                    )



        # -----------------------------
        # Protect AI base score
        # -----------------------------

        adjustment = max(
            adjustment,
            -8
        )


        adjustment = min(
            adjustment,
            5
        )



        final_score = (

            score

            +

            adjustment

        )



        return max(
            final_score,
            0
        )



    df["AI_Learned_Score"] = (

        df["AI_Final_Score"]

        .apply(adjust)

        .round(2)

    )



    return df