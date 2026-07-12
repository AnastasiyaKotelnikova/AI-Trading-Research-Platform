import pandas as pd


INPUT_FILE = "data/cache/market_snapshot.csv"
OUTPUT_FILE = "data/cache/liquid_momentum.csv"


# Filters
MIN_PRICE = 2
MIN_DOLLAR_VOLUME = 5_000_000
MIN_RVOL = 1.5


def scan_liquid_momentum():

    df = pd.read_csv(INPUT_FILE)


    # Remove bad data

    df = df.dropna(
        subset=[
            "Price",
            "Change_%",
            "Volume",
            "Dollar_Volume",
            "RVOL"
        ]
    )


    # -------------------------
    # Liquidity filter
    # -------------------------

    df = df[
        df["Price"] >= MIN_PRICE
    ]


    df = df[
        df["Dollar_Volume"] >= MIN_DOLLAR_VOLUME
    ]


    # -------------------------
    # Unusual volume filter
    # -------------------------

    df = df[
        df["RVOL"] >= MIN_RVOL
    ]



    # -------------------------
    # Rank by momentum
    # -------------------------

    gainers = (
        df.sort_values(
            "Change_%",
            ascending=False
        )
        .head(20)
    )


    gainers.insert(
        0,
        "Rank",
        range(1, len(gainers)+1)
    )


    print("\n🔥 LIQUID MOMENTUM STOCKS\n")

    print(
        gainers[
            [
                "Rank",
                "Symbol",
                "Price",
                "Change_%",
                "Volume",
                "RVOL",
                "Dollar_Volume"
            ]
        ].to_string(index=False)
    )


    gainers.to_csv(
        OUTPUT_FILE,
        index=False
    )


    print("\nSaved:")
    print(OUTPUT_FILE)



if __name__ == "__main__":

    scan_liquid_momentum()