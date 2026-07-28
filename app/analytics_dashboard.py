import os
import pandas as pd

DATABASE = "data/trade_database.csv"


def load_database():

    if not os.path.exists(DATABASE):
        print("Database not found.")
        return None

    return pd.read_csv(DATABASE)


def run():

    df = load_database()

    if df is None:
        return

    print("\n========== ANALYTICS DASHBOARD ==========\n")

    print("Total Trades:")
    print(len(df))

    if "Return_%" in df.columns:
        print("\nAverage Return:")
        print(round(df["Return_%"].mean(), 2), "%")

    if "Status" in df.columns:

        print("\nStatus Summary:")
        print(df["Status"].value_counts())

    if "Strategy" in df.columns:

        print("\nStrategy Performance:")
        print(
            df.groupby("Strategy")["Return_%"]
            .mean()
            .sort_values(ascending=False)
        )

    if "Sector" in df.columns:

        print("\nSector Performance:")
        print(
            df.groupby("Sector")["Return_%"]
            .mean()
            .sort_values(ascending=False)
        )

    if "Confidence_Score" in df.columns:

        print("\nConfidence Score Performance:")
        print(
            df.groupby("Confidence_Score")["Return_%"]
            .mean()
            .sort_values(ascending=False)
        )

    if "Research_Score" in df.columns:

        print("\nTop Research Scores:")
        print(
            df[
                [
                    "Symbol",
                    "Research_Score",
                    "Return_%"
                ]
            ]
            .sort_values(
                "Research_Score",
                ascending=False
            )
            .head(20)
        )


if __name__ == "__main__":

    run()
