import pandas as pd
import os


METRICS_FILE = (
    "data/models/model_metrics.csv"
)

PERFORMANCE_FILE = (
    "data/models/model_champion_status.csv"
)

OUTPUT_FILE = (
    "data/models/model_quality_report.csv"
)

RECOMMENDED_FILE = (
    "data/models/recommended_champion.txt"
)



def evaluate_models():


    print(
        "\n========== MODEL QUALITY EVALUATION =========="
    )


    if not os.path.exists(METRICS_FILE):

        print(
            "Model metrics missing"
        )

        return



    metrics = pd.read_csv(
        METRICS_FILE
    )



    if os.path.exists(PERFORMANCE_FILE):

        performance = pd.read_csv(
            PERFORMANCE_FILE
        )


        # Remove duplicate columns if CSV schema changed
        performance = performance.loc[
            :,
            ~performance.columns.duplicated()
        ]


        performance["Evaluation_Date"] = pd.to_datetime(
            performance["Evaluation_Date"]
        )


        performance = (
            performance
            .sort_values(
                "Evaluation_Date"
            )
            .groupby(
                "Active_Model"
            )
            .last()
            .reset_index()
        )


        # Remove old Model column if present
        performance = performance.drop(
            columns=[
                "Model"
            ],
            errors="ignore"
        )


        performance = performance.rename(
            columns={
                "Active_Model": "Model"
            }
        )


        performance = performance[
            [
                "Model",
                "Completed_Trades",
                "Win_Rate",
                "Average_Return"
            ]
        ].drop_duplicates(
            subset=[
                "Model"
            ]
        )


        df = metrics.merge(
            performance,
            on="Model",
            how="left",
            suffixes=(
                "_metrics",
                "_performance"
            )
        )


        # Use live trading performance
        df["Win_Rate"] = (
            df["Win_Rate_performance"]
            .fillna(
                df.get(
                    "Win_Rate_metrics",
                    0
                )
            )
        )


        df["Average_Return"] = (
            df["Average_Return_performance"]
            .fillna(
                df.get(
                    "Average_Return_metrics",
                    0
                )
            )
        )


    else:

        df = metrics.copy()



    for column in [
        "Completed_Trades",
        "Win_Rate",
        "Average_Return"
    ]:

        if column not in df.columns:

            df[column] = 0


        df[column] = (
            df[column]
            .fillna(0)
        )



    # ================================
    # MODEL QUALITY SCORE
    # ================================

    df["Trading_Quality_Score"] = (

        df["F1"] * 100 * 0.40

        +

        df["Win_Rate"] * 0.30

        +

        df["Average_Return"] * 0.20

        +

        (
            df["Completed_Trades"]
            /
            max(
                df["Completed_Trades"].max(),
                1
            )
            *
            100
            *
            0.10
        )

    )



    result = df.sort_values(
        "Trading_Quality_Score",
        ascending=False
    )



    print(
        result[
            [
                "Model",
                "F1",
                "Win_Rate",
                "Average_Return",
                "Completed_Trades",
                "Trading_Quality_Score"
            ]
        ]
    )



    result.to_csv(
        OUTPUT_FILE,
        index=False
    )



    # ================================
    # RECOMMEND CHAMPION
    # ================================

    recommended_model = (
        result.iloc[0]["Model"]
    )


    with open(
        RECOMMENDED_FILE,
        "w"
    ) as f:

        f.write(
            str(recommended_model)
        )



    print(
        "\nSaved:"
    )

    print(
        OUTPUT_FILE
    )


    print(
        "\nRecommended Champion:"
    )

    print(
        recommended_model
    )




if __name__ == "__main__":

    evaluate_models()