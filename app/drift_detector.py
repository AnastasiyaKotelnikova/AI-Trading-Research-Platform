import os
import pandas as pd


TRAINING_FILE = "data/ml_training_dataset.csv"

SIGNAL_FOLDER = "data/signal_history"



FEATURES = [

    "Rank_Score",

    "Momentum_Score",

    "Trend_Score",

    "Relative_Strength",

    "Risk_Reward",

    "RSI",

    "Return_5D",

    "Return_20D",

    "Distance_From_High_%",

    "Confidence_Score",

    "Research_Score"

]



def latest_signal_file():

    files = [

        os.path.join(
            SIGNAL_FOLDER,
            f
        )

        for f in os.listdir(SIGNAL_FOLDER)

        if f.endswith(".csv")

    ]


    return max(
        files,
        key=os.path.getmtime
    )



def run_drift_check():


    print("\n")
    print("=" * 50)
    print("DATA DRIFT DETECTOR")
    print("=" * 50)



    if not os.path.exists(TRAINING_FILE):

        print("Training dataset missing")
        return



    current_file = latest_signal_file()



    train = pd.read_csv(
        TRAINING_FILE
    )


    current = pd.read_csv(
        current_file
    )



    print("\nTraining Dataset:")
    print(len(train))


    print("\nCurrent Signals:")
    print(len(current))



    print("\nFEATURE COMPARISON\n")



    drift_count = 0



    for feature in FEATURES:


        if feature not in train.columns:
            continue


        if feature not in current.columns:
            continue



        train_mean = train[feature].mean()

        current_mean = current[feature].mean()



        difference = abs(

            current_mean
            -
            train_mean

        )



        percent_change = (

            difference
            /
            abs(train_mean)

            *
            100

        )



        status = "NORMAL"



        if percent_change > 25:

            status = "DRIFT DETECTED"

            drift_count += 1



        print(

            feature,

            "\n Training:",
            round(train_mean,2),

            "\n Current:",
            round(current_mean,2),

            "\n Change:",
            round(percent_change,2),
            "%",

            "\n Status:",
            status,

            "\n"

        )



    print("=" * 50)



    if drift_count == 0:


        print(
            "MARKET DATA STATUS: STABLE"
        )


    else:


        print(
            "MARKET DATA STATUS: WARNING"
        )


        print(
            "Features with drift:",
            drift_count
        )



    print("=" * 50)



if __name__ == "__main__":

    run_drift_check()
