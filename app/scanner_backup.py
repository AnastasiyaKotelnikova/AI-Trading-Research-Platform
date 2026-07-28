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

    from app.universe_loader import build_universe

    return build_universe()



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

def analyze(batch, data):

    results = []

    for sym in batch:

        if sym in ETF_BLOCKLIST:
            continue

        try:

            if sym not in data:
                continue
            
            df = data[sym]

            if df is None or df.empty:
                continue

            # Keep only valid rows
            df = df.dropna(subset=["Open", "Close", "Volume"])

            if len(df) < 20:
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

            if pd.isna(rvol):
                continue

            change = ((close - open_price) / open_price) * 100

            if pd.isna(change):
                continue

            # Filters
            if close < 10:
                continue

            if volume < 2_000_000:
                continue

            if rvol < 2:
                continue

            if change <= 2:
                continue

            dollar_volume = close * volume

            results.append({

                "Symbol": sym,
                "Price": round(close, 2),
                "Change_%": round(change, 2),
                "Volume": volume,
                "RVOL": round(rvol, 2),
                "Dollar_Volume": round(dollar_volume, 2)

            })

        except Exception:
            continue

    return results
            


# =========================
# MAIN SCANNER
# =========================

def run_scanner():


    print(
        f"\n🔥 MARKET SCANNER STARTED — MODE: {MODE}\n"
    )


    symbols = load_symbols()


    if LIMIT_SYMBOLS:

        symbols = symbols[:LIMIT_SYMBOLS]



    batch_size = get_batch_size()

    sleep_time = get_sleep()



    all_results = []



    total_batches = (
        len(symbols)//batch_size
    ) + 1




    for i,batch in enumerate(
        chunk_list(
            symbols,
            batch_size
        )
    ):


        print(
            f"Batch {i+1}/{total_batches} | size={len(batch)}"
        )



        data = fetch_batch(batch)



        if data is None:

            continue



        results = analyze(
            batch,
            data
        )



        all_results.extend(
            results
        )



        time.sleep(
            sleep_time
        )




    # =========================
    # SCORE AND RANK
    # =========================


    df = pd.DataFrame(
        all_results
    )



    if not df.empty:


        df = calculate_scores(
            df
        )


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


        print(

            f"{r['Symbol']:8} "
            f"📈 "
            f"{r['Change_%']:7.2f}% "
            f"| ${r['Price']} "
            f"| RVOL {r['RVOL']} "
            f"| Score {r['Scanner_Score']}"

        )




    # =========================
    # SAVE RESULTS
    # =========================


    with open(
        "data/latest_scan.json",
        "w"
    ) as f:


        json.dump(

            {

                "timestamp":
                    str(datetime.utcnow()),

                "mode":
                    MODE,

                "top_movers":
                    top

            },

            f,

            indent=4

        )



    print(
        "\nSaved → data/latest_scan.json"
    )




# =========================
# RUN
# =========================

if __name__ == "__main__":

    run_scanner()
