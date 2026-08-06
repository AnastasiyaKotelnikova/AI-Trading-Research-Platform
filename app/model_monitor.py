import pandas as pd
import os


TRADE_DATABASE = "data/trade_history.csv"

METRICS_FILE = (
    "data/models/model_metrics.csv"
)



# =====================================================
# LOAD DATA
# =====================================================

def load_database():

    if not os.path.exists(DATABASE_FILE):

        print(
            "Trading database not found"
        )

        return None


    df = pd.read_csv(
        DATABASE_FILE,
        low_memory=False
    )


    return df



# =====================================================
# TRADE PERFORMANCE
# =====================================================

def trade_performance(df):


    print(
        "\n========== TRADE PERFORMANCE =========="
    )


    total_records = len(df)


    print(
        "\nTotal Database Records:",
        total_records
    )



    if "Return_%" not in df.columns:

        print(
            "Return data unavailable"
        )

        return



    # Only completed trades

    completed = df[
        df["Return_%"].notna()
    ]


    completed = completed[
        completed["Return_%"] != ""
    ]



    completed["Return_%"] = pd.to_numeric(
        completed["Return_%"],
        errors="coerce"
    )


    completed = completed.dropna(
        subset=["Return_%"]
    )



    total = len(completed)



    print(
        "Completed Trades:",
        total
    )



    if total == 0:

        print(
            "No completed trades available"
        )

        return



    average_return = (
        completed["Return_%"]
        .mean()
    )


    print(
        "\nAverage Return:",
        round(
            average_return,
            2
        ),
        "%"
    )



    winners = completed[
        completed["Return_%"] > 0
    ]


    losers = completed[
        completed["Return_%"] <= 0
    ]



    print(
        "\nWinning Trades:",
        len(winners)
    )


    print(
        "Losing Trades:",
        len(losers)
    )



    win_rate = (

        len(winners)
        /
        total
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



    average_win = 0

    average_loss = 0



    if len(winners) > 0:

        average_win = (
            winners["Return_%"]
            .mean()
        )


        print(
            "Average Winner:",
            round(
                average_win,
                2
            ),
            "%"
        )



    if len(losers) > 0:

        average_loss = (
            losers["Return_%"]
            .mean()
        )


        print(
            "Average Loser:",
            round(
                average_loss,
                2
            ),
            "%"
        )



    profit_factor = (

        winners["Return_%"].sum()
        /
        abs(
            losers["Return_%"].sum()
        )

        if len(losers) > 0

        else 0

    )



    print(
        "Profit Factor:",
        round(
            profit_factor,
            2
        )
    )



    # ================================
    # EXPECTANCY
    # ================================

    loss_rate = (
        len(losers)
        /
        total
    )



    win_probability = (
        len(winners)
        /
        total
    )



    expectancy = (

        (
            win_probability
            *
            average_win
        )

        -

        (
            loss_rate
            *
            abs(average_loss)
        )

    )



    print(
        "Expectancy:",
        round(
            expectancy,
            2
        ),
        "%"
    )



    return {

        "Completed": total,

        "Win_Rate": win_rate,

        "Average_Return":
            average_return,

        "Expectancy":
            expectancy

    }




# =====================================================
# STRATEGY PERFORMANCE
# =====================================================

def strategy_performance(df):


    print(
        "\n========== STRATEGY PERFORMANCE =========="
    )


    if "Strategy" not in df.columns:

        print(
            "Strategy data unavailable"
        )

        return



    result = (

        df.groupby(
            "Strategy"
        )["Return_%"]

        .agg(
            [
                "count",
                "mean"
            ]
        )

        .sort_values(
            "mean",
            ascending=False
        )

    )


    print(result)



# =====================================================
# CONFIDENCE PERFORMANCE
# =====================================================

def confidence_performance(df):


    print(
        "\n========== CONFIDENCE PERFORMANCE =========="
    )


    if "Confidence_Score" not in df.columns:

        print(
            "Confidence data unavailable"
        )

        return



    result = (

        df.groupby(
            "Confidence_Score"
        )["Return_%"]

        .agg(
            [
                "count",
                "mean"
            ]
        )

        .sort_values(
            "mean",
            ascending=False
        )

    )


    print(result)



# =====================================================
# MODEL HISTORY
# =====================================================

def model_history():


    print(
        "\n========== MODEL HISTORY =========="
    )


    if not os.path.exists(
        METRICS_FILE
    ):

        print(
            "No model history"
        )

        return



    df = pd.read_csv(
        METRICS_FILE
    )



    columns = [

        "Model",
        "Accuracy",
        "F1",
        "Status"

    ]



    available = [

        c

        for c in columns

        if c in df.columns

    ]



    print(

        df[available]
        .tail(10)

    )



# =====================================================
# FUTURE MODEL SCORE
# =====================================================

def model_recommendation(metrics):


    print(
        "\n========== MODEL EVALUATION SCORE =========="
    )


    if metrics is None:

        return



    score = (

        metrics["Win_Rate"]
        *
        0.30

        +

        metrics["Expectancy"]
        *
        0.20

        +

        min(
            metrics["Completed"] / 1000,
            10
        )
        *
        1

    )



    print(
        "Trading Quality Score:",
        round(
            score,
            2
        )
    )



    print(
        """
Future Champion Selection:

40%  ML F1 Score
30%  Win Rate
20%  Expectancy
10%  Trade Volume

Goal:
Select models based on prediction quality
AND actual trading performance.
"""
    )



# =====================================================
# MAIN
# =====================================================

def monitor_model():


    print(
        "\n========== AI PERFORMANCE MONITOR =========="
    )


    df = load_database()


    if df is None:

        return



    metrics = trade_performance(df)

    strategy_performance(df)

    confidence_performance(df)

    model_history()

    model_recommendation(metrics)



    print(
        "\n============================================"
    )



if __name__ == "__main__":

    monitor_model()