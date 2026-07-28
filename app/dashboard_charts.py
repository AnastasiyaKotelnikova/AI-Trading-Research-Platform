from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


ANALYSIS_DIR = Path("data/analysis")
CHART_DIR = Path("data/charts")


def create_sector_chart():
    """Create sector performance chart."""

    df = pd.read_csv(
        ANALYSIS_DIR / "strategy_sector_results.csv"
    )

    sector_summary = (
        df.groupby("Sector")["Return_%"]
        .mean()
        .sort_values(ascending=False)
        .head(10)
    )

    plt.figure(figsize=(9, 5))

    sector_summary.plot(kind="bar")

    plt.title("Average Return by Sector")
    plt.xlabel("Sector")
    plt.ylabel("Average Return (%)")

    plt.xticks(rotation=30, ha="right")

    plt.tight_layout()

    plt.savefig(
        CHART_DIR / "sector_performance.png",
        dpi=150
    )

    plt.close()


def create_strategy_chart():
    """Create strategy distribution chart."""

    df = pd.read_csv(
        ANALYSIS_DIR / "research_ranked.csv"
    )

    strategy_counts = (
        df["Strategy"]
        .value_counts()
    )

    plt.figure(figsize=(8, 5))

    strategy_counts.plot(kind="bar")

    plt.title("Strategy Distribution")
    plt.xlabel("Strategy")
    plt.ylabel("Count")

    plt.xticks(rotation=20, ha="right")

    plt.tight_layout()

    plt.savefig(
        CHART_DIR / "strategy_distribution.png",
        dpi=150
    )

    plt.close()


def create_research_chart():
    """Create top research score chart."""

    df = pd.read_csv(
        ANALYSIS_DIR / "research_ranked.csv"
    )

    top = (
        df.sort_values(
            by="Research_Score",
            ascending=False
        )
        .head(10)
    )

    plt.figure(figsize=(10, 5))

    plt.bar(
        top["Symbol"],
        top["Research_Score"]
    )

    plt.title("Top AI Research Scores")
    plt.xlabel("Symbol")
    plt.ylabel("Research Score")

    plt.tight_layout()

    plt.savefig(
        CHART_DIR / "research_scores.png",
        dpi=150
    )

    plt.close()


def main():

    CHART_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    create_sector_chart()
    create_strategy_chart()
    create_research_chart()

    print("Dashboard charts created successfully.")
    print(CHART_DIR)


if __name__ == "__main__":
    main()
