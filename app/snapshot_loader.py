import pandas as pd


SNAPSHOT_FILE = "data/cache/market_snapshot.csv"


def load_snapshot():

    df = pd.read_csv(SNAPSHOT_FILE)

    # Remove rows with missing prices
    df = df.dropna(subset=["Price"])

    return df


if __name__ == "__main__":

    df = load_snapshot()

    print(df.head())
    print()
    print(f"Loaded {len(df)} stocks")