import pandas as pd
import numpy as np
import json
from datetime import datetime
import os


# ============================================================
# Optimization Profiles
# ============================================================

PROFILES = {


    "AGGRESSIVE": {

        "MIN_TRADES": 100,
        "MIN_SYMBOLS": 10,

        "MIN_WIN_RATE": 25,
        "MIN_PROFIT_FACTOR": 1.5,
        "MIN_EXPECTANCY": 5,

        "MAX_DRAWDOWN": 70

    },


    "BALANCED": {

        "MIN_TRADES": 125,
        "MIN_SYMBOLS": 10,

        "MIN_WIN_RATE": 30,
        "MIN_PROFIT_FACTOR": 2.0,
        "MIN_EXPECTANCY": 5,

        "MAX_DRAWDOWN": 55

    },


    "CONSERVATIVE": {

        "MIN_TRADES": 200,
        "MIN_SYMBOLS": 25,

        "MIN_WIN_RATE": 45,
        "MIN_PROFIT_FACTOR": 2.5,
        "MIN_EXPECTANCY": 3,

        "MAX_DRAWDOWN": 35

    }

}



CURRENT_PROFILE = "BALANCED"



PROFILE = PROFILES[CURRENT_PROFILE]



TARGET_TRADES = 500
TARGET_SYMBOLS = 40


# ============================================================
# Drawdown Calculation
# ============================================================

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



# ============================================================
# Metrics
# ============================================================

def calculate_metrics(filtered):


    returns = pd.to_numeric(
        filtered["Return_%"],
        errors="coerce"
    ).dropna()


    if len(returns) < PROFILE["MIN_TRADES"]:
        return None



    wins = returns[returns > 0]

    losses = returns[returns < 0]


    if len(losses) == 0:
        return None



    # Calculate win rate FIRST

    win_rate = (
        len(wins)
        /
        len(returns)
    ) * 100



    # Calculate symbols FIRST

    unique_symbols = (
        filtered["Symbol"]
        .nunique()
    )



    print(
        "DEBUG:",
        "Trades:",
        len(returns),
        "Symbols:",
        unique_symbols,
        "Win:",
        round(win_rate,2)
    )



    if len(returns) >= 150:

        print(
            "VALIDATION:",
            len(returns),
            "trades",
            unique_symbols,
            "symbols"
        )



    avg_return = returns.mean()



    avg_win = (
        wins.mean()
        if len(wins) > 0
        else 0
    )



    avg_loss = abs(
        losses.mean()
    )



    if abs(losses.sum()) == 0:
        return None



    profit_factor = (

        wins.sum()
        /
        abs(losses.sum())

    )



    if profit_factor < PROFILE["MIN_PROFIT_FACTOR"]:
        return None



    expectancy = (

        (win_rate / 100) * avg_win

        -

        ((1 - win_rate / 100) * avg_loss)

    )



    if expectancy < PROFILE["MIN_EXPECTANCY"]:
        return None



    stop_rate = (

        len(
            filtered[
                filtered["Result"] == "STOP HIT"
            ]
        )
        /
        len(filtered)

    ) * 100



    target_rate = (

        len(
            filtered[
                filtered["Result"] == "TARGET 1 HIT"
            ]
        )
        /
        len(filtered)

    ) * 100



    max_drawdown = calculate_drawdown(
        returns
    )



    if max_drawdown > PROFILE["MAX_DRAWDOWN"]:
        return None



    sharpe_like = (

        avg_return /
        returns.std()

        if returns.std() != 0

        else 0

    )



    if unique_symbols < PROFILE["MIN_SYMBOLS"]:
        return None

    if len(returns) / unique_symbols < 8:
        return None


    avg_trades_symbol = (

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
            round(avg_trades_symbol,2),

        "Win_Rate":
            round(win_rate,2),

        "Average_Return":
            round(avg_return,3),

        "Avg_Win":
            round(avg_win,3),

        "Avg_Loss":
            round(avg_loss,3),

        "Profit_Factor":
            round(profit_factor,3),

        "Expectancy":
            round(expectancy,3),

        "Stop_Loss_Rate":
            round(stop_rate,2),

        "Target_Hit_Rate":
            round(target_rate,2),

        "Max_Drawdown":
            round(max_drawdown,2),

        "Sharpe_Like":
            round(sharpe_like,3)

    }

# ============================================================
# Reliability Score
# ============================================================

def calculate_reliability(metrics):


    trade_score = min(
        metrics["Trades"] /
        TARGET_TRADES,
        1
    )


    symbol_score = min(
        metrics["Unique_Symbols"] /
        TARGET_SYMBOLS,
        1
    )


    diversity_score = (

        1 /
        metrics["Avg_Trades_Per_Symbol"]

        if metrics["Avg_Trades_Per_Symbol"] > 0

        else 0

    )



    reliability = (

        trade_score * 50

        +

        symbol_score * 40

        +

        min(
            diversity_score,
            0.5
        )
        * 20

    )



    return round(
        reliability,
        2
    )



# ============================================================
# Consistency Score
# ============================================================

def calculate_consistency(metrics):

    score = 0


    if metrics["Profit_Factor"] >= 2:
        score += 30

    elif metrics["Profit_Factor"] >= 1.5:
        score += 20


    if metrics["Expectancy"] > 5:
        score += 30

    elif metrics["Expectancy"] > 0:
        score += 15



    if metrics["Unique_Symbols"] >= 25:
        score += 20

    elif metrics["Unique_Symbols"] >= 10:
        score += 10



    if metrics["Max_Drawdown"] < 30:
        score += 20

    elif metrics["Max_Drawdown"] < 50:
        score += 10


    return score


# ============================================================
# Optimizer Score
# ============================================================

def calculate_score(metrics):


    score = (

        metrics["Expectancy"] * 5

        +

        metrics["Profit_Factor"] * 10

        +

        metrics["Win_Rate"] * 0.60

        +

        metrics["Sharpe_Like"] * 20

        -

        metrics["Max_Drawdown"] * 1.5 

        +

        metrics["Reliability_Score"] * 0.5

        +

        metrics["Consistency_Score"]

    )


    if metrics["Unique_Symbols"] >= 25:

        score *= 1.25

    if metrics["Unique_Symbols"] < 10:
        score *= 0.75


    elif metrics["Unique_Symbols"] < 15:

        score *= 0.85


    return round(score,2)



# ============================================================
# Candidate Generation
# ============================================================

def generate_candidates(series):


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



# ============================================================
# Threshold Evaluation
# ============================================================

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



    metrics["Reliability_Score"] = calculate_reliability(
        metrics
    )


    metrics["Consistency_Score"] = calculate_consistency(
        metrics
    )


    metrics["Optimizer_Score"] = calculate_score(
        metrics
    )


    return metrics



# ============================================================
# Optimization
# ============================================================

def optimize(dataset, profile_name):

    global CURRENT_PROFILE
    global PROFILE


    CURRENT_PROFILE = profile_name

    PROFILE = PROFILES[profile_name]


    print(
        "Optimization Profile:",
        CURRENT_PROFILE
    )
    print(
        "\nLoading trade database..."
    )


    df = pd.read_csv(
        dataset,
        low_memory=False
    )


    df = df[
        df["Result"].isin(
            [
                "TARGET 1 HIT",
                "STOP HIT"
            ]
        )
    ].copy()



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



    numeric = [

        "Return_%",

        "Rank_Score",

        "Confidence_Score",

        "Research_Score",

        "Risk_Reward"

    ]



    for col in numeric:

        df[col] = pd.to_numeric(
            df[col],
            errors="coerce"
        )



    df = df.dropna(
        subset=numeric
    )



    df["Risk_Reward"] = df["Risk_Reward"].clip(
        0,
        10
    )



    candidates = {

        col:
        generate_candidates(df[col])

        for col in [

            "Rank_Score",

            "Confidence_Score",

            "Research_Score",

            "Risk_Reward"

        ]

    }



    results=[]



    for r in candidates["Rank_Score"]:

        for c in candidates["Confidence_Score"]:

            for s in candidates["Research_Score"]:

                for rr in candidates["Risk_Reward"]:


                    result = evaluate_threshold(

                        df,
                        r,
                        c,
                        s,
                        rr

                    )


                    if result:

                        results.append(
                            result
                        )



    results_df = pd.DataFrame(
        results
    )



    if len(results_df)==0:

        return results_df



    results_df = results_df.drop_duplicates(

        subset=[

            "Rank_Threshold",

            "Confidence_Threshold",

            "Research_Threshold",

            "Risk_Reward_Threshold"

        ]

    )



    return results_df.sort_values(

        "Optimizer_Score",

        ascending=False

    )



# ============================================================
# Save
# ============================================================

def save_optimal_thresholds(results):


    best = results.iloc[0]


    output = {

         "Profile":
            best["Profile"],

        "Rank_Score":
            float(best["Rank_Threshold"]),


        "Confidence_Score":
            float(best["Confidence_Threshold"]),


        "Research_Score":
            float(best["Research_Threshold"]),


        "Risk_Reward":
            float(best["Risk_Reward_Threshold"]),


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
            output,
            f,
            indent=4
        )



    results.head(25).to_json(

        "data/models/top_thresholds.json",

        orient="records",

        indent=4

    )



# ============================================================
# Main
# ============================================================

if __name__ == "__main__":


    all_results = []


    for profile in PROFILES:


        results = optimize(
            "data/trade_database.csv",
            profile
        )


        if len(results) > 0:

            results["Profile"] = profile

            all_results.append(results)



    if len(all_results) == 0:

        print(
            "No valid thresholds found"
        )

        exit()



    results = pd.concat(
        all_results,
        ignore_index=True
    )


    results = results.sort_values(
        "Optimizer_Score",
        ascending=False
    )


    print(
        "\n===== BEST THRESHOLDS =====\n"
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


    # Save only best overall threshold

    save_optimal_thresholds(
        results
    )


    print(
        "\nThreshold optimization completed."
    )