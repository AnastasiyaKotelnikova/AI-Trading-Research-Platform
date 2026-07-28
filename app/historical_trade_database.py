import os
import pandas as pd


SIGNAL_FOLDER = "data/signal_history"
BACKTEST_FOLDER = "data/backtest_results"

DATABASE_FILE = "data/historical_trade_database.csv"



def latest_file(folder):

    files = [
        os.path.join(folder, f)
        for f in os.listdir(folder)
        if f.endswith(".csv")
    ]

    if not files:
        raise FileNotFoundError(
            f"No CSV files found in {folder}"
        )

    return max(
        files,
        key=os.path.getmtime
    )



def update_database():

    signal_file = latest_file(
        SIGNAL_FOLDER
    )

    result_file = latest_file(
        BACKTEST_FOLDER
    )


    print("\nSignal file:")
    print(signal_file)

    print("\nBacktest file:")
    print(result_file)


    signals = pd.read_csv(
        signal_file
    )

    results = pd.read_csv(
        result_file
    )


    merged = results.merge(

        signals[
            [
                "Symbol",
                "Sector",
                "Signal",
                "Strategy",
                "Research_Score",
                "Confidence_Score",
                "Rank_Score",
                "Momentum_Score",
                "Trend_Score",
                "Relative_Strength",
                "Risk_Reward",
                "RSI",
                "Return_5D",
                "Return_20D",
                "Distance_From_High_%",
                "Above_SMA20",
                "Above_SMA50",
                "Breakout",
                "Overextended"
            ]
        ],

        on="Symbol",

        how="left"

    )


    merged["Test_Date"] = (

        os.path.basename(result_file)

        .replace(
            "forward_test_",
            ""
        )

        .replace(
            ".csv",
            ""
        )

    )


    if os.path.exists(
        DATABASE_FILE
    ):

        old = pd.read_csv(
            DATABASE_FILE
        )


        combined = pd.concat(

            [
                old,
                merged
            ],

            ignore_index=True

        )


        combined.drop_duplicates(

            subset=[
                "Test_Date",
                "Symbol"
            ],

            inplace=True

        )


    else:

        combined = merged



    combined.to_csv(

        DATABASE_FILE,

        index=False

    )


    print("\n================================")
    print("Historical database updated")
    print("================================")


    print("\nSaved:")
    print(DATABASE_FILE)


    print("\nColumns:")
    print(
        combined.columns.tolist()
    )


    print("\nTotal records:")
    print(
        len(combined)
    )



if __name__ == "__main__":

    update_database()
