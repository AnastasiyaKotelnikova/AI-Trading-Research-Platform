import pandas as pd


INPUT_FILE = "data/backtest_results/portfolio_backtest.csv"


STARTING_CAPITAL = 7000

MAX_POSITIONS = 5

POSITION_SIZE = STARTING_CAPITAL / MAX_POSITIONS



def run_portfolio_simulation():

    df = pd.read_csv(INPUT_FILE)


    df["Entry_Date"] = pd.to_datetime(
        df["Entry_Date"]
    )


    df = df.sort_values(
        "Entry_Date"
    )


    cash = STARTING_CAPITAL

    equity = []

    trades = 0

    wins = 0

    losses = 0

    profit = 0

    loss = 0



    for _, trade in df.iterrows():


        return_pct = trade["Return_%"]


        trade_profit = (
            POSITION_SIZE *
            return_pct /
            100
        )


        cash += trade_profit


        trades += 1


        if return_pct > 0:

            wins += 1

            profit += trade_profit

        else:

            losses += 1

            loss += abs(trade_profit)


        equity.append(cash)



    results = pd.DataFrame({

        "Equity":
            equity

    })


    max_equity = (
        results["Equity"]
        .cummax()
    )


    drawdown = (
        results["Equity"]
        -
        max_equity
    ) / max_equity * 100



    print()

    print("==============================")

    print(" PORTFOLIO SIMULATION ")

    print("==============================")

    print()

    print(
        "Starting Capital:",
        STARTING_CAPITAL
    )


    print(
        "Ending Capital:",
        round(cash,2)
    )


    print(
        "Total Return:",
        round(
            (cash-STARTING_CAPITAL)
            /
            STARTING_CAPITAL
            *
            100,
            2
        ),
        "%"
    )


    print(
        "Trades:",
        trades
    )


    print(
        "Win Rate:",
        round(
            wins/trades*100,
            2
        ),
        "%"
    )


    profit_factor = (
        profit/loss
        if loss > 0
        else 0
    )


    print(
        "Profit Factor:",
        round(
            profit_factor,
            2
        )
    )


    print(
        "Maximum Drawdown:",
        round(
            drawdown.min(),
            2
        ),
        "%"
    )



    results.to_csv(
        "data/backtest_results/equity_curve.csv",
        index=False
    )


    print()

    print(
        "Saved:",
        "data/backtest_results/equity_curve.csv"
    )



if __name__ == "__main__":

    run_portfolio_simulation()
