import pandas as pd

TRADE_HISTORY_FILE = "data/trade_history.csv"


# =====================================================
# Load Trade History
# =====================================================

def load_trade_history():

    try:

        return pd.read_csv(
            TRADE_HISTORY_FILE
        )

    except FileNotFoundError:

        print("Trade history not found.")

        return pd.DataFrame()


# =====================================================
# Performance Summary
# =====================================================

def calculate_performance():

    df = load_trade_history()

    if df.empty:

        print("No historical trades.")

        return {}

    closed = df[
        df["Status"].isin(
            [
                "STOP HIT",
                "TARGET 1 HIT",
                "TARGET 2 HIT"
            ]
        )
    ].copy()

    if closed.empty:

        print("No completed trades.")

        return {}

    total = len(closed)

    wins = len(
        closed[
            closed["Outcome"] == "WIN"
        ]
    )

    losses = len(
        closed[
            closed["Outcome"] == "LOSS"
        ]
    )

    win_rate = round(
        wins / total * 100,
        2
    )

    avg_return = round(
        closed["Return_%"].mean(),
        2
    )

    avg_days = round(
        closed["Days_Held"].mean(),
        2
    )

    avg_profit = round(
        closed["Profit_$"].mean(),
        2
    )

    gross_profit = closed.loc[
        closed["Profit_$"] > 0,
        "Profit_$"
    ].sum()

    gross_loss = abs(
        closed.loc[
            closed["Profit_$"] < 0,
            "Profit_$"
        ].sum()
    )

    if gross_loss > 0:

        profit_factor = round(
            gross_profit / gross_loss,
            2
        )

    else:

        profit_factor = float("inf")

    expectancy = round(

        avg_return *
        (win_rate / 100),

        2

    )

    summary = {

        "Total Trades": total,

        "Wins": wins,

        "Losses": losses,

        "Win Rate": win_rate,

        "Average Return": avg_return,

        "Average Holding Days": avg_days,

        "Average Profit": avg_profit,

        "Gross Profit": round(
            gross_profit,
            2
        ),

        "Gross Loss": round(
            gross_loss,
            2
        ),

        "Profit Factor": profit_factor,

        "Expectancy": expectancy

    }

    return summary


# =====================================================
# Strategy Performance
# =====================================================

def strategy_performance():

    df = load_trade_history()

    if df.empty:

        return pd.DataFrame()

    closed = df[
        df["Status"].isin(
            [
                "STOP HIT",
                "TARGET 1 HIT",
                "TARGET 2 HIT"
            ]
        )
    ]

    if closed.empty:

        return pd.DataFrame()

    report = (

        closed
        .groupby("Strategy")
        .agg(

            Trades=("Strategy", "count"),

            Avg_Return=("Return_%", "mean"),

            Avg_Profit=("Profit_$", "mean"),

            Avg_Days=("Days_Held", "mean")

        )

        .round(2)

        .sort_values(
            "Avg_Return",
            ascending=False
        )

    )

    return report


# =====================================================
# AI Decision Performance
# =====================================================

def ai_decision_performance():

    df = load_trade_history()

    if df.empty:

        return pd.DataFrame()

    closed = df[
        df["Status"].isin(
            [
                "STOP HIT",
                "TARGET 1 HIT",
                "TARGET 2 HIT"
            ]
        )
    ]

    if closed.empty:

        return pd.DataFrame()

    report = (

        closed
        .groupby("AI_Decision")
        .agg(

            Trades=("AI_Decision", "count"),

            Avg_Return=("Return_%", "mean"),

            Win_Rate=("Outcome",
                      lambda x:
                      (x == "WIN").mean() * 100)

        )

        .round(2)

        .sort_values(
            "Avg_Return",
            ascending=False
        )

    )

    return report


# =====================================================
# Print Report
# =====================================================

def print_performance_report():

    summary = calculate_performance()

    if not summary:

        return

    print()
    print("=" * 60)
    print("TRADE PERFORMANCE")
    print("=" * 60)
    print()

    for key, value in summary.items():

        print(f"{key:<25} {value}")

    print()

    print("=" * 60)
    print("PERFORMANCE BY STRATEGY")
    print("=" * 60)

    print()

    print(strategy_performance())

    print()

    print("=" * 60)
    print("AI DECISION PERFORMANCE")
    print("=" * 60)

    print()

    print(ai_decision_performance())


# =====================================================
# Manual Test
# =====================================================

if __name__ == "__main__":

    print_performance_report()