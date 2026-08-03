import pandas as pd
import os
from datetime import datetime



# =====================================================
# Single Trade Backtest
# =====================================================

def backtest_trade(
    history,
    entry,
    stop_loss,
    target_1,
    hold_days=5
):

    history = history.reset_index(drop=True)


    if len(history) < hold_days:
        return None



    future = history.iloc[:hold_days]


    for i in range(len(future)):

        high = future["High"].iloc[i]

        low = future["Low"].iloc[i]


        # Conservative assumption:
        # Stop wins if both happen same day

        if high >= target_1 and low <= stop_loss:

            return {
                "Result": "STOP HIT",
                "Return_%": round(
                    ((stop_loss-entry)/entry)*100,
                    2
                )
            }



        if low <= stop_loss:

            return {
                "Result": "STOP HIT",
                "Return_%": round(
                    ((stop_loss-entry)/entry)*100,
                    2
                )
            }



        if high >= target_1:

            return {
                "Result": "TARGET HIT",
                "Return_%": round(
                    ((target_1-entry)/entry)*100,
                    2
                )
            }



    # Still open after holding period

    final_close = future["Close"].iloc[-1]


    return {

        "Result": "OPEN",

        "Return_%": round(
            ((final_close-entry)/entry)*100,
            2
        )

    }





# =====================================================
# Full Backtest Engine
# =====================================================

def run_backtest(
    history,
    symbol="UNKNOWN",
    starting_cash=10000,
    stop_percent=5,
    target_percent=8,
    hold_days=5
):


    history = history.reset_index(drop=True)


    cash = starting_cash


    trades = []



    i = 50



    while i < len(history)-hold_days:



        entry_date = history["Date"].iloc[i]


        entry = history["Close"].iloc[i]



        stop_loss = (

            entry *
            (1-stop_percent/100)

        )


        target = (

            entry *
            (1+target_percent/100)

        )



        future = history.iloc[
            i:i+hold_days+1
        ]



        result = backtest_trade(

            future,

            entry,

            stop_loss,

            target,

            hold_days

        )



        if result is None:
            break



        cash *= (

            1+

            result["Return_%"]/100

        )



        trades.append({

            "Symbol": symbol,

            "Entry_Date": entry_date,

            "Entry_Price": round(entry,2),

            "Stop_Loss": round(stop_loss,2),

            "Target_1": round(target,2),

            "Result": result["Result"],

            "Return_%": result["Return_%"]

        })



        i += hold_days




    trades_df = pd.DataFrame(trades)



    print("\n===== BACKTEST RESULTS =====")

    print(
        "Starting Capital:",
        starting_cash
    )


    print(
        "Ending Capital:",
        round(cash,2)
    )


    if len(trades_df):

        total_return = (

            (cash-starting_cash)

            /

            starting_cash

        )*100


        print(
            "Total Return:",
            round(total_return,2),
            "%"
        )


        print(
            "Trades:",
            len(trades_df)
        )


        print("\nResults:")

        print(
            trades_df["Result"]
            .value_counts()
        )



    return trades_df





# =====================================================
# Save Results
# =====================================================

def save_backtest_results(
    trades_df,
    filename=None
):


    folder = "data/backtest_results"


    os.makedirs(
        folder,
        exist_ok=True
    )


    if filename is None:

        filename = (

            "backtest_"

            +

            datetime.now()
            .strftime("%Y%m%d_%H%M")

            +

            ".csv"

        )


    path = os.path.join(
        folder,
        filename
    )


    trades_df.to_csv(
        path,
        index=False
    )


    print(
        "\nSaved:",
        path
    )


    return path





if __name__ == "__main__":

    print(
        "Backtester module loaded."
    )