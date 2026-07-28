"""
Feature Importance Analyzer

Automatically reads feature names
from trained ML model.
"""

import joblib
import pandas as pd


MODEL_FILE = (
    "data/models/historical_trading_model.pkl"
)



def get_feature_importance():


    print("\nLoading model...\n")


    model = joblib.load(
        MODEL_FILE
    )


    print(
        "Model type:",
        type(model).__name__
    )


    importance = (
        model.feature_importances_
    )


    features = (
        model.feature_names_in_
    )


    print(
        "Features:",
        len(features)
    )


    print(
        "Importance values:",
        len(importance)
    )



    importance_df = pd.DataFrame(
        {
            "Feature": features,
            "Importance": importance
        }
    )


    importance_df = importance_df.sort_values(
        by="Importance",
        ascending=False
    )


    return importance_df




if __name__ == "__main__":


    print(
        "\n========== FEATURE IMPORTANCE ==========\n"
    )


    df = get_feature_importance()


    print(
        df.to_string(
            index=False
        )
    )


    print(
        "\n========== TOP 10 FEATURES ==========\n"
    )


    print(
        df.head(10)
        .to_string(
            index=False
        )
    )
