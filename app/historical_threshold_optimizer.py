import pandas as pd
import numpy as np
import json
from datetime import datetime
import os


MIN_TRADES = 75
MIN_SYMBOLS = 10


def calculate_drawdown(returns):

    equity = (
        1 + returns / 100
    ).cumprod()

    peak = equity.cummax()

    drawdown = (
        (equity - peak)
        /
        peak
    ) * 100

    return abs(drawdown.min())



def calculate_metrics(filtered):

    returns = pd.to_numeric(
        filtered["Return_%"],
        errors="coerce"
    ).dropna()


    if len(returns) < MIN_TRADES:
        return None


    wins = returns[
        returns > 0
    ]

    losses = returns[
        returns < 0
    ]


    if len(losses) == 0:
        return None



    win_rate = (
        len(wins)
        /
        len(returns)
    ) * 100



    avg_return = returns.mean()


    avg_win = (
        wins.mean()
        if len(wins) > 0
        else 0
    )


    avg_loss = abs(
        losses.mean()
    )



    profit_factor = (

        wins.sum()
        /
        abs(losses.sum())

    )



    expectancy = (

        (win_rate / 100) * avg_win

        -

        ((1 - win_rate / 100) * avg_loss)

    )



    stop_rate = (

        len(
            filtered[
                filtered["Result"]
                ==
                "STOP HIT"
            ]
        )
        /
        len(filtered)

    ) * 100



    target_rate = (

        len(
            filtered[
                filtered["Result"]
                ==
                "TARGET 1 HIT"
            ]
        )
        /
        len(filtered)

    ) * 100



    max_drawdown = calculate_drawdown(
        returns
    )



    sharpe_like = (

        avg_return
        /
        returns.std()

        if returns.std() != 0

        else 0

    )



    unique_symbols = (
        filtered["Symbol"]
        .nunique()
    )


    if unique_symbols < MIN_SYMBOLS:
        return None



    avg_trades_per_symbol = (

        len(filtered)
        /
        unique_symbols

    )


    return {

        "Trades":
            len(filtered),

        "Unique_Symbols":
            unique_symbols,

        "Avg_Trades_Per_Symbol":
            round(
                avg_trades_per_symbol,
                2
            ),

        "Win_Rate":
            round(
                win_rate,
                2
            ),

        "Average_Return":
            round(
                avg_return,
                2
            ),

        "Avg_Win":
            round(
                avg_win,
                2
            ),

        "Avg_Loss":
            round(
                avg_loss,
                2
            ),

        "Profit_Factor":
            round(
                profit_factor,
                2
            ),

        "Expectancy":
            round(
                expectancy,
                2
            ),

        "Stop_Loss_Rate":
            round(
                stop_rate,
                2
            ),

        "Target_Hit_Rate":
            round(
                target_rate,
                2
            ),

        "Max_Drawdown":
            round(
                max_drawdown,
                2
            ),

        "Sharpe_Like":
            round(
                sharpe_like,
                3
            )

    }



def calculate_score(metrics):


    score = (

        metrics["Expectancy"] * 5

        +

        metrics["Profit_Factor"] * 10

        +

        metrics["Win_Rate"] * 0.35

        +

        metrics["Sharpe_Like"] * 25

        -

        metrics["Max_Drawdown"] * 2

    )


    # reward diversification

    if metrics["Unique_Symbols"] >= 25:

        score *= 1.25


    elif metrics["Unique_Symbols"] < 10:

        score *= 0.5



    return round(
        score,
        2
    )


    values=[]


    for p in percentiles:


        value = series.quantile(
            p / 100
        )


        if pd.notna(value):

            values.append(
                round(
                    float(value),
                    2
                )
            )



    return sorted(
        list(set(values))
    )


def generate_candidates(series):

    """
    Generate realistic threshold candidates.

    Uses percentiles instead of fixed values
    to adapt to changing score distributions.
    """

    percentiles = [
        40,
        50,
        60,
        70,
        75,
        80,
        85,
        90,
        95
    ]

    values = []

    for p in percentiles:

        value = series.quantile(
            p / 100
        )

        values.append(
            round(float(value),2)
        )


    return sorted(
        list(set(values))
    )



def evaluate_threshold(
        df,
        rank,
        confidence,
        research,
        risk_reward
):


    filtered = df[

        (df["Rank_Score"] >= rank)

        &

        (df["Confidence_Score"] >= confidence)

        &

        (df["Research_Score"] >= research)

        &

        (df["Risk_Reward"] >= risk_reward)

    ].copy()



    if len(filtered) < MIN_TRADES:
        return None


    metrics = calculate_metrics(
        filtered
    )


    if metrics is None:
        return None



    metrics.update({

        "Rank_Threshold":
            rank,

        "Confidence_Threshold":
            confidence,

        "Research_Threshold":
            research,

        "Risk_Reward_Threshold":
            risk_reward

    })



    metrics["Optimizer_Score"] = calculate_score(
        metrics
    )


    return metrics


def save_optimal_thresholds(results):

    if len(results) == 0:

        print(
            "No valid thresholds found"
        )

        return


    best = results.iloc[0]


    thresholds = {

        "Rank_Score":
            float(best["Rank_Threshold"]),

        "Confidence_Score":
            float(best["Confidence_Threshold"]),

        "Research_Score":
            float(best["Research_Threshold"]),

        "Risk_Reward":
            float(best["Risk_Reward_Threshold"]),


        "Minimum_Trades":
            MIN_TRADES,

        "Minimum_Symbols":
            MIN_SYMBOLS,


        "Optimizer_Score":
            float(best["Optimizer_Score"]),


        "Created":
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
    }


    os.makedirs(
        "data/models",
        exist_ok=True
    )


    with open(
        "data/models/optimal_thresholds.json",
        "w"
    ) as f:

        json.dump(
            thresholds,
            f,
            indent=4
        )


    print(
        "\nSaved:"
        " data/models/optimal_thresholds.json"
    )


    # Save top candidates
    results.head(25).to_json(
        "data/models/top_thresholds.json",
        orient="records",
        indent=4
    )


    print(
        "Saved:"
        " data/models/top_thresholds.json"
    )

def optimize(dataset):

    print("\nLoading trade database...")


    df = pd.read_csv(
        dataset,
        low_memory=False
    )


    print(
        "Total rows loaded:",
        len(df)
    )


    print("\nResult distribution:")
    print(
        df["Result"].value_counts()
    )


    # Only completed trades
    df = df[
        df["Result"].isin(
            [
                "TARGET 1 HIT",
                "STOP HIT"
            ]
        )
    ].copy()


    # Remove duplicate forward-test snapshots
    # Keep the highest quality signal for the same stock/date

    df = (
        df
        .sort_values(
            "Rank_Score",
            ascending=False
        )
        .drop_duplicates(
            subset=[
                "Symbol",
                "Scan_Date"
            ],
            keep="first"
        )
    )


    print(
        "\nUnique trades after deduplication:",
        len(df)
    )


    numeric_columns = [

        "Return_%",

        "Rank_Score",

        "Confidence_Score",

        "Research_Score",

        "Risk_Reward"

    ]


    for col in numeric_columns:

        df[col] = pd.to_numeric(
            df[col],
            errors="coerce"
        )


    df = df.dropna(
        subset=numeric_columns
    )


    df["Risk_Reward"] = df["Risk_Reward"].clip(
        0,
        10
    )


    print(
        "\nTrades used:",
        len(df)
    )


    print(
        "Unique Symbols:",
        df["Symbol"].nunique()
    )


    print(
        "Date Range:",
        df["Scan_Date"].min(),
        "to",
        df["Scan_Date"].max()
    )


    candidates = {

        "Rank_Score":
            generate_candidates(
                df["Rank_Score"]
            ),


        "Confidence_Score":
            generate_candidates(
                df["Confidence_Score"]
            ),


        "Research_Score":
            generate_candidates(
                df["Research_Score"]
            ),


        "Risk_Reward":
            generate_candidates(
                df["Risk_Reward"]
            )

    }


    print("\nCandidates:")

    for key,value in candidates.items():

        print(
            key,
            value
        )


    results = []


    for rank in candidates["Rank_Score"]:

        for confidence in candidates["Confidence_Score"]:

            for research in candidates["Research_Score"]:

                for rr in candidates["Risk_Reward"]:


                    result = evaluate_threshold(

                        df,

                        rank,

                        confidence,

                        research,

                        rr

                    )


                    if result:

                        results.append(
                            result
                        )


    results_df = pd.DataFrame(
        results
    )


    if len(results_df) == 0:

        return results_df


    # Remove duplicate outcomes
    results_df = results_df.drop_duplicates(
        subset=[
            "Trades",
            "Unique_Symbols",
            "Win_Rate",
            "Average_Return",
            "Profit_Factor",
            "Expectancy"
        ]
    )


    return results_df.sort_values(
        "Optimizer_Score",
        ascending=False
    )


if __name__ == "__main__":


    results = optimize(
        "data/trade_database.csv"
    )


    if len(results) == 0:

        print(
            "\nNo optimization results."
        )

        exit()



    print(
        "\n===== BEST HISTORICAL THRESHOLDS =====\n"
    )


    print(
        results.head(20)
        .to_string(index=False)
    )



    os.makedirs(
        "data/results",
        exist_ok=True
    )


    results.to_csv(

        "data/results/historical_threshold_results.csv",

        index=False

    )


    print(
        "\nSaved:"
        " data/results/historical_threshold_results.csv"
    )



    save_optimal_thresholds(
        results
    )
