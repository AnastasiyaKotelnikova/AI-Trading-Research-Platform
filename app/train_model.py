import pandas as pd
import os
import joblib
from datetime import datetime

from app.model_registry import evaluate_new_model 

from sklearn.pipeline import Pipeline

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix,
     roc_auc_score
)

from app.ml_backtest import run_ml_backtest



DATA_FILE = "data/historical_ml_dataset.csv"

MODEL_FOLDER = "data/models"


# Reserved for future explicit feature selection.
# Currently all features are selected using df.drop(...).
FEATURE_COLUMNS = [
    
    "Volume",

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

    "Volume_Trend",
]


def evaluate_model(name, model, X_test, y_test):


    prediction = model.predict(X_test)

    auc = 0

    probability = None

    if hasattr(model, "predict_proba"):

        probability = model.predict_proba(X_test)[:,1]

        if probability is not None:

            auc = roc_auc_score(
                y_test,
                probability
            )

            print(
                "\nROC-AUC:",
                round(auc,3)
            )

    accuracy = accuracy_score(
        y_test,
        prediction
    )

    precision = precision_score(
        y_test,
        prediction,
        zero_division=0
    )

    recall = recall_score(
        y_test,
        prediction,
        zero_division=0
    )

    f1 = f1_score(
        y_test,
        prediction,
        zero_division=0
    )


    print("\n======", name, "======")

    print("Accuracy:", round(accuracy,3))
    print("Precision:", round(precision,3))
    print("Recall:", round(recall,3))
    print("F1:", round(f1,3))


    print("\n===== CONFUSION MATRIX =====")

    cm = confusion_matrix(
        y_test,
        prediction
    )

    print(cm)


    print("\n===== CLASSIFICATION REPORT =====")

    print(
        classification_report(
            y_test,
            prediction,
            target_names=[
                "Failed Trade",
                "Successful Trade"
            ],
            zero_division=0
        )
    )

    if probability is not None:

        print("\n===== MODEL PROBABILITY =====")

        print(
            "Average Success Probability:",
            round(probability.mean(),3)
        )


        results = pd.DataFrame({

            "Actual": y_test.values,

            "Prediction": prediction,

            "Success_Probability": probability

        })


        results.to_csv(

            "data/models/test_predictions.csv",

            index=False

        )

        
        print(
            "Highest Probability:",
            round(probability.max(),3)
        )

        print(
            "Lowest Probability:",
            round(probability.min(),3)
        )


    return accuracy, precision, recall, f1, auc



def train():

    df = pd.read_csv(
        DATA_FILE
    )


        # Sort by date to avoid future data leakage

    df["Date"] = pd.to_datetime(
        df["Date"]
    )


    df = df.sort_values(
        "Date"
    )


    train_df = df[
        df["Date"] < "2026-05-15"
    ]


    test_df = df[
        df["Date"] >= "2026-05-15"
    ]


    X_train = train_df[FEATURE_COLUMNS]

    y_train = train_df[
        "Successful_Trade"
    ]


    X_test = test_df[FEATURE_COLUMNS]

    y_test = test_df[
        "Successful_Trade"
    ]


    print("\nTraining samples:", len(X_train))

    print("Testing samples:", len(X_test))

    if len(X_train) == 0 or len(X_test) == 0:
        raise ValueError(
            "Train/test split created an empty dataset. Check dates."
        )

    models = {


        "Logistic Regression":

        LogisticRegression(
            max_iter=1000,
            class_weight="balanced"
        ),


        "Random Forest":

        RandomForestClassifier(

            n_estimators=100,

            max_depth=15,

            min_samples_leaf=10,

            max_features="sqrt",

            class_weight="balanced",

            random_state=42,

            n_jobs=-1

        )

    }



    best_model = None

    best_score = 0

    best_accuracy = 0

    best_precision = 0

    best_recall = 0

    best_auc = 0



    for name, algorithm in models.items():

        print("\nStarting:", name)


        if name == "Logistic Regression":

            pipeline = Pipeline(
                steps=[
                    ("scaler", StandardScaler()),
                    ("model", algorithm)
                ]
            )

        else:

            pipeline = Pipeline(
                steps=[
                    ("model", algorithm)
                ]
            )


        pipeline.fit(
            X_train,
            y_train
        )


        accuracy, precision, recall, f1, auc = evaluate_model(
            name,
            pipeline,
            X_test,
            y_test
        )

        if name == "Random Forest":

            importances = (
                pipeline.named_steps["model"]
                .feature_importances_
            )


            feature_importance = pd.DataFrame({

                "Feature": FEATURE_COLUMNS,

                "Importance": importances

            })


            feature_importance["Importance_%"] = (

                feature_importance["Importance"] * 100

            ).round(2)


            feature_importance = feature_importance.sort_values(
                "Importance",
                ascending=False
            )


            feature_importance.to_csv(
                "data/models/feature_importance.csv",
                index=False
            )


            print("\n===== TOP 15 FEATURES =====\n")

            print(
                feature_importance.head(15)
                .to_string(index=False)
            )

        if f1 > best_score:

            best_score = f1

            best_accuracy = accuracy

            best_model = pipeline

            best_precision = precision

            best_recall = recall

            best_auc = auc



    os.makedirs(
        MODEL_FOLDER,
        exist_ok=True
    )


    existing_models = [

        f for f in os.listdir(MODEL_FOLDER)

        if f.startswith("model_v")
        and f.endswith(".pkl")

    ]


    if existing_models:

        versions = [

            int(
                f.replace(
                    "model_v",
                    ""
                )
                .replace(
                    ".pkl",
                    ""
                )
            )

            for f in existing_models

        ]

        next_version = max(versions)+1

    else:

        next_version = 1



    model_name = f"model_v{next_version}"


    model_path = (

        MODEL_FOLDER

        +

        f"/{model_name}.pkl"

    )


    joblib.dump(
        best_model,
        model_path
    )


    print("\nModel Saved:")
    print(model_path)



    champion_path = (

        MODEL_FOLDER

        +

        "/champion_model.pkl"

    )


    backtest_results = run_ml_backtest()


    if backtest_results:

        average_return = (
            backtest_results["Average_Return"]
        )

        win_rate = (
            backtest_results["Win_Rate"]
        )

    else:

        average_return = None

        win_rate = None



    accepted = evaluate_new_model(
        model_name,
        best_score,
        average_return,
        win_rate,
        best_auc
    )


    if accepted:


        joblib.dump(
            best_model,
            champion_path
        )


        status = "Champion"


        print("\nChampion Model Updated:")
        print(champion_path)


    else:


        status = "Rejected"


        print("\nChampion Model Kept")



    metrics_file = (

        MODEL_FOLDER

        +

        "/model_metrics.csv"

    )


    metrics = pd.DataFrame(

        [

            {

                "Date":
                    datetime.now(),

                "Model":
                    model_name,

                "Accuracy":
                    best_accuracy,

                "F1":
                    best_score,

                "Precision":
                    best_precision,

                "Recall":
                    best_recall,

                "ROC_AUC":
                    best_auc,

                "Training_Records":
                    len(X_train),

                "Average_Return":
                    average_return,

                "Win_Rate":
                    win_rate,

                "Status":
                    status

            }

        ]

    )



    if os.path.exists(metrics_file):

        old_metrics = pd.read_csv(
            metrics_file
        )

        metrics = pd.concat(
            [
                old_metrics,
                metrics
            ],
            ignore_index=True
        )



    metrics.to_csv(
        metrics_file,
        index=False
    )


    print("\nMetrics Saved:")
    print(metrics_file)



if __name__ == "__main__":

    train()
