import pandas as pd


def build_metadata():

    # NASDAQ securities
    nasdaq = pd.read_csv(
        "data/universe/nasdaqlisted.txt",
        sep="|"
    )

    nasdaq = nasdaq[
        [
            "Symbol",
            "Security Name",
            "Market Category",
            "ETF",
            "Test Issue"
        ]
    ]

    nasdaq["Exchange"] = "NASDAQ"


    # NYSE / AMEX / other listed
    other = pd.read_csv(
        "data/universe/otherlisted.txt",
        sep="|"
    )

    other = other[
        [
            "ACT Symbol",
            "Security Name",
            "Exchange",
            "ETF",
            "Test Issue"
        ]
    ]

    other = other.rename(
        columns={
            "ACT Symbol": "Symbol"
        }
    )


    # Combine
    df = pd.concat(
        [nasdaq, other],
        ignore_index=True
    )


    # Clean
    df["Symbol"] = df["Symbol"].astype(str).str.strip()

    df = df.drop_duplicates(
        subset=["Symbol"]
    )


    # Remove obvious non-symbol rows from NASDAQ files
    df = df[
        ~df["Symbol"].isin(["Symbol"])
    ]


    # Save
    output = "data/universe/symbol_metadata.csv"

    df.to_csv(
        output,
        index=False
    )


    print("Metadata created")
    print("Total symbols:", len(df))
    print("Saved:", output)


if __name__ == "__main__":
    build_metadata()
