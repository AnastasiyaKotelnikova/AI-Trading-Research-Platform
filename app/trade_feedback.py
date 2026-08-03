import pandas as pd
import os


TRADE_HISTORY_FILE = "data/trade_history.csv"

FEEDBACK_FILE = "data/trade_feedback.csv"



# =====================================================
# Generate AI Feedback Dataset
# =====================================================

def generate_feedback():


    print()

    print("=" * 60)
    print("AI TRADE FEEDBACK ENGINE")
    print("=" * 60)



    if not os.path.exists(
        TRADE_HISTORY_FILE
    ):

        print(
            "No trade history found."
        )

        return



    df = pd.read_csv(
        TRADE_HISTORY_FILE
    )



    completed = df[
        df["Status"] != "OPEN"
    ]



    if len(completed) == 0:


        print()

        print(
            "No completed trades available."
        )

        return




    feedback = []



    for _, trade in completed.iterrows():


        return_pct = float(
            trade.get(
                "Return_%",
                0
            )
        )



        record = {


            "Symbol":
                trade["Symbol"],


            "Strategy":
                trade.get(
                    "Strategy",
                    ""
                ),


            "AI_Decision":
                trade.get(
                    "AI_Decision",
                    ""
                ),


            "Final_Conviction_Score":
                trade.get(
                    "Final_Conviction_Score",
                    0
                ),


            "Expected_Value":
                trade.get(
                    "Expected_Value",
                    0
                ),


            "Return_%":
                return_pct,


            "AI_Correct":
                1
                if return_pct > 0
                else 0,


            "Outcome":
                trade.get(
                    "Outcome",
                    ""
                )

        }


        feedback.append(
            record
        )



    feedback_df = pd.DataFrame(
        feedback
    )


    feedback_df.to_csv(
        FEEDBACK_FILE,
        index=False
    )



    print()

    print(
        "Feedback records created:",
        len(feedback_df)
    )


    print()

    print(
        "Saved:",
        FEEDBACK_FILE
    )



    print()

    print(
        feedback_df
    )



# =====================================================
# Run
# =====================================================

if __name__ == "__main__":

    generate_feedback()