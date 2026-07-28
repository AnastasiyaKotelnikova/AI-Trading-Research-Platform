import pandas as pd
from datetime import datetime
import os


DATABASE = "data/analysis/research_ranked.csv"

def load_data():

    return pd.read_csv(DATABASE)



def market_summary(df):

    print("\n===== MARKET RESEARCH REPORT =====\n")

    print(
        "Generated:",
        datetime.now()
    )


    print("\n===== SIGNAL DISTRIBUTION =====\n")

    print(
        df["Strategy"]
        .value_counts()
    )



def sector_analysis(df):

    print("\n===== BEST SECTORS =====\n")

    sector = (
        df[df["Strategy"] != "WATCH"]
        .groupby("Sector")["Return_%"]
        .agg(
            [
                "count",
                "mean"
            ]
        )
        .sort_values(
            "mean",
            ascending=False
        )
    )


    print(
        sector.head(10)
    )



def top_candidates(df):

    print("\n===== TOP RESEARCH CANDIDATES =====\n")


    cols = [
        "Symbol",
        "Sector",
        "Strategy",
        "Research_Score",
        "Return_%",
        "Rank_Score",
        "RSI",
        "Risk_Reward"
    ]


    result = (
        df[df["Strategy"] != "WATCH"]
        .sort_values(
            [
                "Research_Score",
                "Rank_Score"
            ],
            ascending=False
        )
        [cols]
        .head(20)
    )


    print(result)
def save_report(df):

    os.makedirs(
        "data/reports",
        exist_ok=True
    )


    filename = (
        "data/reports/"
        +
        datetime.now().strftime(
            "%Y-%m-%d_%H-%M"
        )
        +
        "_research_report.csv"
    )


    df.to_csv(
        filename,
        index=False
    )


    print("\nSaved:")
    print(filename)



def main():

    df = load_data()


    market_summary(df)

    sector_analysis(df)

    top_candidates(df)

    save_report(df)



if __name__ == "__main__":

    main()
