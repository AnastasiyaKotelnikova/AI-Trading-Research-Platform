import pandas as pd
import os


def get_latest_result():

    folder = "data/backtest_results"

    files = [
        f for f in os.listdir(folder)
        if f.endswith(".csv")
    ]

    latest = sorted(files)[-1]

    return os.path.join(folder, latest)



def analyze():

    file = get_latest_result()

    df = pd.read_csv(file)


    closed = df[
        df["Result"] != "OPEN"
    ]


    wins = closed[
        closed["Result"].str.contains("TARGET")
    ]


    losses = closed[
        closed["Result"] == "STOP HIT"
    ]


    print("\n===== PERFORMANCE METRICS =====")


    print("\nClosed Trades:")
    print(len(closed))


    print("\nWins:")
    print(len(wins))


    print("\nLosses:")
    print(len(losses))


    if len(closed):

        win_rate = (
            len(wins) / len(closed)
        ) * 100

        print("\nWin Rate:")
        print(round(win_rate,2), "%")


    print("\nAverage Winning Trade:")

    print(
        round(
            wins["Return_%"].mean(),
            2
        ),
        "%"
    )


    print("\nAverage Losing Trade:")

    print(
        round(
            losses["Return_%"].mean(),
            2
        ),
        "%"
    )


    print("\nBest Trade:")

    print(
        closed.loc[
            closed["Return_%"].idxmax()
        ]
        [["Symbol","Return_%"]]
    )


    print("\nWorst Trade:")

    print(
        closed.loc[
            closed["Return_%"].idxmin()
        ]
        [["Symbol","Return_%"]]
    )


    total_wins = wins["Return_%"].sum()

    total_losses = abs(
        losses["Return_%"].sum()
    )


    profit_factor = (
        total_wins / total_losses
    )


    print("\nProfit Factor:")

    print(
        round(
            profit_factor,
            2
        )
    )


    expected_value = (
        (len(wins)/len(closed))
        *
        wins["Return_%"].mean()
        -
        (len(losses)/len(closed))
        *
        abs(losses["Return_%"].mean())
    )


    print("\nExpected Value per Trade:")

    print(
        round(
            expected_value,
            2
        ),
        "%"
    )



if __name__ == "__main__":

    analyze()
