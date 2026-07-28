"""
Random Forest Hyperparameter Optimizer

Tests multiple Random Forest configurations
and finds the best performing model.

Metrics:
- ROC-AUC (primary)
- F1
- Accuracy
"""

import pandas as pd
import os
import joblib
from datetime import datetime

from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import (
    accuracy_score,
    f1_score,
    roc_auc_score
)


DATA_FILE = "data/historical_ml_dataset.csv"

MODEL_DIR = "data/models"

BEST_MODEL_FILE = (
    "data/models/"
    "optimized_trading_model.pkl"
)


RESULTS_FILE = (
    "data/models/"
    "model_optimization_results.csv"
)


FEATURES = [

    "Return_5D",
    "Return_10D",
    "Return_20D",

    "RSI",
    "RSI_Change",

    "SMA20",
    "SMA50",

    "Above_SMA20",
    "Above_SMA50",

    "SMA_Gap",

    "Momentum_Acceleration",

    "Average_Volume",
    "RVOL",

    "Volatility_20D",

    "ATR",
    "ATR_Percent",

    "Range_Position",

    "Distance_From_52W_High",

    "Volume_Trend"

]



PARAMETERS = [

    {
        "n_estimators": 200,
        "max_depth": 8,
        "min_samples_leaf": 5
    },

    {
        "n_estimators": 300,
        "max_depth": 10,
        "min_samples_leaf": 5
    },

    {
        "n_estimators": 500,
        "max_depth": 12,
        "min_samples_leaf": 5
    },

    {
        "n_estimators": 500,
        "max_depth": 15,
        "min_samples_leaf": 10
    },

    {
        "n_estimators": 700,
        "max_depth": 15,
        "min_samples_leaf": 5
    }

]



def optimize():

    print(
        "\n========== MODEL OPTIMIZER ==========\n"
    )


    df = pd.read_csv(
        DATA_FILE
    )


    df["Date"] = pd.to_datetime(
        df["Date"]
    )


    cutoff = (
        df["Date"]
        .quantile(0.80)
    )


    train = df[
        df["Date"] <= cutoff
    ]


    test = df[
        df["Date"] > cutoff
    ]


    X_train = train[FEATURES]

    y_train = train[
        "Successful_Trade"
    ]


    X_test = test[FEATURES]

    y_test = test[
        "Successful_Trade"
    ]



    results = []

    best_auc = 0

    best_model = None



    for i, params in enumerate(PARAMETERS):


        print(
            f"\nTraining model {i+1}/{len(PARAMETERS)}"
        )


        print(
            params
        )


        model = RandomForestClassifier(

            **params,

            class_weight="balanced",

            random_state=42,

            n_jobs=-1

        )


        model.fit(
            X_train,
            y_train
        )


        predictions = model.predict(
            X_test
        )


        probabilities = model.predict_proba(
            X_test
        )[:,1]



        accuracy = accuracy_score(
            y_test,
            predictions
        )


        f1 = f1_score(
            y_test,
            predictions
        )


        auc = roc_auc_score(
            y_test,
            probabilities
        )



        print(
            "Accuracy:",
            round(accuracy,4)
        )

        print(
            "F1:",
            round(f1,4)
        )

        print(
            "ROC-AUC:",
            round(auc,4)
        )



        results.append({

            "Date":
            datetime.now(),

            **params,

            "Accuracy":
            accuracy,

            "F1":
            f1,

            "ROC_AUC":
            auc

        })



        if auc > best_auc:

            best_auc = auc

            best_model = model



    results_df = pd.DataFrame(
        results
    )


    results_df = results_df.sort_values(
        "ROC_AUC",
        ascending=False
    )


    os.makedirs(
        MODEL_DIR,
        exist_ok=True
    )


    results_df.to_csv(
        RESULTS_FILE,
        index=False
    )


    joblib.dump(
        best_model,
        BEST_MODEL_FILE
    )


    print(
        "\n========== BEST MODEL =========="
    )


    print(
        results_df.head(1)
    )


    print(
        "\nSaved:"
    )


    print(
        BEST_MODEL_FILE
    )


    print(
        RESULTS_FILE
    )



if __name__ == "__main__":

    optimize()