import os
import pandas as pd
from datetime import datetime


SIGNAL_HISTORY = "data/signal_history"
DATABASE_FILE = "data/trade_database.csv"



def build_trade_database():

    print("\n================================")
    print("TRADE DATABASE BUILDER")
    print("================================\n")


    if not os.path.exists(SIGNAL_HISTORY):

        print("No signal history found")
        return


    files = sorted(
        os.listdir(SIGNAL_HISTORY)
    )


    records = []


    for file in files:

        if not file.endswith(".csv"):
            continue


        path = os.path.join(
            SIGNAL_HISTORY,
            file
        )


        df = pd.read_csv(path)


        scan_id = file.replace(
            "_signals.csv",
            ""
        )

        df["Scan_Date"] = scan_id[:10]

        df["Scan_ID"] = scan_id
        

        # Ensure model tracking columns exist
        for column in [
            "Model_Name",
            "Model_Accuracy",
            "Model_F1",
            "Model_Date"
        ]:

            if column not in df.columns:
                df[column] = None


        records.append(df)



    if not records:

        print("No records")
        return



    database = pd.concat(
        records,
        ignore_index=True
    )

    database = database.drop_duplicates(
        subset=[
            "Symbol",
            "Scan_ID",
            "Model_Name"
        ],
        keep="last"
    )



    database.to_csv(
        DATABASE_FILE,
        index=False
    )



    print(
        "Trades stored:",
        len(database)
    )


    print(
        "Saved:",
        DATABASE_FILE
    )




if __name__ == "__main__":

    build_trade_database()
