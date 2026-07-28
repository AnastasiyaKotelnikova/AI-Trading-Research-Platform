import pandas as pd



def add_portfolio_selection(df):

    df = df.copy()


    # -----------------------------
    # Portfolio Priority Score
    # -----------------------------

    df["Portfolio_Score"] = (

        df["AI_Final_Score_Adjusted"] * 0.35

        +

        df["AI_Confidence"] * 0.25

        +

        df["ML_Probability"] * 0.20

        +

        df["Historical_ML_Probability"] * 0.10

        +

        (
            df["Risk_Reward"]
            .clip(0,5)
            /
            5
            *
            100
        )
        * 0.10

    ).round(2)



    # -----------------------------
    # Portfolio Category
    # -----------------------------

    def category(row):


        decision = row.get(
            "AI_Decision",
            ""
        )


        score = row.get(
            "Portfolio_Score",
            0
        )


        if (

            decision == "HIGH CONVICTION"

            and score >= 75

        ):

            return "TOP PICK"



        elif (

            decision == "STRONG CANDIDATE"

            and score >= 60

        ):

            return "PRIMARY WATCH"



        elif score >= 45:

            return "SECONDARY WATCH"



        else:

            return "MONITOR"



    df["Portfolio_Category"] = (

        df.apply(
            category,
            axis=1
        )

    )



    # -----------------------------
    # Rank Portfolio
    # -----------------------------

    df = df.sort_values(

        "Portfolio_Score",

        ascending=False

    )



    # -----------------------------
    # Select top candidates
    # -----------------------------

    df["Portfolio_Rank"] = (

        range(
            1,
            len(df)+1
        )

    )


    return df