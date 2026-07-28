import pandas as pd
import mplfinance as mpf

from pathlib import Path


RESEARCH_FILE = Path(
    "data/analysis/research_ranked.csv"
)

HISTORY_DIR = Path(
    "data/cache/history"
)

OUTPUT_DIR = Path(
    "data/charts/professional"
)



def create_professional_charts():

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )


    research_df = pd.read_csv(
        RESEARCH_FILE
    )


    top_stocks = (
        research_df
        .sort_values(
            by="Research_Score",
            ascending=False
        )
        .head(10)
    )


    for _, stock in top_stocks.iterrows():

        symbol = stock["Symbol"]


        history_file = (
            HISTORY_DIR /
            f"{symbol}.csv"
        )


        if not history_file.exists():

            continue


        df = pd.read_csv(
            history_file
        )


        df["Date"] = pd.to_datetime(
            df["Date"]
        )


        df = df.sort_values(
            "Date"
        )


        df = df.set_index(
            "Date"
        )


        # Moving averages

        df["SMA20"] = (
            df["Close"]
            .rolling(20)
            .mean()
        )


        df["SMA50"] = (
            df["Close"]
            .rolling(50)
            .mean()
        )


        addplots = [

            mpf.make_addplot(
                df["SMA20"]
            ),

            mpf.make_addplot(
                df["SMA50"]
            )

        ]


        entry = stock["Entry"]
        target1 = stock["Target_1"]
        target2 = stock["Target_2"]
        stop = stock["Stop"]


        horizontal_lines = dict(

            hlines=[
                entry,
                target1,
                target2,
                stop
            ],

            colors=[
                "blue",
                "green",
                "green",
                "red"
            ],

            linestyle="--"

        )


        output = (
            OUTPUT_DIR /
            f"{symbol}.png"
        )


        mpf.plot(

            df,

            type="candle",

            volume=True,

            addplot=addplots,

            hlines=horizontal_lines,

            title=(
                f"{symbol} AI Trading Setup"
            ),

            ylabel="Price",

            ylabel_lower="Volume",

            figsize=(
                12,
                8
            ),

            savefig=dict(
                fname=output,
                dpi=150,
                bbox_inches="tight"
            )

        )


    print(
        "Professional charts created:"
    )

    print(
        OUTPUT_DIR
    )



if __name__ == "__main__":

    create_professional_charts()
