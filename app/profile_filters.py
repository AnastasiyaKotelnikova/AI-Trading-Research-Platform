"""
Profile-based filtering.

Controls optional scanner rules that depend
on the active trading profile.
"""


def apply_profile_filters(features, profile):

    """
    Returns True if stock passes profile rules.
    Returns False if stock should be rejected.
    """


    # ---------------------------------
    # Avoid overextended stocks
    # ---------------------------------

    if profile.get("avoid_overextended", False):

        if features.get("RSI", 0) >= 80:
            return False


    # ---------------------------------
    # Require breakout
    # ---------------------------------

    if profile.get("require_breakout", False):

        if not features.get("Breakout", False):
            return False


    # ---------------------------------
    # Premarket gap filter
    # ---------------------------------

    if profile.get("require_gap", False):

        if "Gap_Percent" in features:

            if features["Gap_Percent"] < profile.get(
                "min_gap_percent",
                0
            ):
                return False


    # ---------------------------------
    # Premarket volume filter
    # ---------------------------------

    if profile.get("require_premarket_volume", False):

        if "Premarket_Volume" in features:

            if features["Premarket_Volume"] < profile.get(
                "min_premarket_volume",
                0
            ):
                return False


    # ---------------------------------
    # Float filter
    # ---------------------------------

    if profile.get("max_float"):

        if "Float" in features:

            if features["Float"] > profile["max_float"]:
                return False


    # ---------------------------------
    # Passed all profile rules
    # ---------------------------------

    return True
