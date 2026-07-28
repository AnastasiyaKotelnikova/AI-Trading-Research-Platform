import os
import pandas as pd


PERFORMANCE_FILE = (
    "data/models/model_predictions.csv"
)



def analyze_trading_performance():


    print()
    print("=" * 50)
    print("TRADING PERFORMANCE ANALYZER")
    print("=" * 50)



    if not os.path.exists(
        PERFORMANCE_FILE
    ):

        print(
            "Performance file not found"
        )

        return



    df = pd.read_csv(
        PERFORMANCE_FILE
    )



    if "Return_5D" not in df.columns:

        print(
            "Return_5D column missing"
        )

        return



    completed = df[
        df["Prediction_Result"].isin(
            [
                "SUCCESS",
                "FAILED"
            ]
        )
    ].copy()



    if completed.empty:

        print(
            "No completed trades"
        )

        return



    print()

    print(
        "Total Trades:",
        len(completed)
    )



    winners = completed[
        completed["Return_5D"] > 0
    ]



    losers = completed[
        completed["Return_5D"] <= 0
    ]



    win_rate = (

        len(winners)

        /

        len(completed)

        *

        100

    )



    print(
        "Winning Trades:",
        len(winners)
    )


    print(
        "Losing Trades:",
        len(losers)
    )


    print(
        "Trade Win Rate:",
        round(win_rate,2),
        "%"
    )



    avg_win = (

        winners["Return_5D"]
        .mean()

        if len(winners) > 0

        else 0

    )



    avg_loss = (

        losers["Return_5D"]
        .mean()

        if len(losers) > 0

        else 0

    )



    print()

    print(
        "Average Winning Trade:",
        round(avg_win,2),
        "%"
    )


    print(
        "Average Losing Trade:",
        round(avg_loss,2),
        "%"
    )



    total_profit = (

        winners["Return_5D"]
        .sum()

    )


    total_loss = abs(

        losers["Return_5D"]
        .sum()

    )



    if total_loss > 0:

        profit_factor = (

            total_profit

            /

            total_loss

        )

    else:

        profit_factor = 0



    print()

    print(
        "Profit Factor:",
        round(
            profit_factor,
            2
        )
    )



    print()

    print(
        "Best 5 Trades"
    )

    print(
        completed
        .sort_values(
            "Return_5D",
            ascending=False
        )
        [
            [
                "Symbol",
                "Return_5D",
                "AI_Final_Score",
                "ML_Probability"
            ]
        ]
        .head(5)
    )



    print()

    print(
        "Worst 5 Trades"
    )

    print(
        completed
        .sort_values(
            "Return_5D"
        )
        [
            [
                "Symbol",
                "Return_5D",
                "AI_Final_Score",
                "ML_Probability"
            ]
        ]
        .head(5)
    )



    print()

    print("=" * 50)




if __name__ == "__main__":

    analyze_trading_performance()