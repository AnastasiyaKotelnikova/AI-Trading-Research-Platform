import pandas as pd

from app.universe_loader import build_universe


def save_universe():

    symbols = build_universe()

    df = pd.DataFrame(symbols, columns=["Symbol"])

    output_file = "data/universe/all_symbols.csv"

    df.to_csv(output_file, index=False)

    print(f"Saved {len(df)} symbols")
    print(f"Output: {output_file}")


if __name__ == "__main__":
    save_universe()
