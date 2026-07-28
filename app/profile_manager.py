"""
Profile Manager
Loads and switches active trading profiles.
"""

import json
import os

from app.profiles import PROFILES


ACTIVE_PROFILE_FILE = "data/config/active_profile.json"


def get_active_profile_name():

    if not os.path.exists(ACTIVE_PROFILE_FILE):
        return "swing"

    with open(ACTIVE_PROFILE_FILE, "r") as f:
        data = json.load(f)

    return data.get(
        "active_profile",
        "swing"
    )



def get_active_profile():

    name = get_active_profile_name()

    if name not in PROFILES:
        print(
            f"Unknown profile {name}, using swing"
        )

        name = "swing"


    return PROFILES[name]



def set_active_profile(profile_name):

    if profile_name not in PROFILES:
        raise ValueError(
            f"Profile '{profile_name}' does not exist"
        )


    os.makedirs(
        "data/config",
        exist_ok=True
    )


    with open(ACTIVE_PROFILE_FILE, "w") as f:

        json.dump(
            {
                "active_profile": profile_name
            },
            f,
            indent=4
        )


    print(
        f"Active profile changed to: {profile_name.upper()}"
    )



if __name__ == "__main__":

    print(
        "Current profile:",
        get_active_profile_name()
    )

    print(
        get_active_profile()
    )
