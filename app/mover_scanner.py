import pandas as pd


INPUT_FILE = "data/cache/market_snapshot.csv"
OUTPUT_FILE = "data/cache/top_movers.csv"


def analyze_movers():

    df = pd.read_csv(INPUT_FILE)

    # remove symbols with missing prices
    df = df.dropna(subset=["Price", "Change_%"])


    # convert change to number
    df["Change_%"] = pd.to_numeric(
        df["Change_%"],
        errors="coerce"
    )

    df = df.dropna(subset=["Change_%"])


    # sort biggest moves first
    df = df.sort_values(
        by="Change_%",
        ascending=False
    )


    # add ranking
    df.insert(
        0,
        "Rank",
        range(1, len(df)+1)
    )


    df.to_csv(
        OUTPUT_FILE,
        index=False
    )


    print("\n🔥 TOP GAINERS")
    print(
        df.head(10)[
            ["Rank", "Symbol", "Price", "Change_%"]
        ]
    )


    print("\n🔻 TOP LOSERS")

    print(
        df.tail(10)[
            ["Rank", "Symbol", "Price", "Change_%"]
        ]
    )


    print("\nSaved:", OUTPUT_FILE)



if __name__ == "__main__":
    analyze_movers()