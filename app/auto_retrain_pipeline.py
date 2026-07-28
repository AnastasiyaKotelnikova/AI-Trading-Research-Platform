import subprocess

from app.retraining_trigger import check_retraining_needed


def run():

    print("\n================================")
    print("AUTO RETRAINING PIPELINE")
    print("================================")

    decision = check_retraining_needed()

    if decision != "RETRAIN":

        print("\nNo retraining required.")

        return

    print("\nStarting automatic retraining...")

    steps = [

        (
            "Build Updated Dataset",
            [
                "python",
                "-m",
                "app.historical_ml_builder"
            ]
        ),

        (
            "Train Candidate Model",
            [
                "python",
                "-m",
                "app.train_ml_model"
            ]
        ),

        (
            "Compare Models",
            [
                "python",
                "-m",
                "app.compare_models"
            ]
        ),

        (
            "Clean Registry",
            [
                "python",
                "-m",
                "app.model_registry_cleaner"
            ]
        )

    ]

    for title, command in steps:

        print("\n----------------------------")
        print(title)
        print("----------------------------")

        subprocess.run(command)

    print("\n================================")
    print("PIPELINE COMPLETE")
    print("================================")


if __name__ == "__main__":

    run()
