import pandas as pd

from app.regime_controller import (
    get_current_regime,
    apply_regime_adjustment
)


def add_portfolio_management(
    df,
    account_size=10000,
    max_positions=10,
    risk_per_trade=0.01
):

    df = df.copy()


    # =====================================
    # Market Regime
    # =====================================

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



    # =====================================
    # Rank
    # =====================================

    df = df.sort_values(
        "Final_Conviction_Score",
        ascending=False
    ).reset_index(drop=True)



    # =====================================
    # Process Stocks
    # =====================================

    for index, row in df.iterrows():


        conviction = row.get(
            "Final_Conviction_Score",
            0
        )


        expected_value = row.get(
            "Expected_Value",
            0
        )


        tier = row.get(
            "Conviction_Tier",
            "TIER 4"
        )


        trade_grade = row.get(
            "Trade_Grade",
            "C"
        )


        final_status = row.get(
            "Final_AI_Status",
            ""
        )


        if pd.isna(expected_value):
            expected_value = 0



        portfolio_ranks.append(
            index + 1
        )



        # =====================================
        # HARD AI FILTER
        # =====================================

        if final_status == "NO TRADE":

            portfolio_scores.append(
                conviction
            )

            portfolio_actions.append(
                "REJECT"
            )

            position_allocations.append(
                0
            )

            risk_amounts.append(
                0
            )

            continue



        # =====================================
        # Allocation
        # =====================================

        allocation = 0


        if tier == "TIER 1":

            allocation = 40


        elif tier == "TIER 2":

            allocation = 25


        elif tier == "TIER 3":

            allocation = 10



        if trade_grade == "A":

            allocation += 5


        elif trade_grade == "Avoid":

            allocation = 0



        if expected_value >= 0.25:

            allocation += 5


        elif expected_value < -0.25:

            allocation -= 10



        allocation = max(
            0,
            min(allocation,50)
        )



        allocation = apply_regime_adjustment(
            allocation,
            market_regime
        )



        # =====================================
        # Risk
        # =====================================

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



        allowed_risk = (
            account_size *
            risk_per_trade
        )



        # =====================================
        # Portfolio Score
        # =====================================

        portfolio_score = conviction



        if expected_value >= 0.25:

            portfolio_score += 5


        elif expected_value > 0:

            portfolio_score += 3


        elif expected_value < -0.15:

            portfolio_score -= 5



        if total_risk > allowed_risk:

            portfolio_score -= 10



        portfolio_score = max(
            0,
            round(portfolio_score,2)
        )



        # =====================================
        # Entry Threshold
        # =====================================

        regime = market_regime["Market_Regime"]


        if regime == "STRONG_BULL":

            threshold = 45

        elif regime == "BULL":

            threshold = 50

        elif regime == "NEUTRAL":

            threshold = 55

        else:

            threshold = 65



        # =====================================
        # Decision
        # =====================================

        if expected_value < -0.25:

            action = "REJECT"


        elif (
            portfolio_score >= threshold
            and
            tier in [
                "TIER 1",
                "TIER 2"
            ]
            and
            allocation > 0
        ):

            action = "ALLOW ENTRY"


        elif (
            portfolio_score >= 40
            and
            tier in [
                "TIER 2",
                "TIER 3"
            ]
        ):

            action = "WATCH ENTRY"


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
            round(allocation,2)
        )


        risk_amounts.append(
            round(total_risk,2)
        )



    # =====================================
    # Output
    # =====================================

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



    df["Portfolio_Approved"] = (
        df["Portfolio_Action"]
        ==
        "ALLOW ENTRY"
    )



    df["Portfolio_Status"] = (
        df["Portfolio_Action"]
        .map(
            {
                "ALLOW ENTRY":"APPROVED",
                "WATCH ENTRY":"WATCH",
                "MONITOR":"MONITOR",
                "REJECT":"REJECTED"
            }
        )
    )


    return df