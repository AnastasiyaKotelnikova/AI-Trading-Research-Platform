import os
import pandas as pd
import time
from multiprocessing import Pool, cpu_count

from app.ml_backtester import run_ml_backtest


PRICE_FOLDER = "data/price_history"
OUTPUT_FOLDER = "data/backtest_results"


WORKERS = 4


def process_stock(file):

    symbol = file.replace(
        "_prices.csv",
        ""
    )

    try:

        df = pd.read_csv(
            os.path.join(
                PRICE_FOLDER,
                file
            )
        )

        if len(df) < 70:
            return None


        trades = run_ml_backtest(
            df,
            verbose=False
        )


        if trades is None or len(trades) == 0:
            return None


        trades["Symbol"] = symbol

        return trades


    except Exception as e:

        print(
            symbol,
            "failed:",
            e
        )

        return None



def run_portfolio_backtest():


    start = time.time()


    files = [

        f for f in os.listdir(PRICE_FOLDER)

        if f.endswith("_prices.csv")

    ]


    print()
    print(
        "Stocks Found:",
        len(files)
    )

    print(
        "Workers:",
        WORKERS
    )


    with Pool(
        processes=WORKERS
    ) as pool:


        results = pool.map(
            process_stock,
            files
        )


    all_trades = [

        r for r in results

        if r is not None

    ]


    if len(all_trades)==0:

        print(
            "No trades found"
        )

        return None



    final = pd.concat(
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


    final.to_csv(
        output_file,
        index=False
    )


    print()
    print(
        "========== PORTFOLIO RESULTS =========="
    )

    print(
        "Stocks Tested:",
        len(files)
    )

    print(
        "Stocks With Trades:",
        final["Symbol"].nunique()
    )

    print(
        "Total Trades:",
        len(final)
    )

    print(
        "Average Return:",
        round(
            final["Return_%"].mean(),
            2
        ),
        "%"
    )


    print(
        "Median Return:",
        round(
            final["Return_%"].median(),
            2
        ),
        "%"
    )


    win_rate = (
        (final["Return_%"] > 0)
        .mean()
        *100
    )


    print(
        "Win Rate:",
        round(win_rate,2),
        "%"
    )


    print()

    print(
        "Saved:"
    )

    print(
        output_file
    )


    print()

    print(
        "Runtime:",
        round(
            time.time()-start,
            2
        ),
        "seconds"
    )


    return final



if __name__ == "__main__":

    run_portfolio_backtest()
