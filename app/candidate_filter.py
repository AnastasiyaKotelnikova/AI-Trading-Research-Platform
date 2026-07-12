import pandas as pd


INPUT_FILE = "data/cache/market_snapshot.csv"
OUTPUT_FILE = "data/cache/candidates.csv"


def filter_candidates():

    df = pd.read_csv(INPUT_FILE)


    # Basic quality filters
    filtered = df[
        (df["Price"] >= 5) &
        (df["Price"] <= 500) &
        (df["Dollar_Volume"] >= 20_000_000) &
        (df["RVOL"] >= 1.5) &
        (df["Change_%"] >= 3)
    ]


    filtered = filtered.sort_values(
        by=[
            "RVOL",
            "Change_%",
            "Dollar_Volume"
        ],
        ascending=False
    )


    filtered.to_csv(
        OUTPUT_FILE,
        index=False
    )


    print("\n🔥 CANDIDATES FOUND\n")

    print(
        filtered[
            [
                "Symbol",
                "Price",
                "Change_%",
                "RVOL",
                "Dollar_Volume"
            ]
        ].head(50).to_string(index=False)
    )


    print(
        f"\nTotal candidates: {len(filtered)}"
    )



if __name__ == "__main__":
    filter_candidates()