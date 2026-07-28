import pandas as pd



def add_ai_confidence(df):


    df = df.copy()


    # -----------------------------
    # Safety defaults
    # -----------------------------

    defaults = {

        "ML_Probability": 0,

        "Historical_ML_Probability": 0,

        "Risk_Reward": 0,

        "Rank_Score": 0,

        "Market_Regime_Score": 0

    }


    for col, value in defaults.items():

        if col not in df.columns:

            df[col] = value



    # -----------------------------
    # Confidence Components
    # -----------------------------


    ml_confidence = (

        df["ML_Probability"]

        * 0.40

    )


    historical_confidence = (

        df["Historical_ML_Probability"]

        * 0.20

    )


    technical_confidence = (

        df["Rank_Score"]

        / 100

        * 25

    )


    risk_confidence = (

        df["Risk_Reward"]

        .clip(0,5)

        / 5

        * 10

    )


    market_confidence = (

        df["Market_Regime_Score"]

        / 100

        * 5

    )



    df["AI_Confidence"] = (

        ml_confidence

        +

        historical_confidence

        +

        technical_confidence

        +

        risk_confidence

        +

        market_confidence

    )



    df["AI_Confidence"] = (

        df["AI_Confidence"]

        .clip(0,100)

        .round(2)

    )



    # -----------------------------
    # Confidence Level
    # -----------------------------


    def confidence_label(x):


        if x >= 80:

            return "HIGH"


        elif x >= 60:

            return "MEDIUM"


        elif x >= 40:

            return "LOW"


        else:

            return "VERY LOW"




    df["AI_Confidence_Level"] = (

        df["AI_Confidence"]

        .apply(confidence_label)

    )



    return df