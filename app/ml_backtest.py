import pandas as pd


DATA_FILE = "data/historical_ml_dataset.csv"
PREDICTIONS_FILE = "data/models/test_predictions.csv"


def run_ml_backtest(
    probability_threshold=0.70
):

    print("\n===== ML BACKTEST =====\n")


    df = pd.read_csv(DATA_FILE)

    df["Date"] = pd.to_datetime(
        df["Date"]
    )


    # Same test period used in training
    test_df = df[
        df["Date"] >= "2026-05-15"
    ].copy()


    predictions = pd.read_csv(
        PREDICTIONS_FILE
    )


    test_df = test_df.reset_index(
        drop=True
    )


    test_df["Probability"] = (
        predictions["Success_Probability"]
    )


    trades = test_df[
        test_df["Probability"] >= probability_threshold
    ]


    if len(trades) == 0:

        print(
            "No trades found"
        )

        return


    win_rate = (
        trades["Future_Return_5D"] > 0
    ).mean()


    target_hit_rate = (
        trades["Future_Return_5D"] > 3
    ).mean()


    stop_hit_rate = (
        trades["Future_Max_Drawdown_5D"] < -5
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


    print(
        "Trades:",
        len(trades)
    )

    print(
        "Win Rate:",
        round(win_rate,3)
    )

    print(
        "Target Hit Rate:",
        round(target_hit_rate,3)
    )

    print(
        "Stop Hit Rate:",
        round(stop_hit_rate,3)
    )

    print(
        "Average Return:",
        round(avg_return,3)
    )

    print(
        "Average Winner:",
        round(avg_winner,3)
    )

    print(
        "Average Loser:",
        round(avg_loser,3)
    )


    return {

        "Trades": len(trades),

        "Win_Rate": win_rate,

        "Target_Hit_Rate": target_hit_rate,

        "Stop_Hit_Rate": stop_hit_rate,

        "Average_Return": avg_return

    }



if __name__ == "__main__":

    run_ml_backtest()