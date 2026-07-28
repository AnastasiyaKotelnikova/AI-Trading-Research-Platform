import pandas as pd
from pathlib import Path


INPUT_FILE = Path(
    "data/analysis/research_ranked.csv"
)


OUTPUT_FILE = Path(
    "data/analysis/confidence_scores.csv"
)


def calculate_confidence(row):

    score = 0


    # Risk Reward
    if row["Risk_Reward"] >= 5:
        score += 25
    elif row["Risk_Reward"] >= 3:
        score += 18
    else:
        score += 10


    # Trend
    if row["Above_SMA20"]:
        score += 10

    if row["Above_SMA50"]:
        score += 10


    # Momentum
    if row["Return_20D"] > 10:
        score += 15
    elif row["Return_20D"] > 0:
        score += 10


    # Sector strength
    if row["Sector"]:
        score += 10


    # Strategy quality
    if row["Strategy"] in [
        "STRONG PULLBACK",
        "QUALITY SETUP"
    ]:
        score += 15


    # Avoid overextended
    if not row["Overextended"]:
        score += 5


    return min(score,100)



def create_scores():

    df = pd.read_csv(
        INPUT_FILE
    )


    df["Confidence_Score"] = (
        df.apply(
            calculate_confidence,
            axis=1
        )
    )


    df = df.sort_values(
        "Confidence_Score",
        ascending=False
    )


    df.to_csv(
        OUTPUT_FILE,
        index=False
    )


    print(
        "Confidence scores created:"
    )

    print(
        OUTPUT_FILE
    )



if __name__ == "__main__":

    create_scores()
