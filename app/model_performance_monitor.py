import pandas as pd
import os
import datetime


TRADE_DATABASE = "data/trade_database.csv"

METRICS_FILE = "data/models/model_trade_performance.csv"

MODEL_INFO_FILE = "data/models/model_metrics.csv"



def load_trade_data():

    if not os.path.exists(TRADE_DATABASE):

        raise FileNotFoundError(
            "Trading database not found"
        )


    df = pd.read_csv(
        TRADE_DATABASE,
        low_memory=False
    )


    return df



def load_model_info():

    if not os.path.exists(MODEL_INFO_FILE):

        return {
            "Model": "Unknown",
            "F1": None,
            "Status": "Unknown"
        }


    df = pd.read_csv(
        MODEL_INFO_FILE
    )


    champions = df[
        df["Status"] == "Champion"
    ]


    if len(champions) == 0:

        return {
            "Model": "Unknown",
            "F1": None,
            "Status": "Unknown"
        }


    latest = champions.iloc[-1]


    return {

        "Model": latest["Model"],
        "F1": latest["F1"],
        "Status": latest["Status"]

    }



def calculate_performance(df):


    total = len(df)


    if total == 0:

        return None



    results = df["Result"].value_counts()



    wins = (

        results.get(
            "TARGET 1 HIT",
            0
        )

        +

        results.get(
            "TARGET 2 HIT",
            0
        )

    )


    stops = results.get(
        "STOP HIT",
        0
    )


    open_positions = results.get(
        "OPEN",
        0
    )



    completed = wins + stops



    if completed > 0:

        win_rate = (
            wins /
            completed
        ) * 100

    else:

        win_rate = 0



    avg_return = df[
        "Return_%"
    ].mean()



    avg_rr = df[
        "Risk_Reward"
    ].mean()



    return {

        "Total_Trades": total,

        "Completed_Trades": completed,

        "Wins": wins,

        "Stops": stops,

        "Open": open_positions,

        "Win_Rate_%": round(
            win_rate,
            2
        ),

        "Average_Return_%": round(
            avg_return,
            2
        ),

        "Average_Risk_Reward": round(
            avg_rr,
            2
        )

    }



def save_metrics(metrics):


    row = {

        "Date":

        datetime.datetime.now(),

        **metrics

    }



    new_df = pd.DataFrame(
        [row]
    )



    if os.path.exists(METRICS_FILE):

        old = pd.read_csv(
            METRICS_FILE
        )

        new_df = pd.concat(
            [
                old,
                new_df
            ],
            ignore_index=True
        )



    new_df.to_csv(
        METRICS_FILE,
        index=False
    )



def monitor_model():


    print("\n")
    print("=" * 60)
    print("MODEL PERFORMANCE MONITOR")
    print("=" * 60)



    model = load_model_info()


    print("\nMODEL:")
    print(
        model
    )



    df = load_trade_data()



    metrics = calculate_performance(
        df
    )



    print("\nPERFORMANCE:")
    
    for key,value in metrics.items():

        print(
            key,
            ":",
            value
        )



    save_metrics(
        metrics
    )



    print("\nMonitoring saved:")
    print(
        METRICS_FILE
    )



if __name__ == "__main__":

    monitor_model()
