import pandas as pd


# --------------------------------------------------
# Input file
# --------------------------------------------------

INPUT_FILE = "data/analysis/final_ai_signals.csv"



def generate_report():

    df = pd.read_csv(INPUT_FILE)


    print("\n")
    print("=" * 70)
    print("AI TRADING RESEARCH REPORT")
    print("=" * 70)



    # --------------------------------------------------
    # MODEL INFORMATION
    # --------------------------------------------------

    print("\nMODEL INFORMATION:")


    model_columns = [
        "Model_Name",
        "Model_Accuracy",
        "Model_F1",
        "Model_Status"
    ]


    found_model = False


    for col in model_columns:

        if col in df.columns:

            found_model = True

            print(
                f"{col}:",
                df[col].iloc[0]
            )


    if not found_model:

        print(
            "Model information unavailable"
        )



    # --------------------------------------------------
    # SIGNAL COUNT
    # --------------------------------------------------

    print("\nTOTAL SIGNALS:")

    print(
        len(df)
    )



    # --------------------------------------------------
    # AI STATUS SUMMARY
    # --------------------------------------------------

    if "Final_AI_Status" in df.columns:


        print(
            "\nFINAL AI STATUS DISTRIBUTION:\n"
        )


        print(
            df["Final_AI_Status"]
            .value_counts()
        )



    # --------------------------------------------------
    # RISK ENGINE SUMMARY
    # --------------------------------------------------

    if "Trade_Status" in df.columns:


        print(
            "\nRISK ENGINE STATUS:\n"
        )


        print(
            df["Trade_Status"]
            .value_counts()
        )



    # --------------------------------------------------
    # EXECUTION SUMMARY
    # --------------------------------------------------

    if "Trade_Execution_Status" in df.columns:


        print(
            "\nTRADE EXECUTION STATUS:\n"
        )


        print(
            df["Trade_Execution_Status"]
            .value_counts()
        )



    # --------------------------------------------------
    # TOP AI RANKING
    # --------------------------------------------------

    if "Final_Conviction_Score" in df.columns:


        print(
            "\nTOP AI CONVICTION RANKING:\n"
        )


        columns = [

            "Symbol",
            "AI_Decision",
            "Final_AI_Status",
            "Final_Conviction_Score",
            "Final_Conviction_Rating",
            "Trade_Grade",
            "Trade_Status",
            "Trade_Execution_Status",
            "Reward_Risk",
            "Expected_Value"

        ]


        available = [

            c for c in columns
            if c in df.columns

        ]


        print(

            df[
                available
            ]
            .sort_values(
                "Final_Conviction_Score",
                ascending=False
            )
            .head(25)

        )



    # --------------------------------------------------
    # APPROVED TRADE CANDIDATES
    # --------------------------------------------------

    if "Final_AI_Status" in df.columns:


        approved = df[

            df["Final_AI_Status"]
            ==
            "APPROVED TRADE"

        ]


        print(
            "\nAPPROVED TRADE CANDIDATES:\n"
        )


        if len(approved):

            cols = [

                "Symbol",
                "Final_Conviction_Score",
                "Expected_Value",
                "Trade_Grade",
                "Trade_Status",
                "Trade_Execution_Status",
                "Recommended_Shares"

            ]


            cols = [

                c for c in cols
                if c in approved.columns

            ]


            print(
                approved[cols]
            )


        else:

            print(
                "No approved trades"
            )



    # --------------------------------------------------
    # BEST AI CANDIDATE
    # --------------------------------------------------

    if "Final_Conviction_Score" in df.columns:


        print(
            "\nBEST AI CANDIDATE:\n"
        )


        best = (

            df
            .sort_values(
                "Final_Conviction_Score",
                ascending=False
            )
            .iloc[0]

        )


        fields = [

            "Symbol",
            "AI_Decision",
            "Final_AI_Status",
            "Final_Conviction_Score",
            "Expected_Value",
            "Reward_Risk",
            "Trade_Grade",
            "Trade_Status",
            "Trade_Execution_Status",
            "Recommended_Shares"

        ]


        for field in fields:

            if field in best.index:

                print(
                    f"{field}:",
                    best[field]
                )



    # --------------------------------------------------
    # AI DECISION DISTRIBUTION
    # --------------------------------------------------

    if "AI_Decision" in df.columns:


        print(
            "\nAI DECISION DISTRIBUTION:\n"
        )


        print(
            df["AI_Decision"]
            .value_counts()
        )



    # --------------------------------------------------
    # STRATEGY DISTRIBUTION
    # --------------------------------------------------

    if "Strategy" in df.columns:


        print(
            "\nSTRATEGY DISTRIBUTION:\n"
        )


        print(
            df["Strategy"]
            .value_counts()
        )



    # --------------------------------------------------
    # STRATEGY PERFORMANCE
    # --------------------------------------------------

    if (

        "Strategy" in df.columns

        and

        "Final_Conviction_Score" in df.columns

    ):


        print(
            "\nAVERAGE CONVICTION BY STRATEGY:\n"
        )


        print(

            df.groupby(
                "Strategy"
            )
            [
                "Final_Conviction_Score"
            ]
            .mean()
            .sort_values(
                ascending=False
            )

        )



    # --------------------------------------------------
    # COMPLETE
    # --------------------------------------------------

    print("\n")
    print("=" * 70)
    print("REPORT COMPLETE")
    print("=" * 70)




if __name__ == "__main__":

    generate_report()