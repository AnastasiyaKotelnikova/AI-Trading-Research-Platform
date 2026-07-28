"""
Results Manager

Loads scanner results for dashboards and reports.
"""

import os
import pandas as pd


RESULTS_FOLDER = "data/results"


def get_result_file(profile):

    return os.path.join(
        RESULTS_FOLDER,
        f"{profile}_results.csv"
    )



def load_results(profile):

    file = get_result_file(profile)

    if not os.path.exists(file):

        return pd.DataFrame()


    return pd.read_csv(file)



def get_available_results():

    if not os.path.exists(RESULTS_FOLDER):

        return []


    files = os.listdir(RESULTS_FOLDER)


    profiles = []

    for file in files:

        if file.endswith("_results.csv"):

            profiles.append(
                file.replace(
                    "_results.csv",
                    ""
                )
            )


    return profiles



if __name__ == "__main__":


    print(
        "Available results:"
    )

    print(
        get_available_results()
    )


    df = load_results("scalp")


    print()

    print(
        df.head()
    )
