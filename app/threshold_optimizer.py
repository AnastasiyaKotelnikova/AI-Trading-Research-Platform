import pandas as pd
import numpy as np


def evaluate_thresholds(
        df,
        ai_conf,
        ml_prob,
        hist_ml,
        rank_score
):

    filtered = df[
        (df["AI_Confidence"] >= ai_conf) &
        (df["ML_Probability"] >= ml_prob) &
        (df["Historical_ML_Probability"] >= hist_ml) &
        (df["Rank_Score"] >= rank_score)
    ]


    if len(filtered) == 0:
        return None


    trades = len(filtered)


    avg_ai_score = (
        filtered["AI_Final_Score_Adjusted"]
        .mean()
    )


    avg_confidence = (
        filtered["AI_Confidence"]
        .mean()
    )


    avg_rank = (
        filtered["Rank_Score"]
        .mean()
    )


    # reward quality but avoid choosing only 1 stock
    trade_factor = min(trades / 10, 1)


    optimizer_score = (
        avg_ai_score * 0.5 +
        avg_confidence * 0.2 +
        avg_rank * 0.2 +
        trade_factor * 10
    )


    return {

        "AI_Confidence": ai_conf,
        "ML_Probability": ml_prob,
        "Historical_ML": hist_ml,
        "Rank_Score": rank_score,

        "Trades": trades,

        "Avg_AI_Score":
            round(avg_ai_score,2),

        "Avg_Confidence":
            round(avg_confidence,2),

        "Avg_Rank":
            round(avg_rank,2),

        "Optimizer_Score":
            round(optimizer_score,2)
    }



def optimize_thresholds(dataset):

    df = pd.read_csv(
        dataset,
        low_memory=False
    )


    results=[]


    for ai in np.arange(25,61,2.5):

        for ml in np.arange(10,61,2.5):

            for hist in np.arange(45,76,2.5):

                for rank in np.arange(20,91,2.5):


                    result = evaluate_thresholds(
                        df,
                        ai,
                        ml,
                        hist,
                        rank
                    )


                    if result:
                        results.append(result)



    results_df = pd.DataFrame(results)


    results_df = results_df.sort_values(
        "Optimizer_Score",
        ascending=False
    )


    return results_df



if __name__ == "__main__":


    results = optimize_thresholds(
        "data/results/quality_results.csv"
    )


    print(
        "\n===== OPTIMAL THRESHOLDS =====\n"
    )


    print(
        results.head(20)
        .to_string(index=False)
    )


    results.to_csv(
        "data/results/optimized_thresholds.csv",
        index=False
    )


    print(
        "\nSaved:"
        " data/results/optimized_thresholds.csv"
    )