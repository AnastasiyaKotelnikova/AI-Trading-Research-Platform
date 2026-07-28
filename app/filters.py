import pandas as pd


def apply_filters(
    df,

    # Price filter
    min_price=5,
    max_price=1200,

    # Movement filter
    min_change=3,

    # Volume filter
    min_volume=500_000,

    # Relative volume
    min_rvol=3,

    # Dollar liquidity
    min_dollar_volume=25_000_000
):

    filtered = df.copy()


    # -------------------------
    # Price
    # -------------------------
    filtered = filtered[
        (filtered["Price"] >= min_price) &
        (filtered["Price"] <= max_price)
    ]


    # -------------------------
    # Daily movement
    # -------------------------
    filtered = filtered[
        filtered["Change_%"] >= min_change
    ]


    # -------------------------
    # Average Volume Liquidity
    # -------------------------
    filtered = filtered[
        filtered["Average_Volume"] >= min_volume
    ]


    # -------------------------
    # Relative Volume
    # -------------------------
    filtered = filtered[
        filtered["RVOL"] >= min_rvol
    ]


    # -------------------------
    # Dollar volume
    # -------------------------
    filtered = filtered[
        filtered["Dollar_Volume"] >= min_dollar_volume
    ]


    return filtered
