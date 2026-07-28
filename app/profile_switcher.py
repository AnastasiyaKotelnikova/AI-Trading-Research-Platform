"""
Simple command-line profile switcher.
"""

from app.profile_manager import set_active_profile
from app.profiles import PROFILES


def main():

    print("\nAvailable Profiles:\n")

    profiles = list(PROFILES.keys())

    for i, profile in enumerate(profiles, start=1):
        print(
            f"{i}. {profile.upper()}"
        )


    choice = input(
        "\nSelect profile number: "
    )


    try:

        index = int(choice) - 1

        selected = profiles[index]

        set_active_profile(selected)


    except Exception:

        print(
            "Invalid selection"
        )


if __name__ == "__main__":
    main()
