import pandas as pd
import os


TRADE_HISTORY_FILE = "data/trade_history.csv"



# =====================================================
# Load Trade History
# =====================================================

def load_history():

    if not os.path.exists(
        TRADE_HISTORY_FILE
    ):

        raise FileNotFoundError(
            "Trade history not found."
        )


    return pd.read_csv(
        TRADE_HISTORY_FILE,
        keep_default_na=False
    )




# =====================================================
# Performance Analysis
# =====================================================

def analyze_performance():


    print()

    print("=" * 60)
    print("AI TRADE PERFORMANCE TRACKER")
    print("=" * 60)



    df = load_history()



    if len(df) == 0:

        print(
            "No trades available."
        )

        return




    print()

    print(
        "Total Trades:",
        len(df)
    )



    # -------------------------------------------------
    # OPEN TRADES
    # -------------------------------------------------

    open_trades = df[
        df["Status"] == "OPEN"
    ]



    print()

    print(
        "Open Trades:",
        len(open_trades)
    )



    # -------------------------------------------------
    # CLOSED TRADES
    # -------------------------------------------------

    closed = df[
        df["Status"] == "CLOSED"
    ]



    print()

    print(
        "Closed Trades:",
        len(closed)
    )



    if len(closed) == 0:

        print()

        print(
            "No closed trades yet."
        )

        return




    # -------------------------------------------------
    # WIN / LOSS
    # -------------------------------------------------

    wins = closed[
        closed["Return_%"] > 0
    ]


    losses = closed[
        closed["Return_%"] < 0
    ]



    win_rate = (

        len(wins)

        /

        len(closed)

        *

        100

    )



    print()

    print(
        "Winning Trades:",
        len(wins)
    )


    print(
        "Losing Trades:",
        len(losses)
    )


    print(
        "Win Rate:",
        round(win_rate,2),
        "%"
    )



    # -------------------------------------------------
    # RETURNS
    # -------------------------------------------------

    print()


    print(
        "Average Return:",
        round(
            closed["Return_%"].mean(),
            2
        ),
        "%"
    )



    print(
        "Best Trade:"
    )


    print(

        closed.loc[
            closed["Return_%"].idxmax()
        ]
        [
            [
                "Symbol",
                "Return_%"
            ]
        ]

    )



    print()

    print(
        "Worst Trade:"
    )


    print(

        closed.loc[
            closed["Return_%"].idxmin()
        ]
        [
            [
                "Symbol",
                "Return_%"
            ]
        ]

    )




    # -------------------------------------------------
    # AI DECISION PERFORMANCE
    # -------------------------------------------------

    if "AI_Decision" in closed.columns:


        print()

        print(
            "Performance By AI Decision:"
        )


        print(

            closed.groupby(
                "AI_Decision"
            )
            [
                "Return_%"
            ]
            .agg(
                [
                    "count",
                    "mean"
                ]
            )
            .sort_values(
                "mean",
                ascending=False
            )

        )




    # -------------------------------------------------
    # STRATEGY PERFORMANCE
    # -------------------------------------------------

    if "Strategy" in closed.columns:


        print()

        print(
            "Performance By Strategy:"
        )


        print(

            closed.groupby(
                "Strategy"
            )
            [
                "Return_%"
            ]
            .agg(
                [
                    "count",
                    "mean"
                ]
            )
            .sort_values(
                "mean",
                ascending=False
            )

        )




    print()

    print("=" * 60)

    print(
        "PERFORMANCE ANALYSIS COMPLETE"
    )

    print("=" * 60)




# =====================================================
# Run
# =====================================================

if __name__ == "__main__":

    analyze_performance()