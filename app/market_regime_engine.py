import os
import pandas as pd
from datetime import datetime


OUTPUT_FOLDER = "data/market"
OUTPUT_FILE = "data/market/market_regime_history.csv"


def calculate_market_score(row):

    score = 0


    # ----------------------------------------
    # SPY Trend
    # ----------------------------------------

    if row.get("SPY_Above_SMA50", False):

        score += 30


    # ----------------------------------------
    # QQQ Trend
    # ----------------------------------------

    if row.get("QQQ_Above_SMA50", False):

        score += 30


    # ----------------------------------------
    # Momentum
    # ----------------------------------------

    if row.get("Momentum_Positive", False):

        score += 20


    # ----------------------------------------
    # Volatility
    # ----------------------------------------

    if row.get("Low_Volatility", False):

        score += 20


    return score



def classify_regime(score):


    if score >= 80:

        return (
            "STRONG_BULL",
            100
        )


    elif score >= 60:

        return (
            "BULL",
            80
        )


    elif score >= 40:

        return (
            "NEUTRAL",
            50
        )


    elif score >= 20:

        return (
            "BEAR",
            30
        )


    else:

        return (
            "CRASH",
            0
        )



def generate_market_regime(
    market_data
):


    print(
        "\n========== MARKET REGIME ENGINE =========="
    )


    os.makedirs(
        OUTPUT_FOLDER,
        exist_ok=True
    )


    results = []


    for _, row in market_data.iterrows():


        score = calculate_market_score(
            row
        )


        regime, exposure = classify_regime(
            score
        )


        results.append(

            {

                "Date":
                    row.get(
                        "Date",
                        datetime.now()
                    ),


                "Market_Score":
                    score,


                "Market_Regime":
                    regime,


                "Recommended_Exposure_%":
                    exposure

            }

        )



    result_df = pd.DataFrame(
        results
    )



    result_df.to_csv(
        OUTPUT_FILE,
        index=False
    )



    print(
        result_df
    )


    print(
        "\nSaved:"
    )

    print(
        OUTPUT_FILE
    )


    return result_df



# =================================================
# TEST MODE
# =================================================

if __name__ == "__main__":


    sample_data = pd.DataFrame(

        [

            {

                "Date":
                    datetime.now(),


                "SPY_Above_SMA50":
                    True,


                "QQQ_Above_SMA50":
                    True,


                "Momentum_Positive":
                    True,


                "Low_Volatility":
                    True

            }

        ]

    )


    generate_market_regime(
        sample_data
    )