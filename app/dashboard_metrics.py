def calculate_dashboard_metrics(df):

    metrics = {}

    metrics["Stocks_Scanned"] = len(df)

    metrics["Strong_Buy"] = (
        (df["Signal"] == "STRONG BUY").sum()
    )

    metrics["Buy"] = (
        (df["Signal"] == "BUY").sum()
    )

    metrics["Watch"] = (
        (df["Signal"] == "WATCH").sum()
    )

    metrics["Avoid"] = (
        (df["Signal"] == "AVOID").sum()
    )


    # use only ranked candidates
    top_candidates = df.head(20)


    metrics["Average_Rank"] = round(
        top_candidates["Rank_Score"].mean(),
        1
    )


    metrics["Average_RR"] = round(
        top_candidates["Risk_Reward"].mean(),
        2
    )


    return metrics
