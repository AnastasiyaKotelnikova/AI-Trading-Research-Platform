import pandas as pd

from app.trade_signal import generate_trade_signal


def generate_dashboard(df):

    dashboard = {}

    dashboard["Stocks_Scanned"] = len(df)

    dashboard["Strong_Buy"] = (
        df.apply(generate_trade_signal, axis=1)
        == "STRONG BUY"
    ).sum()

    dashboard["Buy"] = (
        df.apply(generate_trade_signal, axis=1)
        == "BUY"
    ).sum()

    dashboard["Watch"] = (
        df.apply(generate_trade_signal, axis=1)
        == "WATCH"
    ).sum()

    dashboard["Avoid"] = (
        df.apply(generate_trade_signal, axis=1)
        == "AVOID"
    ).sum()

    dashboard["Average_Rank"] = round(
        df.head(20)["Rank_Score"].mean(),
        1
    )

    dashboard["Average_RR"] = round(
        df["Risk_Reward"].mean(),
        2
    )

    return dashboard
