import pandas as pd
import os
import numpy as np


INPUT = "data/analysis/strategy_results.csv"

OUTPUT = "data/analysis/research_ranked.csv"


def load_data():

    return pd.read_csv(INPUT)



def percentile_score(series):

    return (
        series.rank(pct=True) * 100
    )



def calculate_research_score(df):


    # =====================================
    # NORMALIZED FEATURES
    # =====================================

    df["Rank_Percentile"] = percentile_score(
        df["Rank_Score"]
    )


    df["Momentum_Percentile"] = percentile_score(
        df["Momentum_Score"]
    )


    df["Trend_Percentile"] = percentile_score(
        df["Trend_Score"]
    )


    df["Relative_Strength_Percentile"] = percentile_score(
        df["Relative_Strength"]
    )


    # Cap extreme risk reward values

    df["Risk_Reward_Capped"] = (
        df["Risk_Reward"]
        .clip(
            upper=8
        )
    )


    df["RiskReward_Percentile"] = percentile_score(
        df["Risk_Reward_Capped"]
    )


    # =====================================
    # STRATEGY QUALITY
    # =====================================


    strategy_scores = {

        "STRONG PULLBACK": 90,

        "PULLBACK CONTINUATION": 85,

        "QUALITY SETUP": 80,

        "MOMENTUM": 75,

        "WATCH": 60

    }


    df["Strategy_Score"] = (
        df["Strategy"]
        .map(strategy_scores)
        .fillna(50)
    )



    # =====================================
    # FINAL RESEARCH SCORE
    # =====================================


    df["Research_Score"] = (

        df["Rank_Percentile"] * 0.25

        +

        df["Momentum_Percentile"] * 0.15

        +

        df["Trend_Percentile"] * 0.15

        +

        df["Relative_Strength_Percentile"] * 0.20

        +

        df["RiskReward_Percentile"] * 0.15

        +

        df["Strategy_Score"] * 0.10

    )


    df["Research_Score"] = (
        df["Research_Score"]
        .round(2)
    )


    return df



def main():


    print("\n===== RESEARCH RANKER V3 =====\n")


    df = load_data()


    df = calculate_research_score(df)


    print(
        "\nResearch Score Distribution:"
    )


    print(
        df["Research_Score"]
        .describe()
    )



    result = (

        df.sort_values(
            "Research_Score",
            ascending=False
        )
        [
            [
                "Symbol",
                "Sector",
                "Strategy",
                "Research_Score",
                "Rank_Score",
                "Momentum_Score",
                "Trend_Score",
                "Relative_Strength",
                "Risk_Reward",
                "Return_%"
            ]
        ]

        .head(25)

    )


    print(result)



    os.makedirs(
        "data/analysis",
        exist_ok=True
    )


    df.to_csv(
        OUTPUT,
        index=False
    )


    print("\nSaved:")
    print(OUTPUT)



if __name__ == "__main__":
    main()