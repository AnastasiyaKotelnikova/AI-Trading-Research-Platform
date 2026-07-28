import pandas as pd


DATABASE = "data/analysis/strategy_results.csv"


def main():

    print("\n===== STRATEGY SECTOR ANALYSIS =====\n")


    df = pd.read_csv(
        DATABASE
    )


    strategies = [
        "PULLBACK CONTINUATION",
        "QUALITY SETUP",
        "MOMENTUM"
    ]


    for strategy in strategies:

        print("\n========================")
        print(strategy)
        print("========================\n")


        temp = df[
            df["Strategy"] == strategy
        ]


        if len(temp) == 0:
            continue


        result = (
            temp
            .groupby("Sector")
            .agg(
                Trades=("Symbol","count"),
                Win_Rate=(
                    "Return_%",
                    lambda x:
                    round(
                        (x > 0).mean()*100,
                        2
                    )
                ),
                Avg_Return=(
                    "Return_%",
                    "mean"
                )
            )
            .sort_values(
                "Avg_Return",
                ascending=False
            )
        )


        result["Avg_Return"] = result["Avg_Return"].round(2)


        print(result)


    df.to_csv(
        "data/analysis/strategy_sector_results.csv",
        index=False
    )


if __name__ == "__main__":
    main()
