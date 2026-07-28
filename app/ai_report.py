import pandas as pd


# --------------------------------------------------
# Input file
# Final AI decisions contain complete analysis
# --------------------------------------------------

INPUT_FILE = "data/analysis/final_ai_signals.csv"



def generate_report():

    df = pd.read_csv(INPUT_FILE)


    print("\n")
    print("=" * 60)
    print("AI TRADING RESEARCH REPORT")
    print("=" * 60)



    # --------------------------------------------------
    # MODEL INFORMATION
    # --------------------------------------------------

    print("\nMODEL INFORMATION:")


    if "Model_Name" in df.columns:

        print(
            "Active Model:",
            df["Model_Name"].iloc[0]
        )


        if "Model_Accuracy" in df.columns:

            print(
                "Model Accuracy:",
                df["Model_Accuracy"].iloc[0]
            )


        if "Model_F1" in df.columns:

            print(
                "Model F1:",
                df["Model_F1"].iloc[0]
            )


        if "Model_Status" in df.columns:

            print(
                "Model Status:",
                df["Model_Status"].iloc[0]
            )


    else:

        print(
            "Model information unavailable"
        )



    # --------------------------------------------------
    # TOTAL SIGNALS
    # --------------------------------------------------

    print("\nTOTAL SIGNALS:")

    print(
        len(df)
    )



    # --------------------------------------------------
    # FINAL AI CONVICTION RANKING
    # --------------------------------------------------

    if "Final_Conviction_Score" in df.columns:


        print(
            "\nTOP AI CONVICTION RANKING:\n"
        )


        conviction_columns = [

            "Symbol",
            "Strategy",
            "AI_Decision",
            "Final_Conviction_Score",
            "Final_Conviction_Rating",
            "Final_Action",
            "Trade_Grade",
            "Trade_Score",
            "Reward_Risk",
            "Expected_Value"

        ]


        available_columns = [

            col for col in conviction_columns
            if col in df.columns

        ]


        print(

            df[
                available_columns
            ]
            .sort_values(

                "Final_Conviction_Score",
                ascending=False

            )
            .head(25)

        )



    # --------------------------------------------------
    # TRADE MANAGEMENT RANKING
    # --------------------------------------------------

    if "Trade_Score" in df.columns:


        print(
            "\nTOP TRADE MANAGEMENT RANKING:\n"
        )


        trade_columns = [

            "Symbol",
            "AI_Decision",
            "Trade_Score",
            "Trade_Grade",
            "Reward_Risk",
            "Expected_Value",
            "Recommended_Shares",
            "Capital_Required"

        ]


        available_trade_columns = [

            col for col in trade_columns
            if col in df.columns

        ]


        print(

            df[
                available_trade_columns
            ]
            .sort_values(

                "Trade_Score",
                ascending=False

            )
            .head(25)

        )



    # --------------------------------------------------
    # BEST AI ANALYST PICK
    # --------------------------------------------------

    if "Final_Conviction_Score" in df.columns:


        print(
            "\nBEST CURRENT AI TRADE CANDIDATE:\n"
        )


        best_trade = (

            df
            .sort_values(
                "Final_Conviction_Score",
                ascending=False
            )
            .iloc[0]

        )


        print(
            "Symbol:",
            best_trade["Symbol"]
        )


        print(
            "AI Decision:",
            best_trade.get(
                "AI_Decision",
                "N/A"
            )
        )


        print(
            "Conviction Score:",
            best_trade.get(
                "Final_Conviction_Score",
                "N/A"
            )
        )


        print(
            "Conviction Rating:",
            best_trade.get(
                "Final_Conviction_Rating",
                "N/A"
            )
        )


        print(
            "Action:",
            best_trade.get(
                "Final_Action",
                "N/A"
            )
        )


        print(
            "Trade Grade:",
            best_trade.get(
                "Trade_Grade",
                "N/A"
            )
        )


        print(
            "Expected Value:",
            best_trade.get(
                "Expected_Value",
                "N/A"
            )
        )


        print(
            "Reward/Risk:",
            best_trade.get(
                "Reward_Risk",
                "N/A"
            )
        )


        print(
            "Recommended Shares:",
            best_trade.get(
                "Recommended_Shares",
                "N/A"
            )
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
    # FINAL ACTION DISTRIBUTION
    # --------------------------------------------------

    if "Final_Action" in df.columns:


        print(
            "\nFINAL AI ACTION DISTRIBUTION:\n"
        )


        print(

            df["Final_Action"]
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
    # AVERAGE CONVICTION BY STRATEGY
    # --------------------------------------------------

    if (

        "Strategy" in df.columns

        and

        "Final_Conviction_Score" in df.columns

    ):


        print(
            "\nAVERAGE CONVICTION SCORE BY STRATEGY:\n"
        )


        print(

            df.groupby("Strategy")
            ["Final_Conviction_Score"]
            .mean()
            .sort_values(
                ascending=False
            )

        )



    # --------------------------------------------------
    # REPORT COMPLETE
    # --------------------------------------------------

    print("\n")
    print("=" * 60)
    print("REPORT COMPLETE")
    print("=" * 60)




if __name__ == "__main__":

    generate_report()