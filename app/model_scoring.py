import pandas as pd
import os


METRICS_FILE = (
    "data/models/model_metrics.csv"
)

CHAMPION_FILE = (
    "data/models/model_champion_status.csv"
)


OUTPUT_FILE = (
    "data/models/model_quality_scores.csv"
)



def normalize(value, minimum, maximum):

    if maximum == minimum:
        return 0

    return (
        (value - minimum)
        /
        (maximum - minimum)
        *
        100
    )



def calculate_model_scores():

    print(
        "\n========== MODEL QUALITY SCORING =========="
    )


    if not os.path.exists(METRICS_FILE):

        print(
            "Model metrics missing"
        )

        return



    metrics = pd.read_csv(
        METRICS_FILE
    )



    # -----------------------------------------
    # Load champion trading performance
    # -----------------------------------------

    if os.path.exists(CHAMPION_FILE):

        trading = pd.read_csv(
            CHAMPION_FILE
        )


        trading = trading.rename(
            columns={
                "Active_Model": "Model",
                "Win_Rate": "Win_Rate",
                "Average_Return": "Average_Return",
                "Completed_Trades": "Completed_Trades"
            }
        )


        if os.path.exists(CHAMPION_FILE):

            trading = pd.read_csv(
                CHAMPION_FILE
            )


        trading = trading.rename(
            columns={
                "Active_Model": "Model",
                "Win_Rate": "Win_Rate",
                "Average_Return": "Average_Return",
                "Completed_Trades": "Completed_Trades"
            }
        )


        trading = trading[
            [
                "Evaluation_Date",
                "Model",
                "Win_Rate",
                "Average_Return",
                "Completed_Trades"
            ]
        ]


        trading = (
            trading
            .sort_values(
                "Evaluation_Date"
            )
            .drop_duplicates(
                "Model",
                keep="last"
            )
        )




        trading = (
            trading
            .sort_values(
                "Evaluation_Date"
                if "Evaluation_Date" in trading.columns
                else "Model"
            )
            .drop_duplicates(
                "Model",
                keep="last"
            )
        )


    else:

        trading = pd.DataFrame()



    # -----------------------------------------
    # Merge
    # -----------------------------------------

    df = metrics.merge(
        trading,
        on="Model",
        how="left"
    )



    for col in [

        "Win_Rate",
        "Average_Return",
        "Completed_Trades"

    ]:

        if col not in df.columns:

            df[col] = 0


        df[col] = (
            pd.to_numeric(
                df[col],
                errors="coerce"
            )
            .fillna(0)
        )



    # -----------------------------------------
    # Scoring
    # -----------------------------------------

    df["F1_Score"] = (
        df["F1"] * 100
    )


    df["Win_Score"] = normalize(
        df["Win_Rate"],
        0,
        100
    )


    df["Return_Score"] = normalize(
        df["Average_Return"],
        -10,
        10
    )


    df["Volume_Score"] = normalize(
        df["Completed_Trades"],
        0,
        df["Completed_Trades"].max()
    )


    df["Trading_Quality_Score"] = (

        df["F1_Score"] * 0.40

        +

        df["Win_Score"] * 0.30

        +

        df["Return_Score"] * 0.20

        +

        df["Volume_Score"] * 0.10

    )


    df = df.sort_values(
        "Trading_Quality_Score",
        ascending=False
    )



    print(
        df[
            [
                "Model",
                "F1",
                "Win_Rate",
                "Average_Return",
                "Completed_Trades",
                "Trading_Quality_Score"
            ]
        ]
        .head(10)
    )



    df.to_csv(
        OUTPUT_FILE,
        index=False
    )


    print(
        "\nSaved:"
    )

    print(
        OUTPUT_FILE
    )



if __name__ == "__main__":

    calculate_model_scores()