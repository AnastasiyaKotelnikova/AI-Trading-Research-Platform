import pandas as pd
import os
import json
import datetime
from app.trade_management import add_trade_management


from app.ml_predictor import (
    add_ml_predictions,
    add_historical_ml_predictions
)
from app.ai_ranker import add_ai_score



FEATURE_FOLDER = "data/feature_history"

INPUT_FILE = (
    "data/results/quality_results.csv"
)

OUTPUT_FILE = (
    "data/analysis/ai_ranked_signals.csv"
)

STATUS_FILE = (
    "data/pipeline_status.json"
)



# --------------------------------------------------
# Update pipeline status
# --------------------------------------------------

def update_status(step, status, details=None):

    os.makedirs(
        "data",
        exist_ok=True
    )


    if os.path.exists(STATUS_FILE):

        with open(
            STATUS_FILE,
            "r"
        ) as f:

            pipeline = json.load(f)

    else:

        pipeline = {}



    pipeline[step] = {

        "status": status,

        "timestamp":
            str(datetime.datetime.now()),

        "details": details

    }



    with open(
        STATUS_FILE,
        "w"
    ) as f:

        json.dump(
            pipeline,
            f,
            indent=4
        )




# --------------------------------------------------
# Load latest feature data
# --------------------------------------------------

def load_latest_features(symbols):


    feature_list = []


    for symbol in symbols:


        file_path = os.path.join(

            FEATURE_FOLDER,

            f"{symbol}_features.csv"

        )


        if os.path.exists(file_path):


            temp = pd.read_csv(
                file_path
            )


            temp = temp.tail(1)


            temp["Symbol"] = symbol


            feature_list.append(
                temp
            )



    if not feature_list:

        raise ValueError(
            "No feature files found for symbols"
        )



    features = pd.concat(

        feature_list,

        ignore_index=True

    )



    if "Dollar_Volume" not in features.columns:


        if (

            "Volume" in features.columns

            and

            "Close" in features.columns

        ):


            features["Dollar_Volume"] = (

                features["Volume"]

                *

                features["Close"]

            )



    return features





# --------------------------------------------------
# Generate AI ranked signals
# --------------------------------------------------

def generate_ai_signals():


    update_status(
        "ai_signal_engine",
        "RUNNING"
    )


    try:


        df = pd.read_csv(
            INPUT_FILE
        )


        print(
            "\nLoading filtered scanner signals:"
        )

        print(
            len(df)
        )



        if "Strategy" not in df.columns:

            df["Strategy"] = (
                "QUALITY SETUP"
            )



        if "Confidence_Score" not in df.columns:

            df["Confidence_Score"] = 70




        features = load_latest_features(

            df["Symbol"].tolist()

        )



        df = df.merge(

            features,

            on="Symbol",

            how="left",

            suffixes=(
                "",
                "_feature"
            )

        )




        for col in [

            "Return_5D",

            "Return_20D",

            "RSI",

            "Above_SMA20",

            "Above_SMA50"

        ]:


            feature_col = (
                col +
                "_feature"
            )


            if feature_col in df.columns:


                df[col] = df[col].fillna(

                    df[feature_col]

                )


                df.drop(

                    columns=[
                        feature_col
                    ],

                    inplace=True

                )





        # ----------------------------------
        # Research Intelligence Score
        # ----------------------------------


        score_columns = [

            "Momentum_Score",

            "Trend_Score",

            "Volume_Score",

            "Relative_Strength_Score",

            "Setup_Score",

            "Risk_Reward_Score"

        ]



        for col in score_columns:


            if col not in df.columns:

                df[col] = 0




        df["Research_Score"] = (

            df["Momentum_Score"] * 1.2

            +

            df["Trend_Score"]

            +

            df["Volume_Score"] * 0.8

            +

            df["Relative_Strength_Score"]

            +

            df["Setup_Score"]

            +

            df["Risk_Reward_Score"]

        )



        max_score = (

            df["Research_Score"]
            .max()

        )



        if max_score > 0:


            df["Research_Score"] = (

                df["Research_Score"]

                /

                max_score

                *

                120

            )




        print(
            "\nAfter feature merge:"
        )

        print(
            df.shape
        )




        # ----------------------------------
        # ML prediction
        # ----------------------------------

        df = add_ml_predictions(
            df
        )

        
        df = add_historical_ml_predictions(
            df
        )


        # ----------------------------------
        # AI scoring
        # ----------------------------------

        df = add_ai_score(
            df
        )

        df = add_trade_management(
            df
        )


        df = df.sort_values(

            "AI_Final_Score",

            ascending=False

        )



        df.to_csv(

            OUTPUT_FILE,

            index=False

        )




        details = {

            "signals_processed":
                len(df),

            "output":
                OUTPUT_FILE,

            "top_symbol":
                df.iloc[0]["Symbol"]

        }



        update_status(

            "ai_signal_engine",

            "COMPLETED",

            details

        )



        print(
            "\nAI Ranking Complete"
        )

        print(
            OUTPUT_FILE
        )



        print(
            "\nTOP AI SIGNALS\n"
        )



        print(

            df[

                [

                    "Symbol",

                    "Strategy",

                    "Research_Score",

                    "Rank_Score",

                    "ML_Probability",

                    "AI_Final_Score"

                ]

            ]

            .head(20)

        )




    except Exception as e:


        update_status(

            "ai_signal_engine",

            "FAILED",

            str(e)

        )


        raise e





if __name__ == "__main__":


    generate_ai_signals()
