import pandas as pd


DATABASE = "data/analysis/strategy_results.csv"


def add_strategy_score(df):

    strategy_bonus = {

        "PULLBACK CONTINUATION": 15,
        "QUALITY SETUP": 10,
        "MOMENTUM": 5,
        "AVOID": 0
    }


    sector_bonus = {

        "Healthcare": 10,
        "Financial Services": 5,
        "Communication Services": 3,
        "Industrials": 0,
        "Technology": -5,
        "Consumer Cyclical": -5
    }


    df["Strategy_Bonus"] = (
        df["Strategy"]
        .map(strategy_bonus)
        .fillna(0)
    )


    df["Sector_Bonus"] = (
        df["Sector"]
        .map(sector_bonus)
        .fillna(0)
    )


    df["Optimized_Score"] = (
        df["Rank_Score"]
        +
        df["Strategy_Bonus"]
        +
        df["Sector_Bonus"]
    )


    return df



def main():

    print("\n===== STRATEGY OPTIMIZER =====\n")


    df = pd.read_csv(
        DATABASE
    )


    df = add_strategy_score(
        df
    )


    print(
        df[
            [
                "Symbol",
                "Sector",
                "Strategy",
                "Rank_Score",
                "Optimized_Score"
            ]
        ]
        .sort_values(
            "Optimized_Score",
            ascending=False
        )
        .head(20)
    )


    df.to_csv(
        "data/analysis/optimized_results.csv",
        index=False
    )



if __name__ == "__main__":
    main()
