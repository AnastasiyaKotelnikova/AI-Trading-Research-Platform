import pandas as pd
import os


INPUT = "data/analysis/strategy_results.csv"

OUTPUT = "data/analysis/research_ranked.csv"



def load_data():

    return pd.read_csv(INPUT)



def calculate_research_score(df):

    scores = []

    for _, row in df.iterrows():

        score = 0


        # Base quality
        score += row["Rank_Score"]


        # Strategy bonus
        if row["Strategy"] == "PULLBACK CONTINUATION":
            score += 15

        elif row["Strategy"] == "STRONG PULLBACK":
            score += 10

        elif row["Strategy"] == "QUALITY SETUP":
            score += 8

        elif row["Strategy"] == "MOMENTUM":
            score += 5

        else:
            score -= 10



        # Sector strength bonus

        if row["Sector"] == "Healthcare":
            score += 10

        elif row["Sector"] == "Financial Services":
            score += 5



        # Risk reward bonus

        if row["Risk_Reward"] >= 5:
            score += 8

        elif row["Risk_Reward"] >= 3:
            score += 5



        # RSI sweet spot

        if 50 <= row["RSI"] <= 58:
            score += 5


        scores.append(score)


    df["Research_Score"] = scores


    return df



def main():

    print("\n===== RESEARCH RANKER =====\n")


    df = load_data()


    df = calculate_research_score(df)


    result = (
        df.sort_values(
            "Research_Score",
            ascending=False
        )
        [
            [
                "Symbol",
                "Sector",
                "Strategy",
                "Research_Score",
                "Rank_Score",
                "RSI",
                "Risk_Reward",
                "Return_%"
            ]
        ]
        .head(25)
    )


    print(result)



    os.makedirs(
        "data/analysis",
        exist_ok=True
    )


    df.to_csv(
        OUTPUT,
        index=False
    )


    print("\nSaved:")
    print(OUTPUT)



if __name__ == "__main__":
    main()
