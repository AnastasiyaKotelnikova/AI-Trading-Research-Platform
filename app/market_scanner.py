import time
import json
import yfinance as yf
from datetime import datetime

# =========================
# CONFIG
# =========================

MODE = "SAFE"  # SAFE or AGGRESSIVE

SAFE_BATCH_SIZE = 120
AGGRESSIVE_BATCH_SIZE = 500

SAFE_SLEEP = 1.0
AGGRESSIVE_SLEEP = 0.2

# optional limit for testing
LIMIT_SYMBOLS = None


# =========================
# LOAD UNIVERSE
# =========================

def load_symbols():
    from app.universe_loader import build_universe
    return build_universe()


# =========================
# UTILS
# =========================

def chunk_list(lst, size):
    for i in range(0, len(lst), size):
        yield lst[i:i + size]


def get_batch_size():
    return AGGRESSIVE_BATCH_SIZE if MODE == "AGGRESSIVE" else SAFE_BATCH_SIZE


def get_sleep():
    return AGGRESSIVE_SLEEP if MODE == "AGGRESSIVE" else SAFE_SLEEP


# =========================
# DATA FETCH
# =========================

def fetch_batch(batch):
    try:
        data = yf.download(
            tickers=" ".join(batch),
            period="2d",
            interval="1d",
            group_by="ticker",
            threads=True,
            progress=False
        )
        return data
    except Exception as e:
        print("Batch error:", e)
        return None


# =========================
# ANALYSIS
# =========================

def analyze(batch, data):
    results = []

    for sym in batch:
        try:
            if sym not in data:
                continue

            df = data[sym]
            if df is None or df.empty:
                continue

            close = df["Close"].iloc[-1]
            open_price = df["Open"].iloc[-1]

            change = ((close - open_price) / open_price) * 100

            results.append({
                "symbol": sym,
                "price": round(close, 2),
                "change": round(change, 2),
                "score": abs(change)
            })

        except:
            continue

    return results


# =========================
# MAIN ENGINE
# =========================

def run_scanner():
    print(f"\n🔥 MARKET SCANNER STARTED — MODE: {MODE}\n")

    symbols = load_symbols()

    if LIMIT_SYMBOLS:
        symbols = symbols[:LIMIT_SYMBOLS]

    batch_size = get_batch_size()
    sleep_time = get_sleep()

    all_results = []

    total_batches = len(symbols) // batch_size + 1

    for i, batch in enumerate(chunk_list(symbols, batch_size)):
        print(f"Batch {i+1}/{total_batches} | size={len(batch)}")

        data = fetch_batch(batch)
        if data is None:
            continue

        results = analyze(batch, data)
        all_results.extend(results)

        time.sleep(sleep_time)

    # rank results
    all_results.sort(key=lambda x: x["score"], reverse=True)

    top = all_results[:20]

    print("\n=== TOP MOVERS ===")
    for r in top:
        direction = "📈" if r["change"] > 0 else "📉"
        print(f"{r['symbol']:8} {direction} {r['change']:7.2f}% | ${r['price']}")

    # save output
    with open("data/latest_scan.json", "w") as f:
        json.dump({
            "timestamp": str(datetime.utcnow()),
            "mode": MODE,
            "top_movers": top
        }, f, indent=4)

    print("\nSaved → data/latest_scan.json")


# =========================
# RUN
# =========================

if __name__ == "__main__":
    run_scanner()
