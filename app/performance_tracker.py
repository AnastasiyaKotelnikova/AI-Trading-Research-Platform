import os
import pandas as pd
from app.providers.yahoo import get_history


PERFORMANCE_FOLDER = "data/performance_history"

HISTORY_FOLDER = "data/signal_history"



def get_latest_signal_file():

    files = [
        os.path.join(HISTORY_FOLDER, f)
        for f in os.listdir(HISTORY_FOLDER)
        if f.endswith("_signals.csv")
    ]


    if not files:
        raise FileNotFoundError(
            "No signal history files found."
        )


    latest = max(
        files,
        key=os.path.getmtime
    )


    return latest




def run():

    filename = get_latest_signal_file()

    df = pd.read_csv(filename)


    print("\nLatest Signal File:\n")

    print(filename)


    print("\nSignals:")

    print(df.shape[0])


    print("\nBUY Signals:")

    print(
        len(
            df[df["Signal"] == "BUY"]
        )
    )


    buy_signals = df[
        df["Signal"] == "BUY"
    ]


    print("\n===== PERFORMANCE CHECK =====\n")


    results = []


    for _, row in buy_signals.iterrows():

        symbol = row["Symbol"]


        history = get_history(symbol)


        if history is None:
            continue


        current_price = history["Close"].iloc[-1]


        entry = row["Entry"]


        return_pct = (
            (current_price - entry)
            / entry
            * 100
        )


        target1 = row["Target_1"]

        target2 = row["Target_2"]

        stop = row.get(
            "Stop_Loss",
            row.get("Stop")
        )


        if current_price >= target2:

            status = "TARGET 2 HIT"


        elif current_price >= target1:

            status = "TARGET 1 HIT"


        elif current_price <= stop:

            status = "STOP HIT"


        elif current_price > entry:

            status = "WINNING"


        else:

            status = "LOSING"



        results.append(
            {

                "Symbol": symbol,

                "Strategy": row.get(
                    "Strategy",
                    "UNKNOWN"
                ),


                "Confidence_Score": row.get(
                    "Confidence_Score",
                    None
                ),


                "Research_Score": row.get(
                    "Research_Score",
                    None
                ),


                "Rank_Score": row.get(
                    "Rank_Score",
                    None
                ),


                "Sector": row.get(
                    "Sector",
                    None
                ),


                "Entry": entry,


                "Current": round(
                    current_price,
                    2
                ),


                "Return_%": round(
                    return_pct,
                    2
                ),


                "Status": status,


                "Target_1": target1,


                "Target_2": target2,


                "Stop_Loss": stop

            }
        )



    performance = pd.DataFrame(results)



    print(
        performance.head(20)
    )


    print("\n===== STATUS SUMMARY =====\n")


    print(
        performance["Status"]
        .value_counts()
    )



    os.makedirs(
        PERFORMANCE_FOLDER,
        exist_ok=True
    )


    output_file = (
        PERFORMANCE_FOLDER
        + "/"
        + pd.Timestamp.now().strftime("%Y-%m-%d_%H-%M")
        + "_performance.csv"
    )



    performance.to_csv(
        output_file,
        index=False
    )


    print("\nPerformance saved:")

    print(output_file)



    print("\nAverage Return:")


    print(
        round(
            performance["Return_%"].mean(),
            2
        ),
        "%"
    )




if __name__ == "__main__":

    run()
