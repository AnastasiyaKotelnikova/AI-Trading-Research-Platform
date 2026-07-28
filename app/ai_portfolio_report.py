import os
from datetime import datetime



REPORT_FOLDER = "data/reports"



def generate_portfolio_report(df, market_regime=None):


    os.makedirs(
        REPORT_FOLDER,
        exist_ok=True
    )


    report_file = os.path.join(
        REPORT_FOLDER,
        "daily_ai_portfolio_report.txt"
    )


    df = df.copy()


    top = df.head(5)



    lines = []


    lines.append(
        "===================================\n"
    )

    lines.append(
        "AI PORTFOLIO SUMMARY\n"
    )

    lines.append(
        "===================================\n\n"
    )


    lines.append(
        f"Generated: {datetime.now()}\n\n"
    )



    # -----------------------------
    # Market Environment
    # -----------------------------

    lines.append(
        "MARKET ENVIRONMENT\n"
    )

    lines.append(
        "-----------------------------------\n"
    )


    if market_regime:

        lines.append(
            f"Regime: {market_regime}\n\n"
        )

    else:

        lines.append(
            "Regime: Unknown\n\n"
        )



    # -----------------------------
    # Top Candidates
    # -----------------------------


    lines.append(
        "TOP AI CANDIDATES\n"
    )

    lines.append(
        "-----------------------------------\n\n"
    )



    rank = 1


    for _, row in top.iterrows():


        lines.append(
            f"{rank}. {row['Symbol']}\n"
        )


        lines.append(
            f"Portfolio Score: {row.get('Portfolio_Score',0)}\n"
        )


        lines.append(
            f"Category: {row.get('Portfolio_Category','N/A')}\n"
        )


        lines.append(
            f"AI Decision: {row.get('AI_Decision','N/A')}\n"
        )


        lines.append(
            f"AI Confidence: {row.get('AI_Confidence',0)}%\n"
        )


        lines.append(
            f"ML Probability: {row.get('ML_Probability',0)}%\n"
        )


        lines.append(
            f"Historical ML: {row.get('Historical_ML_Probability',0)}%\n"
        )


        lines.append(
            f"Risk/Reward: {row.get('Risk_Reward',0)}\n\n"
        )


        rank += 1



    # -----------------------------
    # Risk Summary
    # -----------------------------


    lines.append(
        "RISK SUMMARY\n"
    )

    lines.append(
        "-----------------------------------\n"
    )


    if market_regime == "Bearish":


        lines.append(
            "Market weakness detected.\n"
        )


        lines.append(
            "Recommended action: Reduce exposure and wait for confirmation.\n"
        )


    elif market_regime == "Bullish":


        lines.append(
            "Market conditions supportive.\n"
        )


        lines.append(
            "Recommended action: Normal position sizing.\n"
        )


    else:


        lines.append(
            "Neutral conditions.\n"
        )



    with open(
        report_file,
        "w",
        encoding="utf-8"
    ) as f:

        f.writelines(lines)



    print(
        "\nAI Portfolio Report Saved:"
    )

    print(
        report_file
    )


    return report_file