import os
import pandas as pd

from app.providers.yahoo import get_history


PERFORMANCE_FILE = (
    "data/models/model_predictions.csv"
)



def prepare_history(history):

    if "Date" in history.columns:

        history["Date"] = pd.to_datetime(
            history["Date"]
        )

        history = history.set_index(
            "Date"
        )


    elif not isinstance(
        history.index,
        pd.DatetimeIndex
    ):

        history.index = pd.to_datetime(
            history.index
        )


    return history.sort_index()



def evaluate_trade(row):


    symbol = row["Symbol"]


    history = get_history(
        symbol
    )


    if history is None:

        return None



    history = prepare_history(
        history
    )



    prediction_date = pd.to_datetime(
        row["Date"]
    )



    future = history[
        history.index >= prediction_date
    ]



    if len(future) == 0:

        return None



    stop_loss = row["Stop_Loss"]

    target = row["Target_1"]



    for _, price in future.iterrows():


        high = price["High"]

        low = price["Low"]



        # Target reached first

        if high >= target:

            return {
                "Result": "Successful",
                "Exit_Price": target
            }



        # Stop loss reached first

        if low <= stop_loss:

            return {
                "Result": "Failed",
                "Exit_Price": stop_loss
            }




    return {
        "Result": "Open",
        "Exit_Price": future["Close"].iloc[-1]
    }





def update_performance():


    print(
        "\n========== PERFORMANCE EVALUATOR ==========\n"
    )



    if not os.path.exists(
        PERFORMANCE_FILE
    ):

        print(
            "Performance file missing"
        )

        return



    df = pd.read_csv(
        PERFORMANCE_FILE
    )



    updated = 0



    for index, row in df.iterrows():


        # Already evaluated

        if pd.notna(
            row["Prediction_Result"]
        ):

            continue



        result = evaluate_trade(
            row
        )



        if result is None:

            continue



        df.loc[
            index,
            "Prediction_Result"
        ] = result["Result"]



        df.loc[
            index,
            "Price_After_20D"
        ] = result["Exit_Price"]



        entry = row["Entry_Price"]


        df.loc[
            index,
            "Return_20D"
        ] = round(
            (
                (
                    result["Exit_Price"]
                    -
                    entry
                )
                /
                entry
            )
            *
            100,
            2
        )



        updated += 1




    df.to_csv(
        PERFORMANCE_FILE,
        index=False
    )



    print(
        "Updated trades:",
        updated
    )


    print(
        "Saved:",
        PERFORMANCE_FILE
    )




if __name__ == "__main__":

    update_performance()
