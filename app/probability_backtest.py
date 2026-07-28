import pandas as pd


DATA_FILE = "data/historical_ml_dataset.csv"
PRED_FILE = "data/models/test_predictions.csv"


def run_backtest():

    print("\n===== PROBABILITY THRESHOLD BACKTEST =====\n")


    df = pd.read_csv(DATA_FILE)

    df["Date"] = pd.to_datetime(df["Date"])


    # Same test period used in training
    test_df = df[
        df["Date"] >= "2026-05-15"
    ].copy()


    predictions = pd.read_csv(
        PRED_FILE
    )


    test_df = test_df.reset_index(drop=True)

    test_df["Probability"] = (
        predictions["Success_Probability"]
    )


    thresholds = [
        0.50,
        0.60,
        0.70,
        0.75,
        0.80,
        0.85
    ]


    results = []


    for threshold in thresholds:


        trades = test_df[
            test_df["Probability"] >= threshold
        ]


        if len(trades) == 0:

            continue


        win_rate = (
            trades["Future_Return_5D"] > 0
        ).mean()


        avg_return = (
            trades["Future_Return_5D"]
            .mean()
        )


        avg_winner = (
            trades[
                trades["Future_Return_5D"] > 0
            ]["Future_Return_5D"]
            .mean()
        )


        avg_loser = (
            trades[
                trades["Future_Return_5D"] <= 0
            ]["Future_Return_5D"]
            .mean()
        )


        results.append({

            "Threshold": threshold,

            "Trades": len(trades),

            "Win_Rate": round(win_rate,3),

            "Average_Return": round(avg_return,3),

            "Average_Winner": round(avg_winner,3),

            "Average_Loser": round(avg_loser,3)

        })


    results = pd.DataFrame(results)


    print(
        results.to_string(index=False)
    )


    results.to_csv(
        "data/models/probability_backtest.csv",
        index=False
    )


    print(
        "\nSaved:"
    )

    print(
        "data/models/probability_backtest.csv"
    )



if __name__ == "__main__":

    run_backtest()