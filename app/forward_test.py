import os
import pandas as pd
from app.providers.yahoo import get_history


SIGNAL_FOLDER = "data/signal_history"
OUTPUT_FOLDER = "data/backtest_results"


def get_latest_signal_file():

    files = [
        f
        for f in os.listdir(SIGNAL_FOLDER)
        if f.endswith(".csv")
    ]

    latest = sorted(files)[-1]

    return os.path.join(
        SIGNAL_FOLDER,
        latest
    )


def evaluate_trade(row, hold_days=5):

    symbol = row["Symbol"]

    history = get_history(symbol)


    if history is None:
        return None


    history = history.tail(hold_days)


    if len(history) < hold_days:
        return None


    entry = row["Entry"]

    target1 = row["Target_1"]

    target2 = row["Target_2"]

    stop = row["Stop"]


    highest = history["High"].max()

    lowest = history["Low"].min()


    if highest >= target2:

        exit_price = target2
        result = "TARGET 2 HIT"


    elif highest >= target1:

        exit_price = target1
        result = "TARGET 1 HIT"


    elif lowest <= stop:

        exit_price = stop
        result = "STOP HIT"


    else:

        exit_price = history["Close"].iloc[-1]
        result = "OPEN"

    return_pct = (
        (exit_price - entry)
        / entry
        * 100
    )


    return {
        "Symbol": symbol,
        "Entry": entry,
        "Exit": round(exit_price,2),
        "Return_%": round(return_pct,2),
        "Highest": round(highest,2),
        "Lowest": round(lowest,2),
        "Target_1": target1,
        "Target_2": target2,
        "Stop": stop,
        "Result": result
    }



def run():

    signal_file = get_latest_signal_file()


    df = pd.read_csv(signal_file)


    buy_signals = df[
        df["Signal"] == "BUY"
    ]


    print("\nBUY Signals:")
    print(len(buy_signals))


    results = []


    print("\nRunning forward test...\n")


    for _, row in buy_signals.iterrows():

        result = evaluate_trade(row)

        if result:
            results.append(result)


    performance = pd.DataFrame(results)


    print(performance.head(20))


    print("\n===== RESULTS =====\n")

    print(
        performance["Result"]
        .value_counts()
    )


    print("\nAverage Return:")

    print(
        performance["Return_%"]
        .mean()
    )


    os.makedirs(
        OUTPUT_FOLDER,
        exist_ok=True
    )


    filename = (
        OUTPUT_FOLDER
        + "/forward_test_"
        + pd.Timestamp.now().strftime("%Y-%m-%d_%H-%M")
        + ".csv"
    )


    performance.to_csv(
        filename,
        index=False
    )


    print("\nSaved:")
    print(filename)



if __name__ == "__main__":

    run()
