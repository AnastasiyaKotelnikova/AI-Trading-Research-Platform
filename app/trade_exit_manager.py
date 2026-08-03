import pandas as pd
from datetime import datetime
import os


TRADE_HISTORY_FILE = "data/trade_history.csv"



# =====================================================
# Load Trades
# =====================================================

def load_trades():

    if not os.path.exists(
        TRADE_HISTORY_FILE
    ):

        raise FileNotFoundError(
            "Trade history file not found."
        )


    return pd.read_csv(
        TRADE_HISTORY_FILE,
        keep_default_na=False
    )




# =====================================================
# Update Exits
# =====================================================

def update_trade_exits(price_df):


    trades = load_trades()


    updated = 0


    today = datetime.today().strftime(
        "%Y-%m-%d"
    )



    for index, trade in trades.iterrows():


        if trade["Status"] != "OPEN":

            continue



        symbol = trade["Symbol"]



        current = price_df[
            price_df["Symbol"] == symbol
        ]



        if current.empty:

            continue



        price = float(
            current.iloc[0]["Close"]
        )


        entry = float(
            trade["Entry_Price"]
        )


        stop = float(
            trade["Stop_Loss"]
        )


        target1 = float(
            trade["Target_1"]
        )


        target2 = float(
            trade["Target_2"]
        )



        result = None



        # -----------------------------
        # Stop Loss
        # -----------------------------

        if price <= stop:

            result = "STOP HIT"



        # -----------------------------
        # Target 2
        # -----------------------------

        elif price >= target2:

            result = "TARGET 2 HIT"



        # -----------------------------
        # Target 1
        # -----------------------------

        elif price >= target1:

            result = "TARGET 1 HIT"



        if result:


            return_percent = (

                (price - entry)

                /

                entry

                *

                100

            )


            trades.at[
                index,
                "Status"
            ] = result



            trades.at[
                index,
                "Exit_Date"
            ] = today



            trades.at[
                index,
                "Exit_Price"
            ] = price



            trades.at[
                index,
                "Return_%"
            ] = round(
                return_percent,
                2
            )



            trades.at[
                index,
                "Outcome"
            ] = (

                "WIN"

                if return_percent > 0

                else

                "LOSS"

            )



            trades.at[
                index,
                "Last_Updated"
            ] = today



            updated += 1




    trades.to_csv(
        TRADE_HISTORY_FILE,
        index=False
    )



    print()

    print("=" * 60)
    print("TRADE EXIT MANAGER")
    print("=" * 60)


    print()

    print(
        "Closed Trades:",
        updated
    )



    return trades




# =====================================================
# Test
# =====================================================

if __name__ == "__main__":


    print(
        "Trade Exit Manager Loaded."
    )