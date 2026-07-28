import pandas as pd

from app.technical_analysis import calculate_technical_indicators
from app.providers.yahoo import get_history


INPUT_FILE = "data/cache/market_snapshot.csv"
OUTPUT_FILE = "data/cache/advanced_scanner_results.csv"


def calculate_score(row, technical):

    score = 0

    # Momentum (0-40)
    change = row["Change_%"]

    if change >= 20:
        score += 40
    elif change >= 10:
        score += 30
    elif change >= 5:
        score += 20
    elif change > 0:
        score += 10


    # Relative volume (0-20)
    rvol = row["RVOL"]

    if rvol >= 5:
        score += 20
    elif rvol >= 3:
        score += 15
    elif rvol >= 2:
        score += 10


    # Liquidity (0-20)
    dollar_volume = row["Dollar_Volume"]

    if dollar_volume >= 500_000_000:
        score += 20
    elif dollar_volume >= 100_000_000:
        score += 15
    elif dollar_volume >= 20_000_000:
        score += 10


    # Trend (0-20)
    if technical["Trend"] == "Bullish":
        score += 20


    return score



def scan():

    df = pd.read_csv(INPUT_FILE)

    results = []

    print("Running advanced scanner...\n")


    for index, row in df.iterrows():

        symbol = row["Symbol"]

        history = get_history(symbol)

        if history is None:
            continue


        technical = calculate_technical_indicators(history)


        score = calculate_score(
            row,
            technical
        )


        status = "Healthy"


        if technical["RSI"] >= 85:
            status = "Extended"


        results.append({

            "Symbol": symbol,
            "Price": row["Price"],
            "Change_%": row["Change_%"],
            "RVOL": row["RVOL"],
            "Dollar_Volume": row["Dollar_Volume"],
            "RSI": technical["RSI"],
            "Trend": technical["Trend"],
            "Score": score,
            "Status": status

        })


        print(symbol, score)


    output = pd.DataFrame(results)


    output = output.sort_values(
        by="Score",
        ascending=False
    )


    output.to_csv(
        OUTPUT_FILE,
        index=False
    )


    print("\n🔥 TOP RESULTS\n")
    print(
        output.head(20).to_string(index=False)
    )

    print("\nSaved:")
    print(OUTPUT_FILE)



if __name__ == "__main__":
    scan()
