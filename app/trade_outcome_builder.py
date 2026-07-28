import pandas as pd
import os


INPUT_FILE = (
    "data/models/model_predictions.csv"
)

OUTPUT_FILE = (
    "data/models/trading_outcomes.csv"
)


def build_outcomes():


    print()
    print("=" * 50)
    print("TRADE OUTCOME BUILDER")
    print("=" * 50)



    if not os.path.exists(INPUT_FILE):

        print("Prediction file missing")
        return



    df = pd.read_csv(INPUT_FILE)



    outcomes = []



    for _, row in df.iterrows():


        entry = row["Entry_Price"]
        stop = row["Stop_Loss"]
        target1 = row["Target_1"]
        target2 = row["Target_2"]

        price5 = row["Price_After_5D"]
        price20 = row["Price_After_20D"]



        outcome = "OPEN"



        if pd.notna(price5):


            if price5 >= target2:

                outcome = "TARGET_2_HIT"


            elif price5 >= target1:

                outcome = "TARGET_1_HIT"


            elif price5 <= stop:

                outcome = "STOP_HIT"



            else:

                outcome = "FAILED"



        outcomes.append(outcome)



    df["Trade_Outcome"] = outcomes



    df.to_csv(
        OUTPUT_FILE,
        index=False
    )



    print(
        df["Trade_Outcome"]
        .value_counts()
    )


    print()

    print("Saved:")
    print(OUTPUT_FILE)



if __name__ == "__main__":
    build_outcomes()