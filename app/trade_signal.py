def generate_trade_signal(row):

    score = row["Rank_Score"]

    rr = row["Risk_Reward"]


    if (
        score >= 90
        and rr >= 2
    ):
        return "STRONG BUY"


    elif (
        score >= 75
        and rr >= 1.5
    ):
        return "BUY"


    elif score >= 60:
        return "WATCH"


    else:
        return "AVOID"
