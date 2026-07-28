import os
import pandas as pd


LEARNING_FILE = (
    "data/models/trading_setup_analysis.csv"
)

def calculate_risk_reward(df):

    df = df.copy()

    required = [
        "Entry_Price",
        "Stop_Loss",
        "Target_1"
    ]

    for col in required:
        if col not in df.columns:
            df["Risk_Reward"] = 0
            return df


    risk = (
        df["Entry_Price"]
        -
        df["Stop_Loss"]
    )


    reward = (
        df["Target_1"]
        -
        df["Entry_Price"]
    )


    df["Risk_Reward"] = (

        reward
        /
        risk.replace(0, 0.01)

    ).round(2)


    df["Risk_Reward"] = (

        df["Risk_Reward"]
        .clip(0,5)

    )


    return df



def apply_learning_adjustment(df):

    """
    Adaptive AI learning adjustment using historical setup performance.

    Uses:
    - Historical win rate
    - Number of trades
    - Confidence based on sample size
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
                    row["Trades"]
                )



                # --------------------------------
                # Confidence factor
                #
                # More trades = stronger learning
                #
                # 10 trades  = 10%
                # 50 trades  = 50%
                # 100+       = 100%
                # --------------------------------

                confidence = min(
                    trades / 100,
                    1
                )



                # --------------------------------
                # Negative learning
                # --------------------------------

                if win_rate < 50:

                    penalty = (

                        (50 - win_rate)

                        /

                        50

                        *

                     8

                    )


                    adjustment -= min(
                        penalty * confidence,
                        8
                    )


                # --------------------------------
                # Positive learning
                # --------------------------------

                else:


                    bonus = (

                        (win_rate - 50)

                        /

                        50

                        *

                        3

                    )


                    adjustment += min(
                        bonus * confidence,
                        5
                    )



        final_score = score + adjustment


        final_score = max(
            final_score,
            score - 8
        )


        final_score = min(
            final_score,
            score + 5
        )


        return final_score



    df["AI_Learned_Score"] = (

        df["AI_Final_Score"]

        .apply(adjust)

        .round(2)

    )


    return df





def add_ai_score(df):

    df = df.copy()

    # Risk_Reward already calculated in integrated_scanner.py


    # -----------------------------------
    # Safety defaults
    # -----------------------------------

    defaults = {

        "Rank_Score": 0,

        "ML_Probability": 0,

        "Historical_ML_Probability": 0,

        "Risk_Reward": 0,

        "Market_Regime_Score": 0

    }


    for col, value in defaults.items():

        if col not in df.columns:

            df[col] = value



    # -----------------------------------
    # Market regime scoring
    # -----------------------------------

    if "Market_Regime" in df.columns:


        def regime_score(x):

            if x == "Bullish":

                return 100

            elif x == "Neutral":

                return 50

            elif x == "Bearish":

                return 20

            else:

                return 0


        df["Market_Regime_Score"] = (
            df["Market_Regime"]
            .apply(regime_score)
        )



    # -----------------------------------
    # Combined ML Intelligence
    # -----------------------------------

    df["Combined_ML_Probability"] = (

        df["ML_Probability"] * 0.70

        +

        df["Historical_ML_Probability"] * 0.30

    ).round(2)



    # -----------------------------------
    # Technical score
    # -----------------------------------

    technical_score = (

        df["Rank_Score"]

        /

        100

        *

        40

    )



    # -----------------------------------
    # ML score
    # -----------------------------------

    ml_score = (

        df["Combined_ML_Probability"]

        /

        100

        *

        25

    )



    # -----------------------------------
    # Historical ML score
    # -----------------------------------

    historical_ml_score = (

        df["Historical_ML_Probability"]

        /

        100

        *

        20

    )



    # -----------------------------------
    # Risk reward scoring
    # -----------------------------------

    def risk_reward_points(rr):

        if rr < 1:

            return 0

        elif rr < 2:

            return 5

        elif rr < 3:

            return 10

        else:

            return 15



    risk_score = (

        df["Risk_Reward"]

        .apply(
            risk_reward_points
        )

    )



    # -----------------------------------
    # Market regime score
    # -----------------------------------

    market_score = (

        df["Market_Regime_Score"]

        /

        100

        *

        5

    )



    # -----------------------------------
    # Base AI score
    # -----------------------------------

    df["AI_Final_Score"] = (

        technical_score

        +

        ml_score

        +

        historical_ml_score

        +

        risk_score

        +

        market_score

    )



    df["AI_Final_Score"] = (

        df["AI_Final_Score"]

        .clip(0,100)

        .round(2)

    )



    # -----------------------------------
    # Historical learning
    # -----------------------------------

    df = apply_learning_adjustment(
        df
    )



    # -----------------------------------
    # Final AI score
    # -----------------------------------

    df["AI_Final_Score_Adjusted"] = (

        df["AI_Learned_Score"]

    ).round(2)



    return df.sort_values(

        "AI_Final_Score_Adjusted",

        ascending=False

    )