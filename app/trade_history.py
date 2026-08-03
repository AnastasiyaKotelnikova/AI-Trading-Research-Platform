import os
import pandas as pd
from datetime import datetime


TRADE_HISTORY_FILE = "data/trade_history.csv"

MAX_HOLD_DAYS = 30



# =====================================================
# Create trade history database
# =====================================================

def initialize_trade_history():

    os.makedirs("data", exist_ok=True)


    if os.path.exists(TRADE_HISTORY_FILE):
        return


    columns = [

        "Trade_ID",

        "Symbol",

        "Entry_Date",
        "Entry_Price",
        "Current_Price",

        "Stop_Loss",
        "Target_1",
        "Target_2",

        "Strategy",

        "AI_Decision",
        "Final_AI_Status",

        "Final_Conviction_Score",
        "Combined_ML_Probability",
        "Expected_Value",

        "Portfolio_Action",
        "Portfolio_Allocation_%",

        "Risk_Status",

        "Recommended_Shares",
        "Capital_Allocation_$",

        "Status",

        "Exit_Date",
        "Exit_Price",

        "Return_%",

        "Profit_$",

        "Days_Held",

        "Outcome",

        "Last_Updated"

    ]


    pd.DataFrame(
        columns=columns
    ).to_csv(
        TRADE_HISTORY_FILE,
        index=False
    )


    print(
        "Created trade history database."
    )




# =====================================================
# Load history
# =====================================================

def load_trade_history():

    initialize_trade_history()


    return pd.read_csv(
        TRADE_HISTORY_FILE
    )




# =====================================================
# Save history
# =====================================================

def save_trade_history(df):

    df.to_csv(
        TRADE_HISTORY_FILE,
        index=False
    )




# =====================================================
# Add newly approved AI trades
# =====================================================

def add_new_trades(ai_df):

    history = load_trade_history()


    today = datetime.today().strftime(
        "%Y-%m-%d"
    )


    new_rows = []


    for _, row in ai_df.iterrows():


        if row.get(
            "Final_AI_Status",
            ""
        ) != "APPROVED TRADE":

            continue



        symbol = row.get(
            "Symbol",
            ""
        )



        duplicate = history[

            (history["Symbol"] == symbol)

            &

            (history["Status"] == "OPEN")

        ]



        if len(duplicate) > 0:

            continue




        entry_price = row.get(
            "Entry_Price",
            row.get(
                "Close",
                0
            )
        )



        trade = {


            "Trade_ID":
                f"{symbol}_{today}",


            "Symbol":
                symbol,


            "Entry_Date":
                today,


            "Entry_Price":
                entry_price,


            "Current_Price":
                entry_price,



            "Stop_Loss":

                row.get(
                    "Stop_Loss",
                    0
                ),



            "Target_1":

                row.get(
                    "Target_1",
                    0
                ),



            "Target_2":

                row.get(
                    "Target_2",
                    0
                ),



            "Strategy":

                row.get(
                    "Strategy",
                    ""
                ),



            "AI_Decision":

                row.get(
                    "AI_Decision",
                    ""
                ),



            "Final_AI_Status":

                row.get(
                    "Final_AI_Status",
                    ""
                ),



            "Final_Conviction_Score":

                row.get(
                    "Final_Conviction_Score",
                    0
                ),



            "Combined_ML_Probability":

                row.get(
                    "Combined_ML_Probability",
                    0
                ),



            "Expected_Value":

                row.get(
                    "Expected_Value",
                    0
                ),



            "Portfolio_Action":

                row.get(
                    "Portfolio_Action",
                    ""
                ),



            "Portfolio_Allocation_%":

                row.get(
                    "Portfolio_Allocation_%",
                    0
                ),



            "Risk_Status":

                row.get(
                    "Risk_Status",
                    ""
                ),



            "Recommended_Shares":

                row.get(
                    "Recommended_Shares",
                    0
                ),



            "Capital_Allocation_$":

                row.get(
                    "Capital_Allocation_$",
                    0
                ),



            "Status":

                "OPEN",



            "Exit_Date":

                "",



            "Exit_Price":

                0,



            "Return_%":

                0,



            "Profit_$":

                0,



            "Days_Held":

                0,



            "Outcome":

                "",



            "Last_Updated":

                today

        }


        new_rows.append(
            trade
        )



    if len(new_rows) > 0:


        history = pd.concat(

            [
                history,
                pd.DataFrame(new_rows)
            ],

            ignore_index=True

        )


        save_trade_history(
            history
        )


        print(
            f"Added {len(new_rows)} new trades."
        )


    else:


        print(
            "No new approved trades."
        )




# =====================================================
# Update open trades
# =====================================================

def update_open_trades(price_df):


    history = load_trade_history()


    today = datetime.today()


    updated = 0



    for index, trade in history.iterrows():



        if trade["Status"] != "OPEN":

            continue



        symbol = trade["Symbol"]



        latest = price_df[

            price_df["Symbol"] == symbol

        ]



        if latest.empty:

            continue



        close = latest.iloc[0]["Close"]



        history.at[
            index,
            "Current_Price"
        ] = close



        entry = trade["Entry_Price"]


        stop = trade["Stop_Loss"]

        target1 = trade["Target_1"]

        target2 = trade["Target_2"]




        days = (

            today -

            datetime.strptime(

                trade["Entry_Date"],

                "%Y-%m-%d"

            )

        ).days



        history.at[
            index,
            "Days_Held"
        ] = days



        history.at[
            index,
            "Last_Updated"
        ] = today.strftime(
            "%Y-%m-%d"
        )




        outcome = None



        if close <= stop:


            outcome = "STOP LOSS"



        elif close >= target2:


            outcome = "TARGET 2 HIT"



        elif close >= target1:


            outcome = "TARGET 1 HIT"



        elif days >= MAX_HOLD_DAYS:


            outcome = "TIME EXIT"




        if outcome is None:

            continue




        history.at[
            index,
            "Status"
        ] = "CLOSED"



        history.at[
            index,
            "Outcome"
        ] = outcome




        history.at[
            index,
            "Exit_Date"
        ] = today.strftime(
            "%Y-%m-%d"
        )



        history.at[
            index,
            "Exit_Price"
        ] = close




        ret = (

            (close - entry)

            /

            entry

            *

            100

        )



        history.at[
            index,
            "Return_%"
        ] = round(
            ret,
            2
        )



        history.at[
            index,
            "Profit_$"
        ] = round(

            ret /

            100

            *

            trade["Capital_Allocation_$"],

            2

        )



        updated += 1




    save_trade_history(
        history
    )


    print(
        f"Updated {updated} trades."
    )




# =====================================================
# Summary
# =====================================================

def print_trade_summary():


    history = load_trade_history()



    print()

    print("=" * 60)

    print("TRADE HISTORY")

    print("=" * 60)



    print()

    print(
        "Total Trades:",
        len(history)
    )



    if len(history) == 0:

        return



    print()



    print(

        history[

            [

                "Symbol",

                "Status",

                "Current_Price",

                "Return_%",

                "Days_Held",

                "Outcome"

            ]

        ]

    )




# =====================================================
# Manual test
# =====================================================

if __name__ == "__main__":


    initialize_trade_history()


    print_trade_summary()