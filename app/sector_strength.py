import yfinance as yf


SECTOR_ETFS = {

    "Technology": "XLK",

    "Healthcare": "XLV",

    "Financial Services": "XLF",

    "Consumer Cyclical": "XLY",

    "Consumer Defensive": "XLP",

    "Communication Services": "XLC",

    "Industrials": "XLI",

    "Energy": "XLE",

    "Utilities": "XLU",

    "Real Estate": "XLRE",

    "Basic Materials": "XLB"
}


def get_sector_strength(sector):

    if sector not in SECTOR_ETFS:
        return 0


    ticker = SECTOR_ETFS[sector]


    try:

        data = yf.download(
            ticker,
            period="1mo",
            interval="1d",
            progress=False,
            auto_adjust=False
        )


        if data.empty:
            return 0


        close = data["Close"]


        if len(close) < 10:
            return 0


        return (
            (close.iloc[-1] -
             close.iloc[-10])
            /
            close.iloc[-10]
            * 100
        )


    except Exception:

        return 0



def calculate_sector_strength(df):

    strong = df[
    df["Rank_Score"] >= 70
]


    sector = (
    strong.groupby("Sector")
        .agg(
            Average_Rank=("Rank_Score", "mean"),
            Top20=("Rank_Score", lambda x: (x >= 80).sum()),
            Stocks=("Symbol", "count")
        )
        .reset_index()
    )


    sector["Average_Rank"] = sector[
        "Average_Rank"
    ].round(2)


    sector = sector.sort_values(
        "Average_Rank",
        ascending=False
    )


    return sector
