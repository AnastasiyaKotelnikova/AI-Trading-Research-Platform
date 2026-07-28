import os
import pandas as pd


# Existing historical ML dataset
DATASET_FILE = "data/historical_ml_dataset.csv"

# Trade results produced by the realistic simulator
TRADES_FILE = (
    "data/backtest_results/"
    "portfolio_backtest_with_dates.csv"
)

# Updated dataset
OUTPUT_FILE = (
    "data/historical_ml_dataset_updated.csv"
)


def main():

    if not os.path.exists(DATASET_FILE):

        print("Historical dataset not found.")
        return

    if not os.path.exists(TRADES_FILE):

        print("Trade history not found.")
        return

    dataset = pd.read_csv(DATASET_FILE)

    trades = pd.read_csv(TRADES_FILE)

    print("\n========== UPDATE TRAINING LABELS ==========\n")

    print("Historical rows:", len(dataset))
    print("Trades found:", len(trades))

    #
    # Create binary target
    #
    trades["Target"] = (
        trades["Return_%"] > 0
    ).astype(int)

    #
    # Keep useful columns only
    #
    trades = trades[[
        "Symbol",
        "Entry_Date",
        "Target"
    ]]

    #
    # Match historical dataset
    #
    trades = trades.rename(
        columns={
            "Entry_Date": "Date"
        }
    )

    #
    # Merge Target back into historical dataset
    #
    updated = dataset.merge(

        trades,

        on=[
            "Symbol",
            "Date"
        ],

        how="left",

        suffixes=(
            "",
            "_NEW"
        )

    )

    #
    # Replace target if we have newer information
    #
    if "Target_NEW" in updated.columns:

        updated["Target"] = updated[
            "Target_NEW"
        ].fillna(
            updated["Target"]
        )

        updated.drop(
            columns=["Target_NEW"],
            inplace=True
        )

    #
    # Save
    #
    updated.to_csv(

        OUTPUT_FILE,

        index=False

    )

    print()

    print("Updated dataset rows:", len(updated))

    print("Saved:")

    print(OUTPUT_FILE)


if __name__ == "__main__":

    main()
