import pandas as pd
import os


from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report
)


from app.model_tracker import save_model_metrics

from app.model_manager import save_versioned_model



DATA_FILE = (
    "data/ml_training_dataset.csv"
)


MODEL_FOLDER = (
    "data/models"
)




FEATURES = [

    "RSI",

    "Return_5D",

    "Return_20D",

    "Distance_From_High_%",

    "Above_SMA20",

    "Above_SMA50",

    "Breakout",

    "Overextended",

    "Rank_Score",

    "Momentum_Score",

    "Trend_Score",

    "Relative_Strength",

    "Risk_Reward"

]




def train():


    df = pd.read_csv(
        DATA_FILE
    )


    print("\nDataset:")
    print(df.shape)



    X = df[FEATURES]

    y = df["Target"]




    # =========================
    # Time based split
    # =========================

    split_index = int(
        len(df) * 0.75
    )


    X_train = X.iloc[:split_index]

    X_test = X.iloc[split_index:]


    y_train = y.iloc[:split_index]

    y_test = y.iloc[split_index:]





    # =========================
    # Model
    # =========================


    model = RandomForestClassifier(

        n_estimators=300,

        max_depth=6,

        class_weight="balanced",

        random_state=42

    )



    model.fit(
        X_train,
        y_train
    )





    predictions = model.predict(
        X_test
    )





    # =========================
    # Metrics
    # =========================


    accuracy = accuracy_score(
        y_test,
        predictions
    )


    precision = precision_score(
        y_test,
        predictions,
        zero_division=0
    )


    recall = recall_score(
        y_test,
        predictions,
        zero_division=0
    )


    f1 = f1_score(
        y_test,
        predictions,
        zero_division=0
    )





    print("\nMODEL RESULTS")
    print("----------------")


    print(
        "Accuracy:",
        round(accuracy,3)
    )


    print(
        "Precision:",
        round(precision,3)
    )


    print(
        "Recall:",
        round(recall,3)
    )


    print(
        "F1:",
        round(f1,3)
    )



    print(
        classification_report(
            y_test,
            predictions,
            zero_division=0
        )
    )






    # =========================
    # Save Metrics History
    # =========================


    save_model_metrics(

        accuracy,

        precision,

        recall,

        f1,

        len(df)

    )







    # =========================
    # Feature Importance
    # =========================


    print("\nFEATURE IMPORTANCE")
    print("------------------")



    importance = pd.DataFrame(

        {

            "Feature": FEATURES,

            "Importance":
                model.feature_importances_

        }

    )



    importance = importance.sort_values(

        by="Importance",

        ascending=False

    )


    print(
        importance
    )






    # =========================
    # Save Versioned Model
    # =========================


    os.makedirs(

        MODEL_FOLDER,

        exist_ok=True

    )



    save_versioned_model(

        model,

        accuracy,

        precision,

        recall,

        f1,

        len(df)

    )



    print(
        "\nTraining complete."
    )



if __name__ == "__main__":

    train()
