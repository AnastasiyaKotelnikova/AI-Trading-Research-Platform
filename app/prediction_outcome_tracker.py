import pandas as pd
import os
import datetime


PREDICTIONS = "data/models/model_predictions.csv"

OUTPUT = "data/models/model_predictions.csv"



def update_predictions():

    print("\n")
    print("="*60)
    print("PREDICTION OUTCOME TRACKER")
    print("="*60)


    if not os.path.exists(PREDICTIONS):

        print("Prediction file missing")
        return


    df = pd.read_csv(
        PREDICTIONS,
        low_memory=False
    )


    print("\nPredictions:")
    print(len(df))


    print("\nColumns:")
    print(df.columns.tolist())


    # Prepare outcome columns

    for col in [
        "Price_After_5D",
        "Price_After_20D",
        "Return_5D",
        "Return_20D",
        "Prediction_Result"
    ]:

        if col not in df.columns:

            df[col] = None



    df.to_csv(
        OUTPUT,
        index=False
    )


    print("\nUpdated:")
    print(OUTPUT)



if __name__ == "__main__":

    update_predictions()