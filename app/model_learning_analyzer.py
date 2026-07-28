import os
import pandas as pd


INPUT_FILE = (
    "data/models/model_feedback.csv"
)

OUTPUT_FILE = (
    "data/models/model_learning_report.csv"
)



def analyze_numeric(df, column, bins):

    if column not in df.columns:
        return None


    temp = df.copy()


    temp["Category"] = pd.cut(
        temp[column],
        bins=bins
    )


    result = (
        temp
        .groupby(
            "Category",
            observed=False
        )
        .agg(
            Trades=("Prediction_Correct", "count"),
            Accuracy=("Prediction_Correct", "mean"),
            Avg_Return_5D=("Return_5D", "mean")
        )
        .reset_index()
    )


    result["Accuracy"] = (
        result["Accuracy"] * 100
    )


    result["Analysis"] = column


    return result



def analyze_category(df, column):

    if column not in df.columns:
        return None


    result = (
        df
        .groupby(
            column,
            observed=False
        )
        .agg(
            Trades=("Prediction_Correct","count"),
            Accuracy=("Prediction_Correct","mean"),
            Avg_Return_5D=("Return_5D","mean")
        )
        .reset_index()
    )


    result["Accuracy"] = (
        result["Accuracy"] * 100
    )


    result["Analysis"] = column


    result = result.rename(
        columns={
            column:"Category"
        }
    )


    return result



def generate_learning_report():


    print()
    print("=" * 50)
    print("MODEL FEATURE LEARNING ANALYZER")
    print("=" * 50)



    if not os.path.exists(INPUT_FILE):

        print(
            "Feedback file not found"
        )

        return



    df = pd.read_csv(
        INPUT_FILE
    )


    print()

    print(
        "Trades analyzed:",
        len(df)
    )



    reports = []



    # -------------------------
    # ML Probability
    # -------------------------

    report = analyze_numeric(
        df,
        "ML_Probability",
        [
            0,
            10,
            25,
            50,
            75,
            100
        ]
    )

    if report is not None:
        reports.append(report)



    # -------------------------
    # AI Score
    # -------------------------

    report = analyze_numeric(
        df,
        "AI_Final_Score",
        [
            0,
            30,
            45,
            60,
            100
        ]
    )

    if report is not None:
        reports.append(report)



    # -------------------------
    # RSI
    # -------------------------

    report = analyze_numeric(
        df,
        "RSI",
        [
            0,
            30,
            40,
            50,
            60,
            70,
            100
        ]
    )

    if report is not None:
        reports.append(report)



    # -------------------------
    # 5 Day Momentum
    # -------------------------

    report = analyze_numeric(
        df,
        "Return_5D",
        [
            -100,
            -10,
            -5,
            0,
            5,
            10,
            100
        ]
    )

    if report is not None:
        reports.append(report)



    # -------------------------
    # 20 Day Momentum
    # -------------------------

    report = analyze_numeric(
        df,
        "Return_20D",
        [
            -100,
            -10,
            0,
            10,
            20,
            100
        ]
    )

    if report is not None:
        reports.append(report)



    # -------------------------
    # Market Regime
    # -------------------------

    report = analyze_category(
        df,
        "Market_Regime"
    )

    if report is not None:
        reports.append(report)



    if reports:


        final_report = pd.concat(
            reports,
            ignore_index=True
        )


        final_report.to_csv(
            OUTPUT_FILE,
            index=False
        )


        print()

        print(
            "Learning report saved:"
        )

        print(
            OUTPUT_FILE
        )


        print()

        print(
            final_report
            .sort_values(
                "Avg_Return_5D",
                ascending=False
            )
            .head(30)
        )


    else:

        print(
            "No learning data available"
        )



if __name__ == "__main__":

    generate_learning_report()