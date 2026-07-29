import pandas as pd
import os
from datetime import datetime


MIN_FORWARD_TRADES = 50
MIN_SYMBOLS = 10


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



def calculate_forward_metrics(df):

    returns = df["Return_%"]


    trades = len(df)

    symbols = df["Symbol"].nunique()


    if trades < MIN_FORWARD_TRADES:
        return None


    if symbols < MIN_SYMBOLS:
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



    status = "PASS"


    if reliability < 50:

        status = "WARNING"


    if reliability < 35:

        status = "FAIL"



    return {

        "Evaluation_Date":
            datetime.now()
            .strftime("%Y-%m-%d %H:%M:%S"),

        "Total_Trades":
            trades,

        "Symbols":
            symbols,

        "Win_Rate":
            round(win_rate,2),

        "Average_Return":
            round(
                returns.mean(),
                2
            ),

        "Profit_Factor":
            round(
                profit_factor,
                2
            ),

        "Expectancy":
            round(
                expectancy,
                2
            ),

        "Max_Drawdown":
            round(
                drawdown,
                2
            ),

        "Reliability_Score":
            round(
                reliability,
                2
            ),

        "Status":
            status
    }



def run_forward_validation():

    print("\nLoading trade database...")


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



    df["Return_%"] = pd.to_numeric(
        df["Return_%"],
        errors="coerce"
    )


    df = df.dropna(
        subset=[
            "Return_%"
        ]
    )



    print(
        "Completed trades:",
        len(df)
    )



    metrics = calculate_forward_metrics(
        df
    )


    if metrics is None:

        print(
            "Not enough forward data"
        )

        return



    print(
        "\n===== FORWARD VALIDATION =====\n"
    )


    print(
        pd.DataFrame(
            [metrics]
        )
        .to_string(index=False)
    )



    os.makedirs(
        "data/results",
        exist_ok=True
    )


    pd.DataFrame(
        [metrics]
    ).to_csv(
        "data/results/forward_validation_report.csv",
        index=False
    )


    print(
        "\nSaved:"
        " data/results/forward_validation_report.csv"
    )



if __name__ == "__main__":

    run_forward_validation()