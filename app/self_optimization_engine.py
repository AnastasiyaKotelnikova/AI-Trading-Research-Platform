"""
Self Optimization Engine v1.7 Step 1

Purpose:
---------
Creates adaptive intelligence weights from previous learning.

Input:
    data/models/adaptive_strategy_weights.json
    data/models/ai_feedback_weights.json
    data/results/strategy_intelligence_report.csv

Outputs:
    data/models/self_optimization_weights.json
    data/results/self_optimization_report.csv


Features:
    - Strategy improvement detection
    - Feedback integration
    - Adaptive confidence scoring
    - Future ranking optimization
"""


import os
import json
import pandas as pd
from datetime import datetime



ADAPTIVE_FILE = (
    "data/models/adaptive_strategy_weights.json"
)

FEEDBACK_FILE = (
    "data/models/ai_feedback_weights.json"
)

STRATEGY_REPORT = (
    "data/results/strategy_intelligence_report.csv"
)


OUTPUT_REPORT = (
    "data/results/self_optimization_report.csv"
)


OUTPUT_WEIGHTS = (
    "data/models/self_optimization_weights.json"
)



def load_json(path):

    with open(path, "r") as f:

        return json.load(f)



def load_data():

    print("\nLoading intelligence data...")


    adaptive = load_json(
        ADAPTIVE_FILE
    )


    feedback = load_json(
        FEEDBACK_FILE
    )


    strategy = pd.read_csv(
        STRATEGY_REPORT,
        low_memory=False
    )


    return adaptive, feedback, strategy



def calculate_optimization(
        adaptive,
        feedback,
        strategy
):

    print(
        "\nCalculating optimization scores..."
    )


    results = []


    feedback_weights = (
        feedback
        .get(
            "Feedback_Weights",
            {}
        )
    )


    adaptive_weights = (
        adaptive
        .get(
            "Strategies",
            {}
        )
    )


    for _, row in strategy.iterrows():


        name = row["Strategy"]


        current_weight = (

            adaptive_weights
            .get(
                name,
                {}
            )
            .get(
                "New_Weight",
                0.1
            )

        )


        related_feedback = []


        for key,value in feedback_weights.items():

            if name in key:

                related_feedback.append(
                    value
                )


        if related_feedback:

            feedback_score = (
                sum(related_feedback)
                /
                len(related_feedback)
            )

        else:

            feedback_score = 0.1



        optimization_score = (

            current_weight * 50

            +

            feedback_score * 50

        )


        results.append(

            {

                "Strategy":
                    name,

                "Current_Weight":
                    round(
                        current_weight,
                        3
                    ),

                "Feedback_Weight":
                    round(
                        feedback_score,
                        3
                    ),

                "Optimization_Score":
                    round(
                        optimization_score,
                        2
                    )

            }

        )


    return pd.DataFrame(results)



def create_weights(report):


    weights = {}


    for _,row in report.iterrows():


        weights[
            row["Strategy"]
        ] = round(

            row["Optimization_Score"]
            /
            100,

            3

        )


    return {

        "Created":
            str(datetime.now()),

        "Optimization_Status":
            "ACTIVE",

        "Strategy_Optimization_Weights":
            weights

    }



def main():

    print(
        "\n=============================="
    )

    print(
        "Self Optimization Engine v1.7"
    )

    print(
        "==============================\n"
    )


    adaptive, feedback, strategy = (
        load_data()
    )


    report = calculate_optimization(
        adaptive,
        feedback,
        strategy
    )


    weights = create_weights(
        report
    )


    os.makedirs(
        "data/results",
        exist_ok=True
    )


    os.makedirs(
        "data/models",
        exist_ok=True
    )


    report.to_csv(
        OUTPUT_REPORT,
        index=False
    )


    with open(
        OUTPUT_WEIGHTS,
        "w"
    ) as f:

        json.dump(
            weights,
            f,
            indent=4
        )


    print(
        "\n===== OPTIMIZATION RESULTS ====="
    )


    print(
        report
        .sort_values(
            "Optimization_Score",
            ascending=False
        )
        .to_string(
            index=False
        )
    )


    print(
        "\nSaved:",
        OUTPUT_REPORT
    )


    print(
        "Saved:",
        OUTPUT_WEIGHTS
    )


    print(
        "\nCompleted:",
        datetime.now()
    )



if __name__ == "__main__":
    main()