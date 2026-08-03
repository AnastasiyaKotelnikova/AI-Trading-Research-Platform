import pandas as pd
from app.trade_history import (
    load_trade_history,
    update_open_trades
)


PRICE_FILE = "data/analysis/final_ai_signals.csv"



# =====================================================
# Load latest prices
# =====================================================

def load_prices():

    df = pd.read_csv(
        PRICE_FILE
    )


    required = [
        "Symbol",
        "Close"
    ]


    for col in required:

        if col not in df.columns:

            raise Exception(
                f"Missing column: {col}"
            )


    return df[
        [
            "Symbol",
            "Close"
        ]
    ]



# =====================================================
# Show current positions
# =====================================================

def show_open_positions(history):


    open_trades = history[
        history["Status"] == "OPEN"
    ].copy()



    if len(open_trades) == 0:

        print(
            "No open trades."
        )

        return False



    print()

    print(
        "Current Open Trades:"
    )


    print(

        open_trades[

            [

                "Symbol",
                "Entry_Price",
                "Stop_Loss",
                "Target_1",
                "Days_Held"

            ]

        ]

    )


    return True



# =====================================================
# Monitor
# =====================================================

def monitor_trades():


    print()

    print("=" * 60)
    print("LIVE TRADE MONITOR")
    print("=" * 60)



    history = load_trade_history()



    if len(history) == 0:

        print(
            "No trades in database."
        )

        return



    has_open = show_open_positions(
        history
    )


    if not has_open:

        return



    print()

    print(
        "Updating prices..."
    )



    prices = load_prices()



    update_open_trades(
        prices
    )



    print()

    print(
        "Checking completed trades..."
    )



    updated_history = load_trade_history()



    closed = updated_history[
        updated_history["Status"] != "OPEN"
    ]



    print(
        "Completed Trades:",
        len(closed)
    )



    print()

    print(
        "Monitoring complete."
    )



# =====================================================
# Run
# =====================================================

if __name__ == "__main__":

    monitor_trades()