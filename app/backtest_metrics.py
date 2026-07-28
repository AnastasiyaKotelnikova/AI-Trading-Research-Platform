import pandas as pd
import numpy as np


BACKTEST_FILE = "data/backtest_results/portfolio_backtest.csv"


def calculate_max_drawdown(returns):

    equity = (1 + returns / 100).cumprod()

    peak = equity.cummax()

    drawdown = (
        (equity - peak)
        /
        peak
    ) * 100

    return drawdown.min()



def calculate_sharpe(returns):

    if returns.std() == 0:
        return 0

    sharpe = (
        returns.mean()
        /
        returns.std()
    ) * np.sqrt(len(returns))

    return sharpe



def run_metrics():

    df = pd.read_csv(
        BACKTEST_FILE
    )


    returns = df["Return_%"]


    wins = returns[
        returns > 0
    ]

    losses = returns[
        returns < 0
    ]


    total_return = returns.sum()


    win_rate = (
        (returns > 0)
        .mean()
        *
        100
    )


    avg_win = (
        wins.mean()
        if len(wins)
        else 0
    )


    avg_loss = (
        losses.mean()
        if len(losses)
        else 0
    )


    profit_factor = (
        wins.sum()
        /
        abs(losses.sum())
        if len(losses)
        else 0
    )


    max_drawdown = calculate_max_drawdown(
        returns
    )


    sharpe = calculate_sharpe(
        returns
    )


    print()
    print("==============================")
    print(" BACKTEST PERFORMANCE REPORT ")
    print("==============================")
    print()


    print(
        "Trades:",
        len(df)
    )

    print(
        "Total Return:",
        round(total_return,2),
        "%"
    )


    print(
        "Average Trade:",
        round(returns.mean(),2),
        "%"
    )


    print(
        "Win Rate:",
        round(win_rate,2),
        "%"
    )


    print(
        "Average Winner:",
        round(avg_win,2),
        "%"
    )


    print(
        "Average Loser:",
        round(avg_loss,2),
        "%"
    )


    print(
        "Profit Factor:",
        round(profit_factor,2)
    )


    print(
        "Maximum Drawdown:",
        round(max_drawdown,2),
        "%"
    )


    print(
        "Sharpe Ratio:",
        round(sharpe,2)
    )


    print()

    print(
        "Best Trade:",
        round(
            returns.max(),
            2
        ),
        "%"
    )


    print(
        "Worst Trade:",
        round(
            returns.min(),
            2
        ),
        "%"
    )


    print()


if __name__ == "__main__":

    run_metrics()
