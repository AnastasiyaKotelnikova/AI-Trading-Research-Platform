import os
import pandas as pd
from datetime import datetime

from app.providers.yahoo import get_history


PREDICTION_FILE = "data/models/model_predictions.csv"


def update_prediction_results():

    if not os.path.exists(PREDICTION_FILE):

        print("Prediction file missing")
        return


    df = pd.read_csv(
        PREDICTION_FILE
    )

    # Force text columns
    df["Prediction_Result"] = (
        df["Prediction_Result"]
        .astype("object")
    )

    df["Price_After_5D"] = pd.to_numeric(
        df["Price_After_5D"],
        errors="coerce"
    )

    df["Return_5D"] = pd.to_numeric(
        df["Return_5D"],
        errors="coerce"
    )


    if len(df) == 0:

        print("No predictions")
        return


    updated = False


    for index, row in df.iterrows():


        # Skip already completed

        if pd.notna(
            row.get("Prediction_Result")
        ):

            continue



        symbol = row["Symbol"]


        try:

            history = get_history(
                symbol
            )


            if history is None:
                continue



            close_prices = (
                history["Close"]
                .dropna()
            )


            if len(close_prices) < 25:
                continue



            current_price = (
                close_prices.iloc[-1]
            )


            prediction_price = (
                row["Entry_Price"]
            )


            return_5d = (
                (current_price - prediction_price)
                /
                prediction_price
                *
                100
            )


            df.loc[
                index,
                "Price_After_5D"
            ] = current_price


            df.loc[
                index,
                "Return_5D"
            ] = round(
                return_5d,
                2
            )


            probability = (
                row["ML_Probability"]
            )


            if probability >= 50:

                if return_5d > 0:

                    result = "SUCCESS"

                else:

                    result = "FAILED"

            else:

                if return_5d <= 0:

                    result = "SUCCESS"

                else:

                    result = "FAILED"



            df.loc[
                index,
                "Prediction_Result"
            ] = result



            updated = True


            print(
                symbol,
                result,
                round(return_5d,2),
                "%"
            )


        except Exception as e:

            print(
                symbol,
                "ERROR",
                e
            )



    if updated:

        df.to_csv(
            PREDICTION_FILE,
            index=False
        )

        print(
            "\nPrediction database updated"
        )

    else:

        print(
            "\nNo new completed predictions"
        )



if __name__ == "__main__":

    update_prediction_results()