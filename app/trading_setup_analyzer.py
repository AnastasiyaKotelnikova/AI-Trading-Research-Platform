import os
import pandas as pd


OUTCOME_FILE = (
    "data/models/trading_outcomes.csv"
)

OUTPUT_FILE = (
    "data/models/trading_setup_analysis.csv"
)



def analyze():

    print()
    print("=" * 50)
    print("TRADING SETUP ANALYZER")
    print("=" * 50)



    if not os.path.exists(OUTCOME_FILE):

        print(
            "Trading outcome file not found"
        )

        return



    df = pd.read_csv(
        OUTCOME_FILE
    )



    print()
    print(
        "Trades analyzed:",
        len(df)
    )



    if len(df) == 0:

        print(
            "No trades available"
        )

        return



    results = []



    # -------------------------
    # Analyze AI Score
    # -------------------------

    if "AI_Final_Score" in df.columns:


        groups = pd.cut(
            df["AI_Final_Score"],
            bins=[
                0,
                30,
                45,
                60,
                100
            ]
        )


        for category, group in df.groupby(
            groups,
            observed=True
        ):


            if len(group) < 5:
                continue



            wins = len(
                group[
                    group["Return_5D"] > 0
                ]
            )



            results.append({

                "Category_Type":
                    "AI_SCORE",


                "Category":
                    str(category),


                "Trades":
                    len(group),


                "Win_Rate":
                    round(
                        wins /
                        len(group)
                        *
                        100,
                        2
                    ),


                "Average_Return":
                    round(
                        group["Return_5D"]
                        .mean(),
                        2
                    )

            })



    # -------------------------
    # Analyze ML Probability
    # -------------------------

    if "ML_Probability" in df.columns:


        groups = pd.cut(
            df["ML_Probability"],
            bins=[
                0,
                10,
                25,
                50,
                75,
                100
            ]
        )


        for category, group in df.groupby(
            groups,
            observed=True
        ):


            if len(group) < 5:
                continue



            wins = len(
                group[
                    group["Trade_Outcome"]
                    !=
                    "STOP_HIT"
                ]
            )


            results.append({

                "Category_Type":
                    "ML_PROBABILITY",


                "Category":
                    str(category),


                "Trades":
                    len(group),


                "Win_Rate":
                    round(
                        wins /
                        len(group)
                        *
                        100,
                        2
                    ),


                "Average_Return":
                    round(
                        group["Return_5D"]
                        .mean(),
                        2
                    )

            })



    # -------------------------
    # Market Regime
    # -------------------------

    if "Market_Regime" in df.columns:


        for category, group in df.groupby(
            "Market_Regime"
        ):


            if len(group) < 5:
                continue



            wins = len(
                group[
                    group["Trade_Outcome"]
                    !=
                    "STOP_HIT"
                ]
            )


            results.append({

                "Category_Type":
                    "MARKET_REGIME",


                "Category":
                    category,


                "Trades":
                    len(group),


                "Win_Rate":
                    round(
                        wins /
                        len(group)
                        *
                        100,
                        2
                    ),


                "Average_Return":
                    round(
                        group["Return_5D"]
                        .mean(),
                        2
                    )

            })



    report = pd.DataFrame(results)



    report = report.sort_values(
        [
            "Win_Rate",
            "Average_Return"
        ],
        ascending=False
    )



    os.makedirs(
        "data/models",
        exist_ok=True
    )


    report.to_csv(
        OUTPUT_FILE,
        index=False
    )



    print()

    print(
        "Learning report saved:"
    )

    print(
        OUTPUT_FILE
    )


    print()

    print(
        report.head(20)
    )



if __name__ == "__main__":

    analyze()