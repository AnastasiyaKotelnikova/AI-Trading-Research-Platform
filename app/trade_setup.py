import ta


def generate_trade_setup(row):

    price = float(row["Price"])


    # -------------------------
    # ATR volatility
    # -------------------------

    try:

        history = row["History"]

        atr_indicator = ta.volatility.AverageTrueRange(
            high=history["High"],
            low=history["Low"],
            close=history["Close"],
            window=14
        )

        atr = atr_indicator.average_true_range().iloc[-1]


    except Exception:

        atr = price * 0.02

    
    # -------------------------
    # Dynamic Stop Loss
    # -------------------------

    try:

        sma20 = history["Close"].rolling(20).mean().iloc[-1]


        # Use the stronger support level
        atr_stop = price - (atr * 1.5)


        stop_loss = min(
            atr_stop,
            sma20 * 0.97
        )

        # Stop must always be below entry
        if stop_loss >= price:

            stop_loss = price - (
                atr * 1.5
            )


    except Exception:

        stop_loss = price - (atr * 1.5)

    # -------------------------
    # Dynamic Targets
    # -------------------------

    recent_high = None

    try:

        recent_high = history["High"].iloc[-21:-1].max()


        resistance_target = recent_high

        atr_target = price + (
            atr * 3
        )


        # Choose stronger upside target
        target_1 = max(
            resistance_target,
            atr_target
        )


        target_2 = target_1 + (
            atr * 3
        )


    except Exception as e:

        print(
            "Target calculation warning:",
            row["Symbol"],
            e
        )


        target_1 = price + (
            atr * 3
        )

        target_2 = price + (
            atr * 6
        )


    # Ensure Target 1 is above price
    if target_1 <= price:

        target_1 = price + (
            atr * 3
        )


    # -------------------------
    # Risk Reward
    # -------------------------

    risk = price - stop_loss

    reward = target_1 - price


    # -------------------------
    # Risk Reward
    # -------------------------

    risk = price - stop_loss

    reward = target_1 - price



    if risk > 0:

        risk_reward = round(
            reward / risk,
            2
        )

    else:

        risk_reward = 0

        # Prevent unrealistic RR
        if risk_reward > 5:

            risk_reward = 5

    print(
        f"{row['Symbol']} | "
        f"Price={price:.2f} | "
        f"Stop={stop_loss:.2f} | "
        f"Target1={target_1:.2f} | "
        f"Risk={risk:.2f} | "
        f"Reward={reward:.2f} | "
        f"RR={risk_reward}"
    )

    return {

        "Entry":
            round(price, 2),


        "Stop_Loss":
            round(stop_loss, 2),


        "Target_1":
            round(target_1, 2),


        "Target_2":
            round(target_2, 2),


        "Risk_Reward":
            risk_reward

    }
