import pandas as pd



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
        # If stop and target happen on same day,
        # assume stop was hit first.

        if high >= target_1 and low <= stop_loss:

            return {

                "Target_Hit": False,

                "Stop_Hit": True,

                "Return_%": round(
                    ((stop_loss - entry) / entry) * 100,
                    2
                )

            }


        # Stop loss

        if low <= stop_loss:

            return {

                "Target_Hit": False,

                "Stop_Hit": True,

                "Return_%": round(
                    ((stop_loss - entry) / entry) * 100,
                    2
                )

            }


        # Profit target

        if high >= target_1:

            return {

                "Target_Hit": True,

                "Stop_Hit": False,

                "Return_%": round(
                    ((target_1 - entry) / entry) * 100,
                    2
                )

            }



    # Neither target nor stop reached.
    # Exit at closing price after hold period.

    final_close = future["Close"].iloc[-1]


    return {

        "Target_Hit": False,

        "Stop_Hit": False,

        "Return_%": round(
            ((final_close - entry) / entry) * 100,
            2
        )

    }





def run_backtest(
    history,
    starting_cash=10000,
    stop_percent=5,
    target_percent=8,
    hold_days=5
):


    history = history.reset_index(drop=True)


    cash = starting_cash


    trades = []


    # Start after enough data exists
    # for indicators in future versions

    i = 50



    while i < len(history) - hold_days:


        entry = history["Close"].iloc[i]


        stop_loss = (

            entry *
            (1 - stop_percent / 100)

        )


        target = (

            entry *
            (1 + target_percent / 100)

        )



        future = history.iloc[
            i:i + hold_days + 1
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

            1 +

            result["Return_%"] / 100

        )



        trades.append({

            "Entry_Date":
                history["Date"].iloc[i],


            "Entry_Price":
                round(entry,2),


            "Return_%":
                result["Return_%"],


            "Target_Hit":
                result["Target_Hit"],


            "Stop_Hit":
                result["Stop_Hit"]

        })



        # Move to next possible trade

        i += hold_days




    trades_df = pd.DataFrame(
        trades
    )



    print("\n===== BACKTEST RESULTS =====")


    print(
        "Starting Capital:",
        starting_cash
    )


    print(
        "Ending Capital:",
        round(cash,2)
    )



    total_return = (

        (cash - starting_cash)

        /

        starting_cash

    ) * 100



    print(

        "Total Return:",

        round(total_return,2),

        "%"

    )



    print(

        "Trades:",

        len(trades_df)

    )



    if len(trades_df) > 0:


        win_rate = (

            (trades_df["Return_%"] > 0)

            .mean()

            * 100

        )


        print(

            "Win Rate:",

            round(win_rate,2),

            "%"

        )


    return trades_df
