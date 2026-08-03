import pandas as pd


def add_trade_management(
    df,
    account_size=10000,
    max_risk_percent=1
):

    df = df.copy()


    entries = []
    stops = []
    targets1 = []
    targets2 = []

    risk_per_share_list = []
    shares_list = []
    capital_list = []

    grades = []
    statuses = []



    for _, row in df.iterrows():

        symbol = row.get(
            "Symbol",
            ""
        )


        # =========================
        # Inputs
        # =========================

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
            10
        )



        close = (
            0
            if pd.isna(close)
            else float(close)
        )


        atr = (
            0
            if pd.isna(atr)
            else float(atr)
        )


        conviction = (
            0
            if pd.isna(conviction)
            else float(conviction)
        )


        allocation = (
            10
            if pd.isna(allocation)
            or allocation == 0
            else float(allocation)
        )



        # =========================
        # Trade Setup
        # =========================

        entry = round(
            close,
            2
        )


        if atr > 0:

            stop = entry - atr * 2

        else:

            stop = entry * 0.95



        stop = max(
            stop,
            0
        )


        risk = entry - stop



        if conviction >= 50:

            m1 = 5
            m2 = 8


        elif conviction >= 40:

            m1 = 4
            m2 = 6


        else:

            m1 = 3
            m2 = 5




        if atr > 0:

            target1 = entry + atr * m1

            target2 = entry + atr * m2


        else:

            target1 = entry + risk * 2

            target2 = entry + risk * 3





        # =========================
        # Approval Logic
        # =========================


        final_status = str(
            row.get(
                "Final_AI_Status",
                ""
            )
        ).strip().upper()



        portfolio_action = str(
            row.get(
                "Portfolio_Action",
                ""
            )
        ).strip().upper()



        risk_status = str(
            row.get(
                "Risk_Status",
                ""
            )
        ).strip().upper()




        approved = row.get(
            "Portfolio_Approved",
            False
        )



        if isinstance(
            approved,
            str
        ):

            approved = (
                approved
                .strip()
                .lower()
                in
                [
                    "true",
                    "yes",
                    "1"
                ]
            )


        else:

            approved = bool(
                approved
            )



        tradable = (

            final_status ==
            "APPROVED TRADE"

            and

            portfolio_action ==
            "ALLOW ENTRY"

            and

            risk_status ==
            "RISK APPROVED"

            and

            approved

        )



        print(
            "TRADE MANAGEMENT:",
            symbol,
            "| Final:",
            final_status,
            "| Portfolio:",
            portfolio_action,
            "| Risk:",
            risk_status,
            "| Approved:",
            approved,
            "| Tradable:",
            tradable
        )





        # =========================
        # Grade
        # =========================


        if tradable:

            grade = "A"

            status = "READY"



        elif final_status == "WATCHLIST":

            grade = "B"

            status = "WATCH"



        elif final_status == "MONITOR":

            grade = "C"

            status = "MONITOR"



        else:

            grade = "D"

            status = "BLOCKED"





        # =========================
        # Position Sizing
        # =========================


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



        if risk > 0:

            shares = int(
                max_loss /
                risk
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



        if not tradable:

            shares = 0

            capital = 0




        # =========================
        # Store
        # =========================


        entries.append(
            entry
        )


        stops.append(
            round(
                stop,
                2
            )
        )


        targets1.append(
            round(
                target1,
                2
            )
        )


        targets2.append(
            round(
                target2,
                2
            )
        )


        risk_per_share_list.append(
            round(
                risk,
                2
            )
        )


        shares_list.append(
            shares
        )


        capital_list.append(
            round(
                capital,
                2
            )
        )


        grades.append(
            grade
        )


        statuses.append(
            status
        )




    # =========================
    # Output
    # =========================


    df["Entry_Price"] = entries

    df["Stop_Loss"] = stops

    df["Target_1"] = targets1

    df["Target_2"] = targets2


    df["Risk_Per_Share"] = risk_per_share_list

    df["Recommended_Shares"] = shares_list

    df["Capital_Allocation_$"] = capital_list


    df["Trade_Grade"] = grades

    df["Trade_Execution_Status"] = statuses





    # =========================
    # Reward Risk
    # =========================


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





    # =========================
    # Expected Value
    # =========================


    if "Combined_ML_Probability" in df.columns:

        probability = df[
            "Combined_ML_Probability"
        ]


    elif "ML_Probability" in df.columns:

        probability = df[
            "ML_Probability"
        ]


    else:

        probability = pd.Series(
            0.5,
            index=df.index
        )



    probability = pd.to_numeric(
        probability,
        errors="coerce"
    ).fillna(0.5)



    if probability.max() > 1:

        probability = probability / 100



    probability = probability.clip(
        0,
        1
    )



    df["Expected_Value"] = (

        probability *

        df["Reward_Risk"]

        -

        (1 - probability)

    ).round(3)



    return df





if __name__ == "__main__":

    print(
        "Trade Management module loaded."
    )