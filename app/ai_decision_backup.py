import pandas as pd

from app.model_loader import get_best_model_info

INPUT_FILE = "data/analysis/ai_ranked_signals.csv"
OUTPUT_FILE = "data/analysis/final_ai_signals.csv"


def classify(score):

    if score >= 45:
        return "HIGH CONVICTION"

    elif score >= 35:
        return "STRONG CANDIDATE"

    elif score >= 25:
        return "WATCHLIST"

    else:
        return "PASS"


def run():

    df = pd.read_csv(INPUT_FILE)

    model_info = get_best_model_info()


    df["Model_Name"] = (
        model_info["Model"]
    )

    df["Model_F1"] = (
        model_info["F1"]
    )

    df["Model_Status"] = (
        model_info["Status"]
    )


    df["AI_Decision"] = (
        df["AI_Final_Score"]
        .apply(classify)
    )


    df = df.sort_values(
        "AI_Final_Score",
        ascending=False
    )


    df.to_csv(
        OUTPUT_FILE,
        index=False
    )


    print("\nAI Decision Engine Complete")

    print(
        OUTPUT_FILE
    )


    print("\nDecision Summary:\n")

    print(
        df["AI_Decision"]
        .value_counts()
    )


    print("\nTOP SIGNALS:\n")


    print(
        df[
            [
                "Symbol",
                "AI_Final_Score",
                "AI_Decision",
                "ML_Probability",
                "Model_Name",
                "Model_F1"
            ]
        ]
        .head(20)
    )



if __name__ == "__main__":

    run()
