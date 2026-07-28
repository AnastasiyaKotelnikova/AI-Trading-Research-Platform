"""
Train ML model for trading signal prediction
"""

import pandas as pd
import os
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score


DATA_FILE = "data/ml_training_dataset.csv"

MODEL_FILE = "data/models/trading_model.pkl"


def train_model():

    print("\n========== ML MODEL TRAINING ==========\n")


    df = pd.read_csv(DATA_FILE)


    print("Records:")
    print(len(df))


    features = [

        "Rank_Score",
        "Momentum_Score",
        "Trend_Score",
        "Relative_Strength",
        "Risk_Reward",
        "RSI",
        "Return_5D",
        "Return_20D",
        "Distance_From_High_%",
        "Above_SMA20",
        "Above_SMA50",
        "Breakout",
        "Overextended",
        "Confidence_Score",
        "Research_Score"

    ]


    X = df[features]

    y = df["Successful_Trade"]


    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.25,
        random_state=42,
        stratify=y
    )


    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=6,
        random_state=42,
        class_weight="balanced"
    )


    print("\nTraining model...")


    model.fit(
        X_train,
        y_train
    )


    predictions = model.predict(
        X_test
    )


    accuracy = accuracy_score(
        y_test,
        predictions
    )


    print("\nAccuracy:")
    print(
        round(accuracy,3)
    )


    print("\nClassification Report:")
    print(
        classification_report(
            y_test,
            predictions
        )
    )


    os.makedirs(
        "data/models",
        exist_ok=True
    )


    joblib.dump(
        model,
        MODEL_FILE
    )


    print("\nModel saved:")
    print(MODEL_FILE)



if __name__ == "__main__":

    train_model()
