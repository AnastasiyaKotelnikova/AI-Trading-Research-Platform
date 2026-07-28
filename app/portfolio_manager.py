import pandas as pd

from app.regime_controller import get_current_regime, apply_regime_adjustment



def add_portfolio_management(
    df,
    account_size=10000,
    max_positions=10,
    risk_per_trade=0.01
):

    # ------------------------------------
    # Market Regime
    # ------------------------------------

    market_regime = get_current_regime()


    print(
        "\nCurrent Market Regime:",
        market_regime["Market_Regime"]
    )


    print(
        "Market Exposure:",
        market_regime["Exposure"],
        "%"
    )


    portfolio_scores = []

    portfolio_actions = []

    position_allocations = []

    risk_amounts = []

    portfolio_ranks = []



    # ------------------------------------
    # Rank by conviction
    # ------------------------------------

    df = df.sort_values(
        "Final_Conviction_Score",
        ascending=False
    ).reset_index(drop=True)


    for index, row in df.iterrows():


        # --------------------------------
        # Base values
        # --------------------------------

        conviction = row.get(
            "Final_Conviction_Score",
            0
        )


        tier = row.get(
            "Conviction_Tier",
            "TIER 4"
        )


        expected_value = row.get(
            "Expected_Value",
            0
        )


        reward_risk = row.get(
            "Reward_Risk",
            0
        )


        trade_grade = row.get(
            "Trade_Grade",
            "C"
        )


        if pd.isna(expected_value):

            expected_value = 0


        if pd.isna(reward_risk):

            reward_risk = 0



        # --------------------------------
        # Portfolio rank
        # --------------------------------

        portfolio_ranks.append(
            index + 1
        )



        # --------------------------------
        # Position sizing
        # --------------------------------

        allocation = 0



        if tier == "TIER 1":

            allocation = 40


        elif tier == "TIER 2":

            allocation = 25


        elif tier == "TIER 3":

            allocation = 10


        else:

            allocation = 0



        # --------------------------------
        # Grade adjustment
        # --------------------------------

        if trade_grade == "A":

            allocation += 5


        elif trade_grade == "Avoid":

            allocation = 0



        # --------------------------------
        # Expected value adjustment
        # --------------------------------

        if expected_value < -0.25:

            allocation -= 5



        # --------------------------------
        # Reward/Risk adjustment
        # --------------------------------

        if reward_risk >= 2:

            allocation += 5



        if allocation < 0:

            allocation = 0



        if allocation > 50:

            allocation = 50



        # --------------------------------
        # Capital allocation
        # --------------------------------

                # ------------------------------------
        # Apply Market Regime Adjustment
        # ------------------------------------

        adjusted_allocation = apply_regime_adjustment(
            allocation,
            market_regime
        )


        capital_allocation = (

            account_size *

            adjusted_allocation /

            100

        )



        # --------------------------------
        # Risk calculation
        # --------------------------------

        allowed_risk = (

            account_size *

            risk_per_trade

        )


        shares = row.get(
            "Recommended_Shares",
            0
        )


        risk_per_share = row.get(
            "Risk_Per_Share",
            0
        )


        if pd.isna(shares):

            shares = 0


        if pd.isna(risk_per_share):

            risk_per_share = 0



        total_risk = (

            shares *

            risk_per_share

        )



        # --------------------------------
        # Portfolio score
        # --------------------------------

        portfolio_score = conviction



        # EV bonus

        if expected_value > 0:

            portfolio_score += 3


        else:

            portfolio_score -= 3



        # Risk penalty

        if total_risk > allowed_risk:

            portfolio_score -= 10



        # Position limit penalty

        if allocation > 50:

            portfolio_score -= 5



        if portfolio_score < 0:

            portfolio_score = 0



        portfolio_score = round(
            portfolio_score,
            2
        )



        # --------------------------------
        # Portfolio decision
        # --------------------------------

        if (

            portfolio_score >= 50

            and

            tier in [
                "TIER 1",
                "TIER 2"
            ]

            and

            allocation > 0

        ):

            action = "ALLOW ENTRY"



        elif portfolio_score >= 35:

            action = "MONITOR"



        else:

            action = "REJECT"




        portfolio_scores.append(
            portfolio_score
        )


        portfolio_actions.append(
            action
        )


        position_allocations.append(
            round(
                 adjusted_allocation,
                2
            )
        )


        risk_amounts.append(
            round(
                total_risk,
                2
            )
        )



    # ------------------------------------
    # Add columns
    # ------------------------------------

    df["Portfolio_Rank"] = portfolio_ranks

    df["Portfolio_Score"] = portfolio_scores

    df["Portfolio_Action"] = portfolio_actions

    df["Portfolio_Allocation_%"] = position_allocations

    df["Market_Regime"] = (
        market_regime["Market_Regime"]
    )


    df["Market_Exposure_%"] = (
        market_regime["Exposure"]
    )

    df["Portfolio_Risk_$"] = risk_amounts


    # ------------------------------------
    # Portfolio approval flag
    # ------------------------------------

    df["Portfolio_Approved"] = (
        df["Portfolio_Action"]
        ==
        "ALLOW ENTRY"
    )

    df["Portfolio_Status"] = "NOT APPROVED"

    df.loc[
        df["Portfolio_Approved"] == True,
        "Portfolio_Status"
    ] = "APPROVED"


    return df