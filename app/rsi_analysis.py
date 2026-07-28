import pandas as pd


DATABASE_FILE = "data/trade_database.csv"


def rsi_analysis():

    df = pd.read_csv(DATABASE_FILE)


    if "RSI" not in df.columns:

        print("RSI column not found in database")
        return


    df["RSI_Range"] = pd.cut(
        df["RSI"],
        bins=[0,50,60,70,80,100]
    )


    print("\n===== RSI PERFORMANCE =====\n")


    result = (
        df.groupby("RSI_Range")
        .agg(
            Trades=("Symbol","count"),
            Win_Rate=("Return_%",lambda x:(x>0).mean()*100),
            Avg_Return=("Return_%","mean")
        )
    )


    print(result.round(2))


if __name__ == "__main__":

    rsi_analysis()
