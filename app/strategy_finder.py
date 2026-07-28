import pandas as pd


DATABASE = "data/trade_database.csv"


def evaluate_strategy(df, name, condition):

    trades = df[condition]

    if len(trades) == 0:
        return

    print("\n========================")
    print(name)
    print("========================")

    print("Trades:", len(trades))

    print(
        "Win Rate:",
        round(
            (trades["Return_%"] > 0).mean() * 100,
            2
        ),
        "%"
    )

    print(
        "Average Return:",
        round(
            trades["Return_%"].mean(),
            2
        ),
        "%"
    )

    print(
        "Best Trade:",
        round(
            trades["Return_%"].max(),
            2
        ),
        "%"
    )

    print(
        "Worst Trade:",
        round(
            trades["Return_%"].min(),
            2
        ),
        "%"
    )

    print("\nSymbols:")
    print(
        trades["Symbol"].tolist()
    )


def find_strategies():

    df = pd.read_csv(DATABASE)


    print("\n===== STRATEGY FINDER =====")


    # Strategy 1:
    # Pullback continuation setup

    strategy1 = (
        (df["Return_20D"] >= 14) &
        (df["Return_20D"] <= 20) &
        (df["Return_5D"] < 0) &
        (df["RSI"] >= 50) &
        (df["RSI"] <= 60) &
        (df["Distance_From_High_%"] <= -8) &
        (df["Distance_From_High_%"] >= -13)
    )


    evaluate_strategy(
        df,
        "Strategy 1 - Pullback Continuation",
        strategy1
    )


    # Strategy 2:
    # Current ranking approach

    strategy2 = (
        (df["Rank_Score"] >= 80) &
        (df["Momentum_Score"] >= 20) &
        (df["Trend_Score"] >= 20)
    )


    evaluate_strategy(
        df,
        "Strategy 2 - Current Scanner",
        strategy2
    )


    # Strategy 3:
    # Strong trend + reasonable risk

    strategy3 = (
        (df["Rank_Score"] >= 80) &
        (df["Risk_Reward"] >= 3) &
        (df["RSI"] >= 50) &
        (df["RSI"] <= 60)
    )


    evaluate_strategy(
        df,
        "Strategy 3 - Quality Setup",
        strategy3
    )


if __name__ == "__main__":

    find_strategies()
