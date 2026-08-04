import os
import pandas as pd

from app.providers.yahoo import get_history


PREDICTION_FILE = "data/models/model_predictions.csv"


def update_prediction_results():

    if not os.path.exists(PREDICTION_FILE):

        print("Prediction file missing")
        return


    df = pd.read_csv(
        PREDICTION_FILE,
        low_memory=False
    )


    # =====================================
    # Ensure required columns
    # =====================================

    if "Prediction_Result" not in df.columns:

        df["Prediction_Result"] = None


    df["Prediction_Result"] = (
        df["Prediction_Result"]
        .astype("object")
    )


    if "Price_After_5D" not in df.columns:

        df["Price_After_5D"] = None


    if "Return_5D" not in df.columns:

        df["Return_5D"] = None


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


        # =====================================
        # Skip completed predictions
        # =====================================

        if row["Prediction_Result"] in [
            "SUCCESS",
            "FAILED",
            "NEUTRAL"
        ]:
            continue



        symbol = row["Symbol"]


        try:


            history = get_history(
                symbol
            )


            if history is None:

                continue



            # =====================================
            # Normalize history dates
            # =====================================

            history = history.copy()


            if not isinstance(
                history.index,
                pd.DatetimeIndex
            ):


                if "Date" in history.columns:


                    history["Date"] = pd.to_datetime(
                        history["Date"]
                    )


                    history = history.set_index(
                        "Date"
                    )


                else:


                    history.index = pd.to_datetime(
                        history.index
                    )



            history = history.sort_index()



            if "Close" not in history.columns:

                print(
                    symbol,
                    "Missing Close column"
                )

                continue



            close_prices = (
                history["Close"]
                .dropna()
            )



            if len(close_prices) < 25:

                continue



            # =====================================
            # Find actual 5 trading day future price
            # =====================================

            prediction_date = pd.to_datetime(
                row["Date"]
            )



            future_prices = history.loc[
                history.index > prediction_date,
                "Close"
            ]



            if len(future_prices) < 5:

                continue



            price_after_5d = (
                future_prices.iloc[4]
            )



            entry_price = float(
                row["Entry_Price"]
            )



            if entry_price <= 0:

                continue



            return_5d = (

                (
                    price_after_5d
                    -
                    entry_price
                )

                /

                entry_price

                *

                100

            )



            # =====================================
            # Save actual outcome data
            # =====================================

            df.loc[
                index,
                "Price_After_5D"
            ] = round(
                price_after_5d,
                2
            )


            df.loc[
                index,
                "Return_5D"
            ] = round(
                return_5d,
                2
            )



            # =====================================
            # Long-only classification
            # =====================================

            if return_5d >= 1.0:

                result = "SUCCESS"


            elif return_5d <= -1.0:

                result = "FAILED"


            else:

                result = "NEUTRAL"



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



    # =====================================
    # Save database
    # =====================================

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
            "\nNo predictions updated"
        )



if __name__ == "__main__":

    update_prediction_results()
    