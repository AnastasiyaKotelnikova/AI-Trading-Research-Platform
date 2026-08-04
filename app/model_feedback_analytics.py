import pandas as pd
import os


TRADE_DB = "data/trade_database.csv"
PREDICTION_DB = "data/models/model_predictions.csv"

OUTPUT = "data/models/model_feedback_analytics.csv"



def analyze_group(df, group_col, category, return_col):

    results = []

    if group_col not in df.columns:
        return results


    for name, group in df.groupby(group_col):


        # Ignore small samples
        if len(group) < 10:
            continue


        results.append({

            "Category": category,

            "Name": name,

            "Trades": len(group),

            "Average_Return":
                round(
                    group[return_col].mean(),
                    3
                ),

            "Win_Rate":
                round(
                    (group[return_col] > 0).mean() * 100,
                    2
                )

        })


    return results




def analyze_feedback():


    print(
        "\n========== MODEL FEEDBACK ANALYTICS ==========\n"
    )


    reports=[]



    # ======================================
    # STRATEGY ENGINE PERFORMANCE
    # ======================================


    if os.path.exists(TRADE_DB):


        trades = pd.read_csv(
            TRADE_DB,
            low_memory=False
        )


        completed = trades[
            trades["Return_%"].notna()
        ].copy()



        print(
            "Completed Strategy Trades:",
            len(completed)
        )



        reports += analyze_group(
            completed,
            "Strategy",
            "STRATEGY",
            "Return_%"
        )


        reports += analyze_group(
            completed,
            "Model_Name",
            "MODEL",
            "Return_%"
        )




    # ======================================
    # ML PREDICTION PERFORMANCE
    # ======================================


    if os.path.exists(PREDICTION_DB):


        pred = pd.read_csv(
            PREDICTION_DB,
            low_memory=False
        )



        completed = pred[
            pred["Prediction_Result"].isin(
                [
                    "SUCCESS",
                    "FAILED", 
                    "NEUTRAL"
                ]
            )
        ].copy()



        print(
            "Completed ML Predictions:",
            len(completed)
        )



        # ------------------------------
        # Overall ML Accuracy
        # ------------------------------


        accuracy = (

            (
                completed["Prediction_Result"]
                ==
                "SUCCESS"
            )
            .mean()
            *
            100

        )


        reports.append({

            "Category":
                "ML_MODEL",

            "Name":
                "Overall Accuracy",

            "Trades":
                len(completed),

            "Average_Return":
                round(
                    completed["Return_5D"].mean(),
                    3
                ),

            "Win_Rate":
                round(
                    accuracy,
                    2
                )

        })



        # ------------------------------
        # Model Performance
        # ------------------------------


        reports += analyze_group(
            completed,
            "Model",
            "ML_MODEL",
            "Return_5D"
        )



        # ------------------------------
        # AI Rating Performance
        # ------------------------------


        reports += analyze_group(
            completed,
            "AI_Rating",
            "AI_RATING",
            "Return_5D"
        )



        # ------------------------------
        # ML Probability Buckets
        # ------------------------------


        completed["ML_Bucket"] = pd.cut(

            completed["ML_Probability"],

            bins=[

                0,
                10,
                20,
                30,
                50,
                100

            ],

            labels=[

                "0-10",
                "10-20",
                "20-30",
                "30-50",
                "50+"

            ]

        )



        reports += analyze_group(
            completed,
            "ML_Bucket",
            "ML_PROBABILITY",
            "Return_5D"
        )



        # ------------------------------
        # AI Final Score Buckets
        # ------------------------------


        if "AI_Final_Score" in completed.columns:


            completed["AI_Bucket"] = pd.cut(

                completed["AI_Final_Score"],

                bins=[

                    0,
                    40,
                    60,
                    80,
                    100

                ],

                labels=[

                    "<40",
                    "40-60",
                    "60-80",
                    "80-100"

                ]

            )


            reports += analyze_group(
                completed,
                "AI_Bucket",
                "AI_SCORE",
                "Return_5D"
            )



    # ======================================
    # SAVE RESULTS
    # ======================================


    if reports:


        final = pd.DataFrame(
            reports
        )


        final.to_csv(
            OUTPUT,
            index=False
        )


        print(
            "\nSaved:"
        )

        print(
            OUTPUT
        )


        print(
            "\n"
        )

        print(
            final.to_string(
                index=False
            )
        )


    else:

        print(
            "No analytics generated"
        )




if __name__=="__main__":

    analyze_feedback()