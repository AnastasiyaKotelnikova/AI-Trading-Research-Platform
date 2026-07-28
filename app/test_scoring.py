from app.snapshot_loader import load_snapshot
from app.scoring import calculate_scores


def main():

    df = load_snapshot()

    df = calculate_scores(df)

    df = df.sort_values(
        "Scanner_Score",
        ascending=False
    )

    print("\n🔥 TOP SCANNER SCORES\n")

    print(
        df[
            [
                "Symbol",
                "Price",
                "Change_%",
                "RVOL",
                "Dollar_Volume",
                "Scanner_Score"
            ]
        ].head(20).to_string(index=False)
    )


if __name__ == "__main__":
    main()
