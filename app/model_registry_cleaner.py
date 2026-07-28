import pandas as pd
import os


METRICS_FILE = "data/models/model_metrics.csv"


def clean_model_registry():

    print("\n================================")
    print("MODEL REGISTRY CLEANUP")
    print("================================\n")


    if not os.path.exists(METRICS_FILE):

        print("Model metrics file not found")
        return



    df = pd.read_csv(
        METRICS_FILE
    )


    print("Before cleanup:")
    print(len(df), "records")



    # Keep latest entry for each model

    df = (
        df.sort_values(
            by="Date"
        )
        .drop_duplicates(
            subset=["Model"],
            keep="last"
        )
    )



    # Sort models by version

    df["Version"] = (
        df["Model"]
        .str.extract(
            r'(\d+)'
        )
        .astype(int)
    )


    df = df.sort_values(
        "Version"
    )


    df = df.drop(
        columns=["Version"]
    )



    # Save

    df.to_csv(
        METRICS_FILE,
        index=False
    )



    print("\nAfter cleanup:")
    print(len(df), "records")


    print("\nCurrent registry:")
    print(df)



    print("\nSaved:")
    print(METRICS_FILE)



if __name__ == "__main__":

    clean_model_registry()
