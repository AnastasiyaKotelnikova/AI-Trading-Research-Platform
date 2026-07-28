import os
import shutil
import subprocess
import sys


UPDATED_DATASET = (
    "data/historical_ml_dataset_updated.csv"
)

MASTER_DATASET = (
    "data/historical_ml_dataset.csv"
)


def run_step(name, command):

    print()
    print("=" * 50)
    print(name)
    print("=" * 50)

    result = subprocess.run(command)

    if result.returncode != 0:

        print()
        print(name, "FAILED")
        return False

    print()
    print(name, "COMPLETE")

    return True


def main():

    print()
    print("=======================================")
    print(" AI MODEL UPDATE PIPELINE")
    print("=======================================")

    #
    # Step 1
    #

    if not run_step(

        "Updating Training Labels",

        [
            sys.executable,
            "-m",
            "app.update_training_labels"
        ]

    ):

        return

    #
    # Step 2
    #

    if os.path.exists(UPDATED_DATASET):

        shutil.copy(

            UPDATED_DATASET,

            MASTER_DATASET

        )

        print()

        print("Historical dataset updated.")

    else:

        print()

        print("Updated dataset not found.")

        return

    #
    # Step 3
    #

    if not run_step(

        "Training New Model",

        [
            sys.executable,
            "-m",
            "app.train_model"
        ]

    ):

        return

    #
    # Finished
    #

    print()
    print("=======================================")
    print(" PIPELINE COMPLETE")
    print("=======================================")

    print()

    print("Champion model is up to date.")


if __name__ == "__main__":

    main()
