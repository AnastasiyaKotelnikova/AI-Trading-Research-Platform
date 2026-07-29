"""
Adaptive Strategy Learner v1.5

Purpose:
- Learn from completed trades
- Measure strategy performance
- Adjust strategy weights automatically
- Save updated strategy intelligence

Input:
    data/trade_database.csv
    data/models/strategy_weights.json

Output:
    data/models/adaptive_strategy_weights.json
"""

import os
import json
import pandas as pd
from datetime import datetime


INPUT_TRADES = "data/trade_database.csv"
INPUT_WEIGHTS = "data/models/strategy_weights.json"
OUTPUT_WEIGHTS = "data/models/adaptive_strategy_weights.json"


def load_data():

    print("\nLoading trade database...")

    df = pd.read_csv(
        INPUT_TRADES,
        low_memory=False
    )

    print(f"Trades loaded: {len(df)}")

    return df


def load_strategy_weights():

    print("\nLoading strategy weights...")

    if os.path.exists(INPUT_WEIGHTS):

        with open(INPUT_WEIGHTS, "r") as f:
            data = json.load(f)

        return data["Strategies"]

    else:
        print("No previous weights found")
        return {}


def calculate_strategy_performance(df):

    print("\nCalculating strategy performance...")

    results = []

    grouped = df.groupby("Strategy")

    for strategy, group in grouped:

        trades = len(group)

        if trades < 10:
            continue


        wins = group[group["Result"].astype(str).str.contains(
            "TARGET|WIN|PROFIT",
            case=False,
            na=False
        )]


        win_rate = round(
            len(wins) / trades * 100,
            2
        )


        avg_return = round(
            pd.to_numeric(
                group["Return_%"],
                errors="coerce"
            ).mean(),
            2
        )


        profit_factor = 0

        profits = pd.to_numeric(
            group["Return_%"],
            errors="coerce"
        )


        gains = profits[profits > 0].sum()
        losses = abs(profits[profits < 0].sum())


        if losses > 0:
            profit_factor = round(
                gains / losses,
                2
            )


        score = calculate_learning_score(
            win_rate,
            avg_return,
            profit_factor,
            trades
        )


        results.append(
            {
                "Strategy": strategy,
                "Trades": trades,
                "Win_Rate": win_rate,
                "Average_Return": avg_return,
                "Profit_Factor": profit_factor,
                "Learning_Score": score
            }
        )


    return pd.DataFrame(results)



def calculate_learning_score(
        win_rate,
        avg_return,
        profit_factor,
        trades
):

    score = 0


    # win rate contribution
    score += win_rate * 0.4


    # return contribution
    score += avg_return * 5


    # profit factor contribution
    score += profit_factor * 10


    # sample confidence
    confidence = min(trades / 1000, 1)

    score *= confidence


    return round(score, 2)



def update_weights(performance, old_weights):

    print("\nUpdating strategy weights...")

    updated = {}


    for _, row in performance.iterrows():

        strategy = row["Strategy"]

        old_weight = 0

        if strategy in old_weights:
            old_weight = old_weights[strategy].get(
                "Weight",
                0
            )


        learning_score = row["Learning_Score"]


        # Convert performance into adjustment
        new_weight = old_weight


        if learning_score >= 70:
            new_weight += 0.10

        elif learning_score >= 45:
            new_weight += 0.03

        elif learning_score < 25:
            new_weight -= 0.08


        # keep range safe
        new_weight = max(
            0.05,
            min(
                new_weight,
                1.0
            )
        )


        change = round(
            new_weight - old_weight,
            3
        )


        updated[strategy] = {

            "Old_Weight": round(
                old_weight,
                3
            ),

            "New_Weight": round(
                new_weight,
                3
            ),

            "Change": change,

            "Learning_Score": row["Learning_Score"],

            "Win_Rate": row["Win_Rate"],

            "Average_Return": row["Average_Return"],

            "Trades": int(row["Trades"])

        }


    return updated



def save_results(updated):

    output = {

        "Created": str(datetime.now()),

        "Engine": "Adaptive Strategy Learner v1.5",

        "Strategies": updated

    }


    os.makedirs(
        "data/models",
        exist_ok=True
    )


    with open(
        OUTPUT_WEIGHTS,
        "w"
    ) as f:

        json.dump(
            output,
            f,
            indent=4
        )


    print(
        f"\nSaved: {OUTPUT_WEIGHTS}"
    )



def main():

    df = load_data()

    old_weights = load_strategy_weights()

    performance = calculate_strategy_performance(df)


    print("\n===== STRATEGY LEARNING RESULTS =====")

    print(
        performance.to_string(
            index=False
        )
    )


    updated = update_weights(
        performance,
        old_weights
    )


    print("\n===== UPDATED WEIGHTS =====")

    for strategy, data in updated.items():

        print(
            strategy,
            "=>",
            data["New_Weight"]
        )


    save_results(updated)



if __name__ == "__main__":
    main()