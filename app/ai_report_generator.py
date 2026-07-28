import os
from datetime import datetime


REPORT_FOLDER = "data/reports"


def generate_ai_report(df):

    os.makedirs(REPORT_FOLDER, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")

    report_file = (
        f"{REPORT_FOLDER}/AI_Report_{timestamp}.txt"
    )


    with open(report_file, "w", encoding="utf-8") as f:

        f.write("=" * 60 + "\n")
        f.write("AI STOCK ANALYSIS REPORT\n")
        f.write("=" * 60 + "\n\n")

        f.write(
            f"Generated: {datetime.now()}\n\n"
        )


        for _, row in df.iterrows():

            f.write("\n")
            f.write("=" * 60 + "\n")

            f.write(
                f"{row['Symbol']} AI RESEARCH REPORT\n"
            )

            f.write("=" * 60 + "\n\n")


            # Overview

            f.write("AI Evaluation\n")
            f.write("-" * 30 + "\n")

            f.write(
                f"AI Score: "
                f"{row.get('AI_Final_Score',0)} / 100\n"
            )

            f.write(
                f"Rating: "
                f"{row.get('AI_Rating','N/A')}\n"
            )


            f.write(
                f"Confidence: "
                f"{row.get('AI_Confidence_Level','N/A')}\n"
            )


            f.write(
                f"Combined ML Probability: "
                f"{row.get('Combined_ML_Probability',0)}%\n\n"
            )


            # Market

            f.write("Market Conditions\n")
            f.write("-" * 30 + "\n")

            f.write(
                f"Regime: "
                f"{row.get('Market_Regime','N/A')}\n\n"
            )


            # Thesis

            f.write("AI Summary\n")
            f.write("-" * 30 + "\n")

            f.write(
                f"{row.get('AI_Summary','No summary')}\n\n"
            )


            # Trade Setup

            f.write("Trade Setup\n")
            f.write("-" * 30 + "\n")

            f.write(
                f"Entry: ${row.get('Entry',0):.2f}\n"
            )

            f.write(
                f"Stop Loss: ${row.get('Stop_Loss',0):.2f}\n"
            )

            f.write(
                f"Target 1: ${row.get('Target_1',0):.2f}\n"
            )

            f.write(
                f"Target 2: ${row.get('Target_2',0):.2f}\n"
            )

            f.write(
                f"Risk Reward: "
                f"{row.get('Risk_Reward',0)}\n\n"
            )


            # Strengths / Risks

            f.write("Strengths\n")
            f.write("-" * 30 + "\n")

            f.write(
                f"{row.get('Strengths','N/A')}\n\n"
            )


            f.write("Risks\n")
            f.write("-" * 30 + "\n")

            f.write(
                f"{row.get('Risks','N/A')}\n"
            )


            f.write("\n")


    print()
    print("AI Report Generated:")
    print(report_file)


    return report_file