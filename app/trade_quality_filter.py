import pandas as pd
import json
import os


DEFAULT_THRESHOLDS = {

    "Rank_Score": 50,

    "Research_Score": 80,

    "Risk_Reward": 1.5,

    "AI_Confidence": 25,

    "Combined_ML_Strength": 40

}



def load_thresholds():

    path = "data/models/optimal_thresholds.json"


    if os.path.exists(path):

        with open(path, "r") as f:

            thresholds = json.load(f)


        final = DEFAULT_THRESHOLDS.copy()

        final.update(thresholds)


        print("\n======================================")
        print(" LOADED QUALITY THRESHOLDS")
        print("======================================")

        print("Rank Score        :", final["Rank_Score"])
        print("Research Score    :", final["Research_Score"])
        print("Risk Reward       :", final["Risk_Reward"])
        print("AI Confidence     :", final["AI_Confidence"])
        print("Combined ML       :", final["Combined_ML_Strength"])

        print()


        return final



    print("\n======================================")
    print(" USING DEFAULT THRESHOLDS")
    print("======================================")

    return DEFAULT_THRESHOLDS.copy()





def load_optimal_thresholds():

    return load_thresholds()






def apply_trade_quality_filter(df):


    df = df.copy()


    thresholds = load_thresholds()


    print("\nLoaded Quality Thresholds:")
    print(thresholds)



    # --------------------------------
    # Default
    # --------------------------------

    df["Trade_Quality"] = "WATCH"





    # --------------------------------
    # Minimum price
    # --------------------------------

    df.loc[
        df["Price"] < 10,
        "Trade_Quality"
    ] = "REJECT"





    # --------------------------------
    # AI confidence
    # --------------------------------

    df.loc[
        df["AI_Confidence"] < thresholds["AI_Confidence"],
        "Trade_Quality"
    ] = "REJECT"





    # --------------------------------
    # Combined ML strength
    # --------------------------------

    df["Combined_ML_Strength"] = (

        df["ML_Probability"] * 0.40

        +

        df["Historical_ML_Probability"] * 0.60

    )



    df.loc[
        df["Combined_ML_Strength"] < thresholds["Combined_ML_Strength"],
        "Trade_Quality"
    ] = "REJECT"





    # --------------------------------
    # Research support
    # --------------------------------

    df.loc[
        df["Research_Score"] < thresholds["Research_Score"],
        "Trade_Quality"
    ] = "REJECT"





    # --------------------------------
    # Rank quality
    # --------------------------------

    df.loc[
        df["Rank_Score"] < thresholds["Rank_Score"],
        "Trade_Quality"
    ] = "REJECT"





    # --------------------------------
    # Risk reward
    # --------------------------------

    df.loc[
        df["Risk_Reward"] < thresholds["Risk_Reward"],
        "Trade_Quality"
    ] = "REJECT"







         # =================================
    # FINAL QUALITY CLASSIFICATION
    # =================================

    df["Trade_Quality"] = "WATCH"


    # HIGH QUALITY
    df.loc[
        (
            (df["Rank_Score"] >= thresholds["Rank_Score"])
            &
            (df["AI_Confidence"] >= thresholds["AI_Confidence"])
            &
            (df["Combined_ML_Strength"] >= thresholds["Combined_ML_Strength"])
            &
            (df["Research_Score"] >= thresholds["Research_Score"])
            &
            (df["Risk_Reward"] >= thresholds["Risk_Reward"])
        ),
        "Trade_Quality"
    ] = "HIGH QUALITY"


    # QUALITY
    df.loc[
        (
            (df["Trade_Quality"] == "WATCH")
            &
            (df["Rank_Score"] >= 60)
            &
            (df["AI_Confidence"] >= 30)
            &
            (df["Combined_ML_Strength"] >= 40)
            &
            (df["Risk_Reward"] >= 2)
        ),
        "Trade_Quality"
    ] = "QUALITY"


    # REJECT ONLY IF REALLY BAD
    df.loc[
        (
            (df["AI_Confidence"] < 25)
            |
            (df["Combined_ML_Strength"] < 30)
            |
            (df["Rank_Score"] < 20)
            |
            (df["Risk_Reward"] < 1.5)
        ),
        "Trade_Quality"
    ] = "REJECT"


    return df