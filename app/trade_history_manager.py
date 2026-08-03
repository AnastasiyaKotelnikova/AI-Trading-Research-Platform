import pandas as pd

from app.trade_history import (
    add_new_trades,
    print_trade_summary
)


AI_SIGNAL_FILE = "data/analysis/final_ai_signals.csv"



def update_trade_history():


    print()

    print("=" * 60)
    print("UPDATING TRADE HISTORY")
    print("=" * 60)



    df = pd.read_csv(
        AI_SIGNAL_FILE
    )


    print()

    print(
        "AI Signals Loaded:",
        len(df)
    )


    approved = df[
        df["Final_AI_Status"]
        ==
        "APPROVED TRADE"
    ]


    print(
        "Approved Trades:",
        len(approved)
    )


    if len(approved) > 0:

        print()

        print(
            approved[
                [
                    "Symbol",
                    "Final_AI_Status",
                    "Entry_Price",
                    "Expected_Value"
                ]
            ]
        )


    add_new_trades(
        df
    )


    print_trade_summary()



if __name__ == "__main__":

    update_trade_history()