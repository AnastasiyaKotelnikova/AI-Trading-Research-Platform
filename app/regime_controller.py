import pandas as pd
import os


REGIME_FILE = (
    "data/market/market_regime_history.csv"
)



def get_current_regime():


    if not os.path.exists(REGIME_FILE):

        return {

            "Market_Regime":
                "UNKNOWN",

            "Exposure":
                50

        }



    df = pd.read_csv(
        REGIME_FILE
    )


    latest = df.iloc[-1]


    return {

        "Market_Regime":
            latest["Market_Regime"],

        "Exposure":
            latest["Recommended_Exposure_%"],

        "Score":
            latest["Market_Score"]

    }



def apply_regime_adjustment(
    allocation,
    regime
):


    exposure = regime["Exposure"]


    adjusted = (

        allocation *

        exposure /

        100

    )


    return round(
        adjusted,
        2
    )



if __name__ == "__main__":


    regime = get_current_regime()


    print(
        "\n========== CURRENT MARKET REGIME =========="
    )


    print(
        "Regime:",
        regime["Market_Regime"]
    )


    print(
        "Exposure:",
        regime["Exposure"],
        "%"
    )