import os
import pandas as pd


DATASET_FILE = "data/ml_training_dataset.csv"

MODEL_FILE = "data/models/champion_model.pkl"

METRICS_FILE = "data/models/model_metrics.csv"

TRADING_DATABASE = "data/trade_database.csv"



def run_monitor():

    print("\n")
    print("=" * 50)
    print("ML MODEL MONITOR")
    print("=" * 50)



    # ==========================
    # DATASET CHECK
    # ==========================


    if os.path.exists(DATASET_FILE):

        df = pd.read_csv(
            DATASET_FILE
        )


        print("\nTRAINING DATA")

        print(
            "Records:",
            len(df)
        )


        if "Successful_Trade" in df.columns:


            success_rate = (

                df["Successful_Trade"]
                .mean()
                *
                100

            )


            print(
                "Historical Success Rate:",
                round(success_rate,2),
                "%"
            )


    else:

        print(
            "\nTraining dataset missing"
        )



    # ==========================
    # MODEL STATUS
    # ==========================


    print("\nMODEL STATUS")


    if os.path.exists(MODEL_FILE):

        print(
            "Champion Model:"
        )

        print(
            MODEL_FILE
        )

    else:

        print(
            "Champion model missing"
        )



    # ==========================
    # MODEL HISTORY
    # ==========================


    if os.path.exists(METRICS_FILE):


        metrics = pd.read_csv(
            METRICS_FILE
        )


        print("\nMODEL HISTORY")


        print(
            metrics.tail(5)
        )


        champion = metrics[
            metrics["Status"]=="Champion"
        ]


        if len(champion):

            latest = champion.iloc[-1]


            print("\nCurrent Champion:")

            print(
                latest["Model"]
            )


            print(
                "F1:",
                round(
                    latest["F1"],
                    3
                )
            )



    # ==========================
    # TRADING PERFORMANCE
    # ==========================


    if os.path.exists(TRADING_DATABASE):


        trades = pd.read_csv(
            TRADING_DATABASE
        )


        print("\nTRADING PERFORMANCE")


        print(
            "Trades:",
            len(trades)
        )


        if "Result" in trades.columns:


            wins = (

                trades["Result"]
                .astype(str)
                .str.contains(
                    "WIN",
                    case=False
                )
                .sum()

            )


            win_rate = (

                wins
                /
                len(trades)
                *
                100

            )


            print(
                "Win Rate:",
                round(
                    win_rate,
                    2
                ),
                "%"
            )



        if "Return_%" in trades.columns:


            print(
                "Average Return:",
                round(
                    trades["Return_%"].mean(),
                    2
                ),
                "%"
            )



    # ==========================
    # RETRAINING DECISION
    # ==========================


    print("\nRETRAINING CHECK")


    if os.path.exists(DATASET_FILE):


        records = len(df)


        if records < 100:


            print(
                "NO RETRAINING"
            )


            print(
                "Reason:"
            )


            print(
                "Need more training records"
            )


        else:


            print(
                "RETRAINING AVAILABLE"
            )


    print("\n")
    print("=" * 50)



if __name__ == "__main__":

    run_monitor()
