import pandas as pd
import os
import numpy as np


INPUT = "data/analysis/strategy_results.csv"

OUTPUT = "data/analysis/research_ranked.csv"



def load_data():

    return pd.read_csv(INPUT)



def normalize(series):

    if series.max() == series.min():
        return pd.Series(
            [50] * len(series),
            index=series.index
        )

    return (
        (series - series.min())
        /
        (series.max() - series.min())
        *
        100
    )



def calculate_research_score(df):


    # =====================================
    # Normalize individual factors
    # =====================================


    rank_score = normalize(
        df["Rank_Score"]
    )


    momentum_score = normalize(
        df["Momentum_Score"]
    )


    trend_score = normalize(
        df["Trend_Score"]
    )


    relative_strength = normalize(
        df["Relative_Strength"]
    )


    risk_reward = normalize(
        df["Risk_Reward"]
    )


    return_score = normalize(
        df["Return_%"]
    )



    # =====================================
    # Technical bonuses
    # =====================================


    technical_bonus = pd.Series(
        0,
        index=df.index
    )


    technical_bonus += (
        df["Above_SMA20"]
        .astype(int)
        * 5
    )


    technical_bonus += (
        df["Above_SMA50"]
        .astype(int)
        * 5
    )


    technical_bonus += (
        df["Breakout"]
        .astype(int)
        * 10
    )


    technical_bonus -= (
        df["Overextended"]
        .astype(int)
        * 10
    )



    # =====================================
    # Weighted Research Model
    # =====================================


    raw_score = (

        rank_score * 0.30

        +

        momentum_score * 0.15

        +

        trend_score * 0.15

        +

        relative_strength * 0.15

        +

        risk_reward * 0.15

        +

        return_score * 0.10

        +

        technical_bonus

    )



    df["Raw_Research_Score"] = (
        raw_score
    )



    # =====================================
    # Percentile ranking
    # =====================================


    df["Research_Score"] = (

        df["Raw_Research_Score"]
        .rank(
            pct=True
        )

        *

        100

    ).round(2)



    return df




def main():


    print(
        "\n===== RESEARCH RANKER V2 =====\n"
    )


    df = load_data()


    df = calculate_research_score(
        df
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


    print(
        "\nSaved:"
    )

    print(
        OUTPUT
    )



if __name__ == "__main__":

    main()