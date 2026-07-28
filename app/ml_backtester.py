import pandas as pd
import joblib

from app.features import (
    build_features,
    FEATURE_COLUMNS
)

from app.backtester import (
    backtest_trade
)

MODEL_PATH = "data/models/champion_model.pkl"

MODEL = joblib.load(MODEL_PATH)

def run_ml_backtest(
    history,
    starting_cash=10000,
    probability_threshold=0.65,
    stop_percent=5,
    target_percent=8,
    hold_days=5,
    verbose=True
):

    history = history.copy()
    history = history.reset_index(drop=True)

    # Build all technical indicators
    features = build_features(history)

    # Predict ALL probabilities at once
    probabilities = MODEL.predict_proba(
        features[FEATURE_COLUMNS]
    )[:, 1]

    cash = starting_cash
    trades = []

    i = 50

    while i < len(features) - hold_days:

        probability = probabilities[i]

        if probability < probability_threshold:
            i += 1
            continue

        entry = history["Close"].iloc[i]

        stop_loss = entry * (1 - stop_percent / 100)

        target = entry * (1 + target_percent / 100)

        future = history.iloc[
            i:i + hold_days + 1
        ]

        result = backtest_trade(
            future,
            entry,
            stop_loss,
            target,
            hold_days
        )

        if result is None:
            break

        cash *= (
            1 +
            result["Return_%"] / 100
        )

        trades.append({

            "Entry_Date":
                history["Date"].iloc[i],

            "Entry_Price":
                round(entry, 2),

            "Prediction_Probability":
                round(probability, 3),

            "Return_%":
                result["Return_%"],

            "Target_Hit":
                result["Target_Hit"],

            "Stop_Hit":
                result["Stop_Hit"]

        })

        i += hold_days

    trades_df = pd.DataFrame(trades)

    total_return = (
        (cash - starting_cash)
        /
        starting_cash
    ) * 100

    if verbose:

        print("\n===== ML PROBABILITY BACKTEST =====")

        print(
            "Starting Capital:",
            starting_cash
        )

        print(
            "Ending Capital:",
            round(cash, 2)
        )

        print(
            "Total Return:",
            round(total_return, 2),
            "%"
        )

        print(
            "Trades:",
            len(trades_df)
        )

        if len(trades_df):

            win_rate = (
                (trades_df["Return_%"] > 0)
                .mean()
                * 100
            )

            print(
                "Win Rate:",
                round(win_rate, 2),
                "%"
            )

    return trades_df
