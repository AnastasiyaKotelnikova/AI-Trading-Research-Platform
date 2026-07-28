import pandas as pd


DATABASE = "data/trade_database.csv"


def analyze():

    df = pd.read_csv(DATABASE)

    print("\n===== ENTRY ANALYSIS =====\n")


    factors = [
        "Return_5D",
        "Return_20D",
        "Distance_From_High_%",
        "RSI"
    ]


    for factor in factors:

        if factor not in df.columns:
            print(f"{factor} missing")
            continue


        print("\n--------------------")
        print(factor)


        df["Group"] = pd.qcut(
            df[factor],
            4,
            duplicates="drop"
        )


        print(
            df.groupby(
                "Group",
                observed=True
            )
            .agg(
                Trades=("Return_%","count"),
                Win_Rate=(
                    "Return_%",
                    lambda x: round((x>0).mean()*100,2)
                ),
                Avg_Return=("Return_%","mean")
            )
        )


if __name__ == "__main__":
    analyze()
