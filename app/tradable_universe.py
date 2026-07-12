import pandas as pd


def build_tradable_universe():

    df = pd.read_csv(
        "data/universe/symbol_metadata.csv"
    )


    # Remove ETFs
    df = df[df["ETF"] == "N"]


    # Remove test securities
    df = df[df["Test Issue"] == "N"]


    # Remove strange symbols
    df = df[
        ~df["Symbol"].str.contains(
            r"[\.\$\/]",
            regex=True,
            na=False
        )
    ]


    # Keep only common stock names
    df = df[
        df["Security Name"].str.contains(
            "Common Stock",
            case=False,
            na=False
        )
    ]


    df = df.drop_duplicates(
        subset=["Symbol"]
    )


    output = "data/universe/tradable_symbols.csv"


    df.to_csv(
        output,
        index=False
    )


    print("Tradable universe created")
    print("Total stocks:", len(df))
    print("Saved:", output)


if __name__ == "__main__":
    build_tradable_universe()