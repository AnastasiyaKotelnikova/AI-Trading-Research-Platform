"""
Trade Simulator

Simulates historical trades using:
- next day open entry
- profit target
- stop loss
- maximum holding period

Used to create realistic ML labels.
"""


import pandas as pd



# =========================
# TRADE SETTINGS
# =========================

TARGET_PERCENT = 8

STOP_PERCENT = 4

MAX_HOLD_DAYS = 10



def simulate_trade(
    df,
    entry_index
):

    """
    Simulate one historical trade.

    Entry:
        Next trading day open

    Exit:
        Target reached
        Stop reached
        Maximum holding period reached

    Returns:
        Dictionary with trade result
    """



    # Need enough future data

    if entry_index + MAX_HOLD_DAYS >= len(df):

        return None



    # Entry is next day's open

    entry_price = float(
        df["Open"].iloc[entry_index + 1]
    )


    target_price = (
        entry_price *
        (1 + TARGET_PERCENT / 100)
    )


    stop_price = (
        entry_price *
        (1 - STOP_PERCENT / 100)
    )



    for day in range(
        1,
        MAX_HOLD_DAYS + 1
    ):


        future = df.iloc[
            entry_index + day
        ]


        high = float(
            future["High"]
        )


        low = float(
            future["Low"]
        )


        close = float(
            future["Close"]
        )



        # Target hit

        if high >= target_price:

            return {

                "Trade_Result": 1,

                "Trade_Return_%":
                    TARGET_PERCENT,

                "Exit_Reason":
                    "Target Hit",

                "Holding_Days":
                    day

            }



        # Stop hit

        if low <= stop_price:

            return {

                "Trade_Result": 0,

                "Trade_Return_%":
                    -STOP_PERCENT,

                "Exit_Reason":
                    "Stop Hit",

                "Holding_Days":
                    day

            }



    # Time exit

    final_close = float(
        df["Close"]
        .iloc[
            entry_index + MAX_HOLD_DAYS
        ]
    )


    trade_return = (
        (
            final_close
            -
            entry_price
        )
        /
        entry_price
    ) * 100



    return {

        "Trade_Result":
            int(trade_return > 0),

        "Trade_Return_%":
            round(
                trade_return,
                2
            ),

        "Exit_Reason":
            "Time Exit",

        "Holding_Days":
            MAX_HOLD_DAYS

    }
