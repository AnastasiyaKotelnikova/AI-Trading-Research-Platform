import pandas as pd


INPUT_FILE = (
    "data/backtest_results/"
    "portfolio_backtest_with_dates.csv"
)


STARTING_CAPITAL = 7000

MAX_POSITIONS = 5

POSITION_PERCENT = 0.20



def run_simulation():

    df = pd.read_csv(
        INPUT_FILE
    )


    df["Entry_Date"] = pd.to_datetime(
        df["Entry_Date"]
    )

    df["Exit_Date"] = pd.to_datetime(
        df["Exit_Date"]
    )


    df = df.sort_values(
        "Entry_Date"
    )


    cash = STARTING_CAPITAL

    open_positions = []

    completed_trades = []

    equity_curve = []


    all_dates = pd.date_range(

        df["Entry_Date"].min(),

        df["Exit_Date"].max()

    )


    for current_date in all_dates:


        # Close finished trades

        still_open = []


        for position in open_positions:


            if position["Exit_Date"] <= current_date:


                profit = (
                    position["Position_Size"]
                    *
                    position["Return_%"]
                    /
                    100
                )


                cash += (
                    position["Position_Size"]
                    +
                    profit
                )


                completed_trades.append(
                    position
                )


            else:

                still_open.append(
                    position
                )


        open_positions = still_open



        # Find new entries

        todays_trades = df[

            df["Entry_Date"] == current_date

        ]


        for _, trade in todays_trades.iterrows():


            if len(open_positions) >= MAX_POSITIONS:

                break



            symbol = trade["Symbol"]


            already_open = any(

                x["Symbol"] == symbol

                for x in open_positions

            )


            if already_open:

                continue



            position_size = (
                cash *
                POSITION_PERCENT
            )


            if position_size <= 0:

                continue



            cash -= position_size


            open_positions.append({

                "Symbol":
                    symbol,

                "Entry_Date":
                    trade["Entry_Date"],

                "Exit_Date":
                    trade["Exit_Date"],

                "Return_%":
                    trade["Return_%"],

                "Position_Size":
                    position_size

            })



        invested = sum(

            x["Position_Size"]

            for x in open_positions

        )


        equity_curve.append({

            "Date":
                current_date,

            "Equity":
                cash + invested

        })



    equity = pd.DataFrame(
        equity_curve
    )


    trades = pd.DataFrame(
        completed_trades
    )


    print()

    print("==============================")

    print(" REALISTIC PORTFOLIO RESULTS ")

    print("==============================")

    print()


    ending_value = equity["Equity"].iloc[-1]


    print(
        "Starting Capital:",
        STARTING_CAPITAL
    )


    print(
        "Ending Capital:",
        round(
            ending_value,
            2
        )
    )


    print(
        "Total Return:",
        round(
            (ending_value - STARTING_CAPITAL)
            /
            STARTING_CAPITAL
            *
            100,
            2
        ),
        "%"
    )


    print(
        "Completed Trades:",
        len(trades)
    )


    if len(trades):

        print(

            "Win Rate:",

            round(

                (trades["Return_%"] > 0)
                .mean()
                *
                100,

                2

            ),

            "%"

        )



    peak = equity["Equity"].cummax()


    drawdown = (

        equity["Equity"]

        -

        peak

    ) / peak * 100


    print(

        "Maximum Drawdown:",

        round(

            drawdown.min(),

            2

        ),

        "%"

    )


    equity.to_csv(

        "data/backtest_results/"
        "realistic_equity_curve.csv",

        index=False

    )


    trades.to_csv(

        "data/backtest_results/"
        "realistic_completed_trades.csv",

        index=False

    )


    print()

    print(
        "Saved realistic results."
    )



if __name__ == "__main__":

    run_simulation()
