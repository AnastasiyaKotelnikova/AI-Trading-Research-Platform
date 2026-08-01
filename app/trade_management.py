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



    for _, row in df.iterrows():


        # =============================
        # Input values
        # =============================

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


        allocation = row.get(
            "Portfolio_Allocation_%",
            0
        )


        conviction = row.get(
            "Final_Conviction_Score",
            0
        )


        if pd.isna(close):
            close = 0


        if pd.isna(atr):
            atr = 0


        if pd.isna(allocation):
            allocation = 0


        if pd.isna(conviction):
            conviction = 0



        # =============================
        # Entry
        # =============================

        entry = round(
            close,
            2
        )



        # =============================
        # ATR Stop Loss
        # =============================

        if atr > 0:

            stop = entry - (
                atr * 2
            )

        else:

            stop = entry * 0.95



        stop = max(
            stop,
            0
        )



        # =============================
        # Adaptive Targets
        # =============================

        risk = entry - stop


        if atr > 0:


            if conviction >= 50:

                target_multiplier_1 = 5
                target_multiplier_2 = 8


            elif conviction >= 40:

                target_multiplier_1 = 4
                target_multiplier_2 = 6


            else:

                target_multiplier_1 = 3
                target_multiplier_2 = 5



            target1 = entry + (
                atr *
                target_multiplier_1
            )


            target2 = entry + (
                atr *
                target_multiplier_2
            )


        else:


            target1 = entry + (
                risk * 2
            )


            target2 = entry + (
                risk * 3
            )



        # =============================
        # Risk per share
        # =============================

        risk_share = (
            entry -
            stop
        )



        # =============================
        # Capital allocation
        # =============================

        capital = (
            account_size *
            allocation /
            100
        )



        # =============================
        # Position sizing
        # =============================

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



        entry_prices.append(
            entry
        )


        stop_losses.append(
            round(stop,2)
        )


        targets_1.append(
            round(target1,2)
        )


        targets_2.append(
            round(target2,2)
        )


        risk_per_shares.append(
            round(risk_share,2)
        )


        recommended_shares.append(
            shares
        )


        capital_allocations.append(
            round(capital,2)
        )



    # =============================
    # Add columns
    # =============================

    df["Entry_Price"] = entry_prices

    df["Stop_Loss"] = stop_losses

    df["Target_1"] = targets_1

    df["Target_2"] = targets_2

    df["Risk_Per_Share"] = risk_per_shares

    df["Recommended_Shares"] = recommended_shares

    df["Capital_Allocation_$"] = capital_allocations



    # =============================
    # Reward Risk
    # =============================

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

        reward_distance

        /

        risk_distance.replace(
            0,
            0.01
        )

    ).round(2)



    # =============================
    # Expected Value
    # =============================

    if "Combined_ML_Probability" in df.columns:

        win_probability = df[
            "Combined_ML_Probability"
        ]


    elif "ML_Probability" in df.columns:

        win_probability = df[
            "ML_Probability"
        ]


    else:

        win_probability = 0.5



    if isinstance(
        win_probability,
        pd.Series
    ):

        if win_probability.max() > 1:

            win_probability = (
                win_probability / 100
            )


        win_probability = win_probability.clip(
            0,
            1
        )


    else:

        win_probability = 0.5



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