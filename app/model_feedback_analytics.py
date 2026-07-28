import pandas as pd
import os


DATABASE_FILE = "data/trade_database.csv"

OUTPUT_FILE = (
    "data/models/model_feedback_analytics.csv"
)


def analyze_feedback():

    print("\n========== MODEL FEEDBACK ANALYTICS ==========\n")


    if not os.path.exists(DATABASE_FILE):

        print("Trade database not found")
        return


    df = pd.read_csv(
        DATABASE_FILE,
        low_memory=False
    )


    # ======================================
    # Completed Trades
    # ======================================

    if "Result" in df.columns:

        completed = df[
            ~df["Result"].isin(
                [
                    "OPEN",
                    "OPEN POSITION"
                ]
            )
        ].copy()

    else:

        completed = df[
            df["Return_%"].notna()
        ].copy()



    print("Completed Trades:")
    print(len(completed))


    if len(completed) == 0:

        print("No completed trades yet")
        return



    reports = []



    # ======================================
    # MODEL PERFORMANCE
    # ======================================

    if "Model_Name" in completed.columns:


        model_data = completed[
            completed["Model_Name"].notna()
        ].copy()


        if len(model_data) > 0:


            model_report = (

                model_data
                .groupby("Model_Name")
                ["Return_%"]
                .agg(
                    [
                        "count",
                        "mean",
                        lambda x:
                        (x > 0).mean()*100
                    ]
                )
            )


            model_report.columns = [

                "Trades",
                "Average_Return",
                "Win_Rate"

            ]


            model_report["Category"] = (
                "MODEL"
            )


            reports.append(
                model_report.reset_index()
            )



    # ======================================
    # AI SCORE PERFORMANCE
    # ======================================

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



        score_report = (

            completed
            .groupby(
                "AI_Bucket",
                observed=False
            )
            ["Return_%"]
            .agg(

                [
                    "count",
                    "mean",
                    lambda x:
                    (x > 0).mean()*100
                ]

            )

        )



        score_report.columns = [

            "Trades",
            "Average_Return",
            "Win_Rate"

        ]



        score_report["Category"] = (
            "AI_SCORE"
        )


        reports.append(
            score_report.reset_index()
        )



    # ======================================
    # STRATEGY PERFORMANCE
    # ======================================

    if "Strategy" in completed.columns:


        strategy_report = (

            completed
            .groupby("Strategy")
            ["Return_%"]
            .agg(

                [
                    "count",
                    "mean",
                    lambda x:
                    (x > 0).mean()*100
                ]

            )

        )



        strategy_report.columns = [

            "Trades",
            "Average_Return",
            "Win_Rate"

        ]



        strategy_report["Category"] = (
            "STRATEGY"
        )


        reports.append(
            strategy_report.reset_index()
        )



    # ======================================
    # MARKET REGIME PERFORMANCE
    # ======================================

    if (
        "Market_Regime" in completed.columns
        and completed["Market_Regime"].notna().sum() > 0
    ):


        regime_report = (

            completed
            .groupby("Market_Regime")
            ["Return_%"]
            .agg(

                [
                    "count",
                    "mean",
                    lambda x:
                    (x > 0).mean()*100
                ]

            )

        )


        regime_report.columns = [

            "Trades",
            "Average_Return",
            "Win_Rate"

        ]



        regime_report["Category"] = (
            "MARKET_REGIME"
        )


        reports.append(
            regime_report.reset_index()
        )



    # ======================================
    # AI DECISION PERFORMANCE
    # ======================================

    if "AI_Decision" in completed.columns:


        decision_report = (

            completed
            .groupby("AI_Decision")
            ["Return_%"]
            .agg(

                [
                    "count",
                    "mean",
                    lambda x:
                    (x > 0).mean()*100
                ]

            )

        )


        decision_report.columns = [

            "Trades",
            "Average_Return",
            "Win_Rate"

        ]


        decision_report["Category"] = (
            "AI_DECISION"
        )


        reports.append(
            decision_report.reset_index()
        )



    # ======================================
    # SAVE RESULTS
    # ======================================

    if reports:


        final = pd.concat(

            reports,

            ignore_index=True

        )


        final.to_csv(

            OUTPUT_FILE,

            index=False

        )


        print("\nFeedback analytics saved:")
        print(OUTPUT_FILE)


        print("\n")
        print(final)


    else:

        print(
            "No analytics generated"
        )



if __name__ == "__main__":

    analyze_feedback()
