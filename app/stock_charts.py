import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


RESEARCH_FILE = Path(
    "data/analysis/research_ranked.csv"
)


HISTORY_DIR = Path(
    "data/cache/history"
)


CHART_DIR = Path(
    "data/charts/stocks"
)



def create_stock_charts():

    CHART_DIR.mkdir(
        parents=True,
        exist_ok=True
    )


    research_df = pd.read_csv(
        RESEARCH_FILE
    )


    stocks = (
        research_df
        .sort_values(
            by="Research_Score",
            ascending=False
        )
        .head(10)
    )


    for _, stock in stocks.iterrows():

        symbol = stock["Symbol"]


        file = HISTORY_DIR / f"{symbol}.csv"


        if not file.exists():

            continue


        df = pd.read_csv(
            file
        )


        df["Date"] = pd.to_datetime(
            df["Date"]
        )


        df = df.sort_values(
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


        # RSI

        delta = (
            df["Close"]
            .diff()
        )


        gain = (
            delta
            .clip(lower=0)
            .rolling(14)
            .mean()
        )


        loss = (
            -delta
            .clip(upper=0)
            .rolling(14)
            .mean()
        )


        rs = gain / loss


        df["RSI"] = (
            100 -
            (100 / (1 + rs))
        )


        fig, axes = plt.subplots(
            3,
            1,
            figsize=(10,8),
            sharex=True,
            gridspec_kw={
                "height_ratios":[3,1,1]
            }
        )


        # PRICE CHART

        axes[0].plot(
            df["Date"],
            df["Close"]
        )


        axes[0].plot(
            df["Date"],
            df["SMA20"]
        )


        axes[0].plot(
            df["Date"],
            df["SMA50"]
        )


        axes[0].set_title(
            f"{symbol} Price Trend"
        )


        axes[0].set_ylabel(
            "Price"
        )


        # Trade levels

        entry = stock["Entry"]
        target1 = stock["Target_1"]
        target2 = stock["Target_2"]
        stop = stock["Stop"]


        axes[0].axhline(
            entry
        )


        axes[0].axhline(
            target1
        )


        axes[0].axhline(
            target2
        )


        axes[0].axhline(
            stop
        )


        last_date = df["Date"].iloc[-1]


        axes[0].text(
            last_date,
            entry,
            " ENTRY"
        )


        axes[0].text(
            last_date,
            target1,
            " TARGET 1"
        )


        axes[0].text(
            last_date,
            target2,
            " TARGET 2"
        )


        axes[0].text(
            last_date,
            stop,
            " STOP"
        )



        # Volume

        axes[1].bar(
            df["Date"],
            df["Volume"]
        )


        axes[1].set_ylabel(
            "Volume"
        )



        # RSI

        axes[2].plot(
            df["Date"],
            df["RSI"]
        )


        axes[2].axhline(
            70
        )


        axes[2].axhline(
            30
        )


        axes[2].set_ylabel(
            "RSI"
        )


        plt.xticks(
            rotation=45
        )


        plt.tight_layout()


        output = (
            CHART_DIR /
            f"{symbol}.png"
        )


        plt.savefig(
            output,
            dpi=150
        )


        plt.close()



    print(
        "Advanced stock charts created:"
    )


    print(
        CHART_DIR
    )



if __name__ == "__main__":

    create_stock_charts()
