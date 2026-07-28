from app.snapshot_loader import load_snapshot
from app.filters import apply_filters
from app.scoring import calculate_scores


def main():

    df = load_snapshot()


    # Apply trading criteria
    df = apply_filters(
        df,
        min_price=5,
        max_price=1200,
        min_change=3,
        min_volume=500_000,
        min_rvol=2,
        min_dollar_volume=25_000_000
    )


    # Add score
    df = calculate_scores(df)


    # Rank
    df = df.sort_values(
        "Scanner_Score",
        ascending=False
    )


    print("\n🔥 FILTERED MOMENTUM SCANNER\n")


    print(
        df[
            [
                "Symbol",
                "Price",
                "Change_%",
                "RVOL",
                "Volume",
                "Dollar_Volume",
                "Scanner_Score"
            ]
        ]
        .head(30)
        .to_string(index=False)
    )


    print()
    print("Stocks found:", len(df))


if __name__ == "__main__":
    main()
