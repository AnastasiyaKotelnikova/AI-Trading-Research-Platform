import pandas as pd
import os
from datetime import datetime


INPUT_FILE = "data/trade_database.csv"

OUTPUT_FILE = "data/results/trade_quality_report.csv"


def load_data():

    print("\nLoading trade database...")

    df = pd.read_csv(
        INPUT_FILE,
        low_memory=False
    )

    print(f"Total trades loaded: {len(df)}")

    return df



def calculate_metrics(df):

    print("\nCalculating trade quality metrics...")


    # Convert returns
    df["Return_%"] = pd.to_numeric(
        df["Return_%"],
        errors="coerce"
    )


    # Determine outcome quality

    df["Win"] = (
        df["Result"]
        .astype(str)
        .str.contains(
            "TARGET",
            case=False,
            na=False
        )
    )


    df["Loss"] = (
        df["Result"]
        .astype(str)
        .str.contains(
            "STOP",
            case=False,
            na=False
        )
    )


    # Group by strategy signals

    grouped = df.groupby(
        [
            "Signal",
            "Strategy",
            "Model_Name"
        ]
    ).agg(

        Trades=("Symbol","count"),

        Symbols=("Symbol","nunique"),

        Win_Rate=("Win","mean"),

        Average_Return=("Return_%","mean"),

        Avg_Win=(
            "Return_%",
            lambda x: x[x > 0].mean()
        ),

        Avg_Loss=(
            "Return_%",
            lambda x: x[x < 0].mean()
        ),

        Profit_Factor=(
            "Return_%",
            lambda x:
            x[x > 0].sum() /
            abs(x[x < 0].sum())
            if abs(x[x < 0].sum()) > 0
            else 0
        )

    ).reset_index()



    grouped["Win_Rate"] = (
        grouped["Win_Rate"] * 100
    ).round(2)


    grouped["Average_Return"] = (
        grouped["Average_Return"]
        .round(2)
    )


    grouped["Reliability_Score"] = (
        grouped["Win_Rate"] * 0.4
        +
        grouped["Profit_Factor"] * 10
        +
        grouped["Trades"].clip(0,100) / 10
    ).round(2)


    grouped = grouped.sort_values(
        "Reliability_Score",
        ascending=False
    )


    return grouped



def save_report(report):

    os.makedirs(
        "data/results",
        exist_ok=True
    )


    report["Analysis_Date"] = (
        datetime.now()
    )


    report.to_csv(
        OUTPUT_FILE,
        index=False
    )


    print(
        f"\nSaved: {OUTPUT_FILE}"
    )



def main():

    df = load_data()

    report = calculate_metrics(df)

    print("\n===== TRADE QUALITY RESULTS =====\n")

    print(
        report.head(10)
        .to_string(index=False)
    )


    save_report(report)



if __name__ == "__main__":
    main()