import pandas as pd


def detect_breakout(history, lookback=20):
    """
    Detects whether today's close is above the previous
    'lookback' trading days' highest close.
    """

    if history is None:
        return None

    if len(history) < lookback + 1:
        return None

    df = history.copy()

    df["Close"] = pd.to_numeric(df["Close"])

    current_close = df["Close"].iloc[-1]

    previous_high = df["Close"].iloc[-(lookback + 1):-1].max()

    breakout = current_close > previous_high

    return {
        "Breakout": breakout,
        "Current_Close": round(current_close, 2),
        "Previous_High": round(previous_high, 2),
        "Distance_%": round(
            (current_close - previous_high)
            / previous_high * 100,
            2
        )
    }