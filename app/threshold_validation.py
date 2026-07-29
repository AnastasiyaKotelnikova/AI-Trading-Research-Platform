import pandas as pd
import json
import os
from datetime import datetime


MIN_VALIDATION_TRADES = 50
MIN_VALIDATION_SYMBOLS = 10



def load_thresholds():

    with open(
        "data/models/optimal_thresholds.json",
        "r"
    ) as f:

        return json.load(f)



def calculate_drawdown(returns):

    equity = (
        1 + returns / 100
    ).cumprod()

    peak = equity.cummax()

    drawdown = (
        (equity - peak)
        /
        peak
    ) * 100

    return abs(drawdown.min())



def calculate_validation_metrics(df):


    returns = df["Return_%"]


    trades = len(df)

    symbols = df["Symbol"].nunique()


    if trades < MIN_VALIDATION_TRADES:
        return None


    if symbols < MIN_VALIDATION_SYMBOLS:
        return None



    wins = returns[
        returns > 0
    ]

    losses = returns[
        returns < 0
    ]



    if len(losses) == 0:
        return None



    win_rate = (
        len(wins)
        /
        trades
    ) * 100



    avg_return = returns.mean()


    profit_factor = (

        wins.sum()
        /
        abs(losses.sum())

    )



    expectancy = (

        (win_rate / 100)
        *
        wins.mean()

        -

        ((1-win_rate/100)
        *
        abs(losses.mean()))

    )



    drawdown = calculate_drawdown(
        returns
    )



    reliability = (

        min(trades / 200, 1) * 40

        +

        min(symbols / 50, 1) * 30

        +

        min(profit_factor / 5, 1) * 30

    )



    return {

        "Validation_Trades":
            trades,

        "Validation_Symbols":
            symbols,

        "Win_Rate":
            round(win_rate,2),

        "Average_Return":
            round(avg_return,2),

        "Profit_Factor":
            round(profit_factor,2),

        "Expectancy":
            round(expectancy,2),

        "Max_Drawdown":
            round(drawdown,2),

        "Reliability_Score":
            round(reliability,2)

    }



def validate_thresholds():


    print("\nLoading thresholds...")


    thresholds = load_thresholds()



    print(
        thresholds
    )



    print(
        "\nLoading trades..."
    )


    df = pd.read_csv(
        "data/trade_database.csv",
        low_memory=False
    )



    df = df[
        df["Result"].isin(
            [
                "TARGET 1 HIT",
                "STOP HIT"
            ]
        )
    ].copy()



    df["Scan_Date"] = pd.to_datetime(
        df["Scan_Date"]
    )



    cutoff = df["Scan_Date"].quantile(
        0.70
    )



    validation = df[
        df["Scan_Date"] > cutoff
    ].copy()



    print(
        "Validation period:",
        validation["Scan_Date"].min(),
        "to",
        validation["Scan_Date"].max()
    )



    validation = validation[

        (validation["Rank_Score"]
         >= thresholds["Rank_Score"])

        &

        (validation["Confidence_Score"]
         >= thresholds["Confidence_Score"])

        &

        (validation["Research_Score"]
         >= thresholds["Research_Score"])

        &

        (validation["Risk_Reward"]
         >= thresholds["Risk_Reward"])

    ]



    metrics = calculate_validation_metrics(
        validation
    )



    if metrics is None:

        print(
            "\nValidation failed:"
            " insufficient data"
        )

        return



    metrics["Validation_Date"] = (
        datetime.now()
        .strftime("%Y-%m-%d %H:%M:%S")
    )



    os.makedirs(
        "data/results",
        exist_ok=True
    )


    pd.DataFrame(
        [metrics]
    ).to_csv(
        "data/results/threshold_validation_report.csv",
        index=False
    )



    print(
        "\n===== VALIDATION RESULTS =====\n"
    )


    print(
        pd.DataFrame(
            [metrics]
        ).to_string(index=False)
    )


    print(
        "\nSaved:"
        " data/results/threshold_validation_report.csv"
    )



if __name__ == "__main__":

    validate_thresholds()