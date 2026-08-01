import pandas as pd


def add_trade_management(
    df,
    account_size=10000,
    max_risk_percent=1
):

    df = df.copy()


    entry_prices = []
    stop_losses = []
    targets_1 = []
    targets_2 = []

    risk_per_shares = []
    recommended_shares = []
    capital_allocations = []

    trade_grades = []
    trade_statuses = []


    for _, row in df.iterrows():


        close = row.get(
            "Close",
            row.get(
                "Adjusted_Close",
                0
            )
        )


        atr = row.get(
            "ATR",
            0
        )


        conviction = row.get(
            "Final_Conviction_Score",
            0
        )


        allocation = row.get(
            "Portfolio_Allocation_%",
            0
        )


        close = 0 if pd.isna(close) else close
        atr = 0 if pd.isna(atr) else atr
        conviction = 0 if pd.isna(conviction) else conviction
        allocation = 0 if pd.isna(allocation) else allocation



        # ==========================
        # Calculate setup ALWAYS
        # ==========================


        entry = round(close,2)



        if atr > 0:

            stop = entry - atr * 2

        else:

            stop = entry * 0.95



        stop = max(
            stop,
            0
        )


        risk_share = entry - stop



        if conviction >= 50:

            multiplier1 = 5
            multiplier2 = 8


        elif conviction >=40:

            multiplier1 = 4
            multiplier2 = 6


        else:

            multiplier1 = 3
            multiplier2 = 5



        if atr > 0:

            target1 = entry + atr * multiplier1

            target2 = entry + atr * multiplier2


        else:

            target1 = entry + risk_share * 2

            target2 = entry + risk_share * 3



        capital = (
            account_size *
            allocation /
            100
        )


        max_loss = (
            account_size *
            max_risk_percent /
            100
        )


        if risk_share > 0:

            shares = int(
                max_loss /
                risk_share
            )

        else:

            shares = 0



        if entry > 0:

            max_shares = int(
                capital /
                entry
            )

            shares = min(
                shares,
                max_shares
            )



        # ==========================
        # Execution approval
        # ==========================

        final_status = row.get(
            "Final_AI_Status",
            ""
        )


        portfolio_action = row.get(
            "Portfolio_Action",
            ""
        )


        approved = row.get(
            "Portfolio_Approved",
            False
        )


        tradable = (

            final_status == "APPROVED TRADE"
            and
            portfolio_action == "ALLOW ENTRY"
            and
            bool(approved)

        )



        if tradable:

            trade_grade = "A"
            trade_status = "READY"


        else:

            trade_grade = "Avoid"
            trade_status = "BLOCKED"

            shares = 0
            capital = 0



        entry_prices.append(entry)
        stop_losses.append(round(stop,2))
        targets_1.append(round(target1,2))
        targets_2.append(round(target2,2))

        risk_per_shares.append(
            round(risk_share,2)
        )

        recommended_shares.append(
            shares
        )

        capital_allocations.append(
            round(capital,2)
        )


        trade_grades.append(
            trade_grade
        )

        trade_statuses.append(
            trade_status
        )



    # ==========================
    # Output columns
    # ==========================


    df["Entry_Price"] = entry_prices
    df["Stop_Loss"] = stop_losses
    df["Target_1"] = targets_1
    df["Target_2"] = targets_2

    df["Risk_Per_Share"] = risk_per_shares

    df["Recommended_Shares"] = recommended_shares

    df["Capital_Allocation_$"] = capital_allocations


    df["Trade_Grade"] = trade_grades

    df["Trade_Status"] = trade_statuses



    # ==========================
    # Reward Risk
    # ==========================


    risk_distance = (
        df["Entry_Price"]
        -
        df["Stop_Loss"]
    )


    reward_distance = (
        df["Target_1"]
        -
        df["Entry_Price"]
    )


    df["Reward_Risk"] = (

        reward_distance /

        risk_distance.replace(
            0,
            0.01
        )

    ).round(2)



    # ==========================
    # Expected Value
    # ==========================


    if "Combined_ML_Probability" in df.columns:

        win_probability = df[
            "Combined_ML_Probability"
        ]


    elif "ML_Probability" in df.columns:

        win_probability = df[
            "ML_Probability"
        ]


    else:

        win_probability = pd.Series(
            0.5,
            index=df.index
        )



    win_probability = pd.to_numeric(
        win_probability,
        errors="coerce"
    ).fillna(0.5)



    if win_probability.max() > 1:

        win_probability /= 100



    win_probability = win_probability.clip(
        0,
        1
    )



    df["Expected_Value"] = (

        (
            win_probability *
            df["Reward_Risk"]
        )

        -

        (
            1 -
            win_probability
        )

    ).round(3)



    return df