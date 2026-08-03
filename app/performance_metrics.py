import pandas as pd
import os



BACKTEST_FOLDER = "data/backtest_results"



def get_trade_file():

    file = os.path.join(
        BACKTEST_FOLDER,
        "realistic_completed_trades.csv"
    )


    if not os.path.exists(file):

        raise FileNotFoundError(
            "realistic_completed_trades.csv not found"
        )


    return file





def analyze():


    file = get_trade_file()


    print("\nLoading:")
    print(file)



    df = pd.read_csv(file)



    print("\n===== PERFORMANCE METRICS =====")



    total_trades = len(df)


    print(
        "\nTotal Trades:",
        total_trades
    )



    if total_trades == 0:

        print(
            "No trades available."
        )

        return




    # -------------------------------
    # WIN / LOSS
    # -------------------------------


    wins = df[
        df["Return_%"] > 0
    ]


    losses = df[
        df["Return_%"] < 0
    ]



    print(
        "\nWinning Trades:",
        len(wins)
    )


    print(
        "Losing Trades:",
        len(losses)
    )



    win_rate = (

        len(wins)

        /

        total_trades

    ) * 100



    print(
        "\nWin Rate:",
        round(win_rate,2),
        "%"
    )



    # -------------------------------
    # AVERAGES
    # -------------------------------


    if len(wins):

        print(
            "\nAverage Winning Trade:",
            round(
                wins["Return_%"].mean(),
                2
            ),
            "%"
        )


    if len(losses):

        print(
            "\nAverage Losing Trade:",
            round(
                losses["Return_%"].mean(),
                2
            ),
            "%"
        )



    # -------------------------------
    # BEST / WORST
    # -------------------------------


    best = df.loc[
        df["Return_%"].idxmax()
    ]


    worst = df.loc[
        df["Return_%"].idxmin()
    ]



    print(
        "\nBest Trade:"
    )


    print(
        best[
            [
                "Symbol",
                "Return_%"
            ]
        ]
    )



    print(
        "\nWorst Trade:"
    )


    print(
        worst[
            [
                "Symbol",
                "Return_%"
            ]
        ]
    )



    # -------------------------------
    # PROFIT FACTOR
    # -------------------------------


    gross_profit = wins[
        "Return_%"
    ].sum()



    gross_loss = abs(
        losses[
            "Return_%"
        ].sum()
    )



    if gross_loss == 0:

        profit_factor = float("inf")


    else:

        profit_factor = (
            gross_profit /
            gross_loss
        )



    print(
        "\nProfit Factor:",
        round(
            profit_factor,
            2
        )
    )



    # -------------------------------
    # EXPECTED VALUE
    # -------------------------------


    expected_value = (

        (

            len(wins)

            /

            total_trades

        )

        *

        wins["Return_%"].mean()


        -

        (

            len(losses)

            /

            total_trades

        )

        *

        abs(
            losses["Return_%"].mean()
        )

    )



    print(
        "\nExpected Value per Trade:",
        round(
            expected_value,
            2
        ),
        "%"
    )



    # -------------------------------
    # TOTAL RETURN
    # -------------------------------


    total_return = df[
        "Return_%"
    ].sum()



    print(
        "\nTotal Strategy Return:",
        round(
            total_return,
            2
        ),
        "%"
    )



    print(
        "\n===== ANALYSIS COMPLETE ====="
    )





if __name__ == "__main__":

    analyze()