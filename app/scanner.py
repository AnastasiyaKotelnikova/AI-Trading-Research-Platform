import os
from app.explanation import build_explanation
import pandas as pd
from app.scoring import calculate_scores
import time
import json
import yfinance as yf
from datetime import datetime


# =========================
# CONFIG
# =========================

MODE = "SAFE"

SAFE_BATCH_SIZE = 80
AGGRESSIVE_BATCH_SIZE = 300

SAFE_SLEEP = 2.0
AGGRESSIVE_SLEEP = 0.5


LIMIT_SYMBOLS = None

# =========================
# ETF / LEVERAGED PRODUCT FILTER
# =========================

ETF_BLOCKLIST = [
    "SOXL",
    "NVDL",
    "NVDX",
    "TQQQ",
    "SQQQ",
    "SPXL",
    "SPXS"
]


# =========================
# LOAD UNIVERSE
# =========================

def load_symbols():

    import pandas as pd

    df = pd.read_csv(
        "data/universe/tradable_symbols.csv"
    )

    return df["Symbol"].tolist()



# =========================
# BATCH CONTROL
# =========================

def chunk_list(lst, size):

    for i in range(0, len(lst), size):
        yield lst[i:i + size]



def get_batch_size():

    if MODE == "AGGRESSIVE":
        return AGGRESSIVE_BATCH_SIZE

    return SAFE_BATCH_SIZE



def get_sleep():

    if MODE == "AGGRESSIVE":
        return AGGRESSIVE_SLEEP

    return SAFE_SLEEP



# =========================
# DOWNLOAD DATA
# =========================

def fetch_batch(batch):

    try:

        data = yf.download(
            tickers=" ".join(batch),
            period="3mo",
            interval="1d",
            group_by="ticker",
            threads=True,
            progress=False,
            auto_adjust=False
        )

        return data


    except Exception as e:

        print("Batch error:", e)

        return None



# =========================
# ANALYZE STOCKS
# =========================

def analyze(batch, data, spy_return):

    results = []

    debug = {
        "not_in_data": 0,
        "empty": 0,
        "short_history": 0,
        "low_price": 0,
        "low_volume": 0,
        "low_rvol": 0,
        "low_change": 0,
        "low_dollar_volume": 0,
        "errors": 0
    }

    for sym in batch:


        try:

            if sym not in data:
                debug["not_in_data"] += 1
                continue
            
            df = data[sym]

            if df is None or df.empty:
                debug["empty"] += 1
                continue

            # Keep only valid rows
            df = df.dropna(subset=["Open", "Close", "Volume"])

            if len(df) < 20:
                debug["short_history"] += 1
                continue

            close = float(df["Close"].iloc[-1])
            open_price = float(df["Open"].iloc[-1])
            volume = int(df["Volume"].iloc[-1])


            if (
                pd.isna(close)
                or pd.isna(open_price)
                or pd.isna(volume)
            ):
                continue

            if open_price <= 0:
                continue

            volume_series = df["Volume"].dropna()

            if len(volume_series) < 20:
                continue

            avg_volume = volume_series.tail(20).mean()

            if pd.isna(avg_volume) or avg_volume <= 0:
                continue

            rvol = volume / avg_volume

            # Average dollar volume (20-day liquidity)
            avg_dollar_volume = close * avg_volume

            if avg_dollar_volume < 20_000_000:
                continue

            if pd.isna(rvol):
                continue

            change = ((close - open_price) / open_price) * 100

            # =====================
            # TREND ANALYSIS
            # =====================

            sma20 = (
                df["Close"]
                .rolling(20)
                .mean()
                .iloc[-1]
            )

            sma50 = (
                df["Close"]
                .rolling(50)
                .mean()
                .iloc[-1]
            )


            above_sma20 = close > sma20
            above_sma50 = close > sma50


            # =========================
            # 20 DAY HIGH / BREAKOUT
            # =========================

            previous_high_20 = (
                df["High"]
                .rolling(20)
                .max()
                .iloc[-2]
            )

            if pd.isna(previous_high_20):
                continue

            breakout = close >= previous_high_20

            distance_from_high = (
                (previous_high_20 - close)
                /
                previous_high_20
            ) * 100


            # =========================
            # RELATIVE STRENGTH VS SPY
            # =========================

            if len(df) < 21:
                debug["short_history"] += 1
                continue

            stock_return = (
                close
                /
                float(df["Close"].iloc[-21])
                - 1
            ) * 100

            relative_strength = (
                stock_return
                - spy_return
            )

            if pd.isna(change):
                continue


            # Filters
            if close < 10:
                debug["low_price"] += 1
                continue

            if close > 500:
                continue

            if volume < 2_000_000:
                debug["low_volume"] += 1
                continue

            if rvol < 2:
                debug["low_rvol"] += 1
                continue

            if change <= 2:
                debug["low_change"] += 1
                continue

            dollar_volume = close * volume

            if dollar_volume < 50_000_000:
                debug["low_dollar_volume"] += 1
                continue

            results.append({

                "Symbol": sym,
                "Price": round(close, 2),
                "Change_%": round(change, 2),
                "Volume": volume,
                "RVOL": round(rvol, 2),
                "Dollar_Volume": round(dollar_volume, 2),
                "Avg_Dollar_Volume": round(avg_dollar_volume, 2),
                "Breakout": breakout,
                "Above_SMA20": above_sma20,
                "Above_SMA50": above_sma50,
                "Distance_From_High_%": round(
                    distance_from_high,
                    2
                ),
                "Relative_Strength": round(
                    relative_strength,
                    2
                ),
            })

        except Exception as e:
            debug["errors"] += 1
            continue

    print("DEBUG:", debug)

    return results


# =========================
# MAIN SCANNER
# =========================

def run_scanner():


    print(
        f"\n🔥 MARKET SCANNER STARTED — MODE: {MODE}\n"
    )


    print("Loading symbols...")

    symbols = load_symbols()

    print("Symbols loaded:", len(symbols))


    # =========================
    # MARKET BENCHMARK (SPY)
    # =========================

    print("Loading SPY...")

    spy_data = yf.download(
        "SPY",
        period="3mo",
        interval="1d",
        progress=False,
        auto_adjust=False,
        timeout=10
    )


    if spy_data.empty or len(spy_data) < 21:

        print("⚠ SPY unavailable - using neutral market condition")
        spy_return = 0

    else:

        spy_return = (
            spy_data["Close"].iloc[-1].item()
            /
            spy_data["Close"].iloc[-21].item()
            - 1
        ) * 100

        print(
            f"SPY loaded | 20-day return: {spy_return:.2f}%"
        )


    if LIMIT_SYMBOLS:
        symbols = symbols[:LIMIT_SYMBOLS]


    batch_size = get_batch_size()

    sleep_time = get_sleep()


    all_results = []


    total_batches = (
        len(symbols)//batch_size
    ) + 1


    for i, batch in enumerate(
        chunk_list(symbols, batch_size)
    ):

        print(
            f"Batch {i+1}/{total_batches} | size={len(batch)}"
        )


        data = fetch_batch(batch)


        if data is None:
            continue


        results = analyze(
            batch,
            data,
            spy_return
        )


        all_results.extend(results)


        time.sleep(
            sleep_time
        )


    # =========================
    # SCORE AND RANK
    # =========================

    print("Total candidates found:", len(all_results))

    df = pd.DataFrame(all_results)


    if not df.empty:

        df = calculate_scores(df)

        explanations = []

        for _, row in df.iterrows():
            explanations.append(
                build_explanation(row)
            )

        df["Reasons"] = [
            x["Reasons"]
            for x in explanations
        ]

        df["Risks"] = [
            x["Risks"]
            for x in explanations
        ]


        df = df.sort_values(
            by="Scanner_Score",
            ascending=False
        )


        top = df.head(20).to_dict(
            orient="records"
        )


    else:

        top = []


    print(
        "\n=== TOP MOMENTUM STOCKS ==="
    )


    for r in top:

        print("\n" + "=" * 40)

        print(
            f"{r['Symbol']} "
            f"| Score {r['Scanner_Score']}"
        )

        print(
            f"Price: ${r['Price']} "
            f"| Change: +{r['Change_%']}% "
            f"| RVOL: {r['RVOL']}"
        )

        print("\nReasons:")

        for reason in r["Reasons"]:
            print(f"  ✓ {reason}")


        print("\nRisks:")

        if r["Risks"]:
            for risk in r["Risks"]:
                print(f"  ⚠ {risk}")
        else:
            print("  None")


    # =========================
    # SAVE RESULTS
    # =========================

    os.makedirs(
        "data/history",
        exist_ok=True
    )

    timestamp = datetime.now().strftime(
        "%Y-%m-%d_%H-%M"
    )

    # Latest JSON
    with open(
        "data/latest_scan.json",
        "w"
    ) as f:

        json.dump(
            {
                "timestamp": str(datetime.utcnow()),
                "mode": MODE,
                "top_movers": top
            },
            f,
            indent=4
        )

    # Latest CSV
    df.to_csv(
        "data/latest_scan.csv",
        index=False
    )

    # Historical JSON
    with open(
        f"data/history/{timestamp}.json",
        "w"
    ) as f:

        json.dump(
            {
                "timestamp": str(datetime.utcnow()),
                "mode": MODE,
                "top_movers": top
            },
            f,
            indent=4
        )

    # Historical CSV
    df.to_csv(
        f"data/history/{timestamp}.csv",
        index=False
    )


    print(
        "\nSaved → data/latest_scan.json"
    )


# =========================
# RUN
# =========================

if __name__ == "__main__":

    run_scanner()
    
