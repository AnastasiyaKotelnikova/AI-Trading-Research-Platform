import pandas as pd
import os


FEEDBACK_FILE = "data/trade_feedback.csv"



# =====================================================
# Load Feedback
# =====================================================

def load_feedback():

    if not os.path.exists(
        FEEDBACK_FILE
    ):

        print()

        print(
            "No trade feedback dataset found."
        )

        print(
            "Complete trades are required before AI learning."
        )

        return None


    return pd.read_csv(
        FEEDBACK_FILE
    )



# =====================================================
# AI Learning Analysis
# =====================================================

def analyze_learning():


    print()

    print("=" * 60)
    print("AI LEARNING ENGINE")
    print("=" * 60)



    df = load_feedback()


    if df is None:

        return


    if len(df) == 0:

        print(
            "No feedback records."
        )

        return


    print()

    print(
        "Feedback Records:",
        len(df)
    )



    # -------------------------------------------------
    # Overall AI Accuracy
    # -------------------------------------------------

    accuracy = (

        df["AI_Correct"]
        .mean()

        *

        100

    )


    print()

    print(
        "AI Accuracy:",
        round(
            accuracy,
            2
        ),
        "%"
    )



    # -------------------------------------------------
    # Decision Reliability
    # -------------------------------------------------

    if "AI_Decision" in df.columns:


        print()

        print(
            "AI Decision Reliability:"
        )


        decision = (

            df.groupby(
                "AI_Decision"
            )
            [
                "AI_Correct"
            ]
            .agg(
                [
                    "count",
                    "mean"
                ]
            )

        )


        decision["mean"] = (

            decision["mean"]

            *

            100

        )


        decision.rename(
            columns={
                "mean":
                "Accuracy_%"
            },
            inplace=True
        )


        print(decision)




    # -------------------------------------------------
    # Strategy Performance
    # -------------------------------------------------

    if "Strategy" in df.columns:


        print()

        print(
            "Strategy Performance:"
        )


        print(

            df.groupby(
                "Strategy"
            )
            [
                "Return_%"
            ]
            .mean()
            .sort_values(
                ascending=False
            )

        )




    # -------------------------------------------------
    # Conviction Analysis
    # -------------------------------------------------

    if "Final_Conviction_Score" in df.columns:


        print()

        print(
            "Average Conviction Score:"
        )


        print(

            df[
                "Final_Conviction_Score"
            ]
            .mean()

        )




    print()

    print("=" * 60)

    print(
        "LEARNING ANALYSIS COMPLETE"
    )

    print("=" * 60)




# =====================================================
# Run
# =====================================================

if __name__ == "__main__":

    analyze_learning()