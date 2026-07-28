"""
Trading Profiles
Controls scanner behavior without changing core engine.
"""


SCALP_PROFILE = {

    "name": "SCALP",

    # Price
    "min_price": 0.10,
    "max_price": 100,

    # Liquidity
    "min_average_volume": 500_000,
    "min_dollar_volume": 5_000_000,

    # Momentum
    "min_change": 5,
    "min_rvol": 3,

    # Trading style
    "holding_period": "minutes-hours",

    # Risk
    "risk_level": "high",

    # Technical filters
    "avoid_overextended": True,
    "max_rsi": 80,

    # Risk management
    "max_stop_loss_percent": 8,

    # Short-term preference
    "prefer_intraday": True,

    # Advanced filters
    "avoid_overextended": True,
    "require_breakout": False,

    # Premarket
    "require_gap": False,
    "min_gap_percent": 0,

    "require_premarket_volume": False,
    "min_premarket_volume": 0,

    # Catalyst
    "require_news": False,

    # Float
    "max_float": None
}



SWING_PROFILE = {

    "name": "SWING",

    # Price
    "min_price": 5,
    "max_price": 1200,

    # Liquidity
    "min_average_volume": 500_000,
    "min_dollar_volume": 25_000_000,

    # Momentum
    "min_change": 3,
    "min_rvol": 1.5,

    "holding_period": "days-weeks",

    "risk_level": "medium",

    # Advanced filters
    "avoid_overextended": True,
    "require_breakout": False,

    # Premarket
    "require_gap": False,
    "min_gap_percent": 0,

    "require_premarket_volume": False,
    "min_premarket_volume": 0,

    "require_news": False,

    "max_float": None,
}



QUALITY_PROFILE = {

    "name": "QUALITY",

    # Price
    "min_price": 20,
    "max_price": 1200,

    # Liquidity
    "min_average_volume": 500_000,
    "min_dollar_volume": 25_000_000,

    # Momentum
    "min_change": 2,
    "min_rvol": 1.2,

    "holding_period": "weeks-months",

    "risk_level": "low",

    "avoid_overextended": True,
    "require_breakout": False,

    "require_gap": False,
    "min_gap_percent": 0,

    "require_premarket_volume": False,
    "min_premarket_volume": 0,

    "require_news": False,

    "max_float": None
}



# ==================================
# PREMARKET SCALP PROFILE
# ==================================

PREMARKET_SCALP_PROFILE = {

    "name": "PREMARKET SCALP",

    # Price
    "min_price": 0.10,
    "max_price": 50,

    # Liquidity
    "min_average_volume": 500_000,
    "min_dollar_volume": 5_000_000,

    # Momentum
    "min_change": 3,
    "min_rvol": 3,

    # Premarket conditions
    "require_premarket_volume": True,
    "min_premarket_volume": 100_000,

    # Gap
    "require_gap": True,
    "min_gap_percent": 3,

    # Catalyst
    "require_news": True,

    # Trading style
    "holding_period": "minutes-hours",

    # Risk
    "risk_level": "very_high",

    # Float
    "max_float": 50_000_000,

    # Technical
    "avoid_overextended": True,
    "max_rsi": 85,

    # Opening strategy
    "trade_first_hour": True,

    "avoid_overextended": True,
    "require_breakout": False,

    "max_float": 20_000_000

}



# ==================================
# BREAKOUT PROFILE
# ==================================

BREAKOUT_PROFILE = {

    "name": "BREAKOUT",

    # Price
    "min_price": 5,
    "max_price": 1200,

    # Liquidity
    "min_average_volume": 1_000_000,
    "min_dollar_volume": 25_000_000,

    # Momentum
    "min_change": 3,
    "min_rvol": 2,

    # Technical
    "require_breakout": True,

    # Trading style
    "holding_period": "days-weeks",

    # Risk
    "risk_level": "medium-high",

    "avoid_overextended": False,
    "require_breakout": True,

    "require_gap": False,
    "min_gap_percent": 0,

    "require_premarket_volume": False,
    "min_premarket_volume": 0,

    "require_news": False,

    "max_float": None
}



# ==================================
# AVAILABLE PROFILES
# ==================================

PROFILES = {

    "scalp": SCALP_PROFILE,

    "premarket_scalp": PREMARKET_SCALP_PROFILE,

    "breakout": BREAKOUT_PROFILE,

    "swing": SWING_PROFILE,

    "quality": QUALITY_PROFILE

}
