import os
import pandas as pd

from app.ml_backtester import run_ml_backtest


PRICE_FOLDER = "data/price_history"
OUTPUT_FOLDER = "data/backtest_results"


def run_portfolio_backtest():

    all_trades = []

    files = [

        f

        for f in os.listdir(PRICE_FOLDER)

        if f.endswith("_prices.csv")

    ]

    print()
    print("Stocks Found:", len(files))
    print()

    for file in files:

        symbol = file.replace(
            "_prices.csv",
            ""
        )

        print(symbol)

        try:

            df = pd.read_csv(

                os.path.join(
                    PRICE_FOLDER,
                    file
                )

            )

        except Exception:

            print("Could not read", symbol)

            continue


        # Skip stocks with little history
        if len(df) < 70:

            continue


        try:

           trades = run_ml_backtest(
               df,
               verbose=False
            )

        except Exception as e:

            print(symbol, "failed:", e)

            continue


        if trades is None:

            continue


        if len(trades) == 0:

            continue


        trades["Symbol"] = symbol

        all_trades.append(trades)


    if len(all_trades) == 0:

        print()
        print("No trades found.")
        return None


    results = pd.concat(

        all_trades,

        ignore_index=True

    )


    os.makedirs(

        OUTPUT_FOLDER,

        exist_ok=True

    )


    output_file = os.path.join(

        OUTPUT_FOLDER,

        "portfolio_backtest.csv"

    )


    results.to_csv(

        output_file,

        index=False

    )


    print()
    print("========== PORTFOLIO RESULTS ==========")
    print()

    print(
        "Stocks Tested:",
        len(files)
    )

    print(
        "Stocks With Trades:",
        results["Symbol"].nunique()
    )

    print(
        "Total Trades:",
        len(results)
    )

    print(
        "Average Return:",
        round(
            results["Return_%"].mean(),
            2
        ),
        "%"
    )

    print(
        "Median Return:",
        round(
            results["Return_%"].median(),
            2
        ),
        "%"
    )

    print(
        "Best Trade:",
        round(
            results["Return_%"].max(),
            2
        ),
        "%"
    )

    print(
        "Worst Trade:",
        round(
            results["Return_%"].min(),
            2
        ),
        "%"
    )

    win_rate = (

        (results["Return_%"] > 0)

        .mean()

        * 100

    )

    print(
        "Win Rate:",
        round(win_rate, 2),
        "%"
    )

    print()

    print("Saved:")
    print(output_file)

    return results


if __name__ == "__main__":

    run_portfolio_backtest()
