import os
import pandas as pd


RESULT_FILE = "data/results/quality_results.csv"

LIVE_DATABASE = "data/live_trade_database.csv"



def update_live_database():

    if not os.path.exists(RESULT_FILE):

        raise FileNotFoundError(
            "Scanner results not found."
        )


    df = pd.read_csv(
        RESULT_FILE
    )


    columns = [

        "Symbol",
        "Sector",
        "Signal",

        "AI_Final_Score",
        "AI_Rating",

        "ML_Probability",
        "ML_Prediction",

        "Rank_Score",

        "Entry",
        "Stop_Loss",
        "Target_1",
        "Target_2",

        "Risk_Reward",

        "RSI",

        "Return_5D",
        "Return_20D",

        "Above_SMA20",
        "Above_SMA50",

        "Breakout",
        "Overextended"

    ]


    live = df[
        [
            c for c in columns
            if c in df.columns
        ]
    ].copy()



    live["Scan_Date"] = (
        pd.Timestamp.now()
        .strftime(
            "%Y-%m-%d_%H-%M"
        )
    )



    if os.path.exists(
        LIVE_DATABASE
    ):

        old = pd.read_csv(
            LIVE_DATABASE
        )


        combined = pd.concat(
            [
                old,
                live
            ],
            ignore_index=True
        )


        combined.drop_duplicates(

            subset=[
                "Scan_Date",
                "Symbol"
            ],

            inplace=True

        )


    else:

        combined = live



    combined.to_csv(
        LIVE_DATABASE,
        index=False
    )


    print("\nLive trade database updated:")
    print(LIVE_DATABASE)

    print("\nTotal records:")
    print(len(combined))



if __name__ == "__main__":

    update_live_database()
