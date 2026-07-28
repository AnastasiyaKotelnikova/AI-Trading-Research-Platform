import pandas as pd


DATABASE = "data/analysis/strategy_results.csv"


def main():

    print("\n===== STRATEGY BACKTEST =====\n")


    df = pd.read_csv(DATABASE)


    strategies = [
        "PULLBACK CONTINUATION",
        "QUALITY SETUP",
        "MOMENTUM"
    ]


    results = []


    for strategy in strategies:

        temp = df[
            df["Strategy"] == strategy
        ]


        if len(temp) == 0:
            continue


        wins = temp[
            temp["Return_%"] > 0
        ]


        results.append(
            {
                "Strategy": strategy,
                "Trades": len(temp),
                "Win_Rate": round(
                    len(wins) / len(temp) * 100,
                    2
                ),
                "Avg_Return": round(
                    temp["Return_%"].mean(),
                    2
                ),
                "Best": round(
                    temp["Return_%"].max(),
                    2
                ),
                "Worst": round(
                    temp["Return_%"].min(),
                    2
                )
            }
        )


    result_df = pd.DataFrame(results)


    print(result_df)


    result_df.to_csv(
        "data/analysis/strategy_performance.csv",
        index=False
    )


if __name__ == "__main__":
    main()
