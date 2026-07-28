import pandas as pd


INPUT_FILE = "data/cache/market_snapshot.csv"
OUTPUT_FILE = "data/cache/liquid_movers.csv"


# minimum requirements
MIN_PRICE = 1
MAX_PRICE = 1000
MIN_VOLUME = 300000
MIN_DOLLAR_VOLUME = 2000000


def scan_liquid_movers():

    df = pd.read_csv(INPUT_FILE)

    # remove missing data
    df = df.dropna()


    # price filter
    df = df[
        (df["Price"] >= MIN_PRICE) &
        (df["Price"] <= MAX_PRICE)
    ]


    # create dollar volume
    df["Dollar_Volume"] = (
        df["Price"] * df["Volume"]
    )


    # liquidity filters
    df = df[
        (df["Volume"] >= MIN_VOLUME) &
        (df["Dollar_Volume"] >= MIN_DOLLAR_VOLUME)
    ]


    # rank by movement
    df = df.sort_values(
        by="Change_%",
        ascending=False
    )


    df.insert(
        0,
        "Rank",
        range(1, len(df)+1)
    )


    df.to_csv(
        OUTPUT_FILE,
        index=False
    )


    print("\n🔥 LIQUID MOVERS")
    print(
        df.head(20)
        [["Rank",
          "Symbol",
          "Price",
          "Change_%",
          "Volume",
          "Dollar_Volume"]]
    )


    print("\nSaved:")
    print(OUTPUT_FILE)



if __name__ == "__main__":
    scan_liquid_movers()
