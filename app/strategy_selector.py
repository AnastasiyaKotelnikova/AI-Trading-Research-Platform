import pandas as pd


DATABASE = "data/trade_database.csv"


def load_data():

    return pd.read_csv(
        DATABASE
    )



def classify_strategy(df):

    results = []


    for _, row in df.iterrows():

        strategy = "WATCH"


        # Strong Pullback
        if (
            row["Return_20D"] > 10
            and row["Return_5D"] < -2
            and 50 <= row["RSI"] <= 60
            and row["Rank_Score"] >= 80
        ):
            strategy = "PULLBACK CONTINUATION"


        # Pullback
        elif (
            row["Return_20D"] > 10
            and row["Return_5D"] < 0
            and 50 <= row["RSI"] <= 60
        ):
            strategy = "PULLBACK CONTINUATION"


        # Quality
        elif (
            row["Rank_Score"] >= 80
            and row["Trend_Score"] >= 15
            and row["Risk_Reward"] >= 2.5
        ):
            strategy = "QUALITY SETUP"


        # Momentum
        elif (
            row["Momentum_Score"] >= 20
            and row["Return_20D"] > 15
        ):
            strategy = "MOMENTUM"


        results.append(strategy)


    df["Strategy"] = results

    return df

def main():

    print("\n===== STRATEGY SELECTOR =====\n")


    df = load_data()

    df = classify_strategy(df)



    print(
        df["Strategy"]
        .value_counts()
    )


    print("\nTOP STRATEGIES\n")


    print(
        df[
            df["Strategy"] != "AVOID"
        ]
        [
            [
                "Symbol",
                "Strategy",
                "Return_%",
                "Rank_Score",
                "RSI",
                "Return_20D",
                "Return_5D"
            ]
        ]
        .head(30)
    )


    df.to_csv(
        "data/analysis/strategy_results.csv",
        index=False
    )



if __name__ == "__main__":

    main()
