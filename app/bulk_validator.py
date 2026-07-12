import yfinance as yf
import pandas as pd
import time

BATCH_SIZE = 200


def chunk(lst, size):
    for i in range(0, len(lst), size):
        yield lst[i:i + size]


def is_valid_batch(batch):
    try:
        data = yf.download(
            tickers=" ".join(batch),
            period="1d",
            interval="1d",
            group_by="ticker",
            threads=True,
            progress=False
        )

        valid = []

        if data is None:
            return valid

        for sym in batch:
            try:
                if sym in data and not data[sym].empty:
                    valid.append(sym)
            except:
                continue

        return valid

    except:
        return []


def run():
    from app.universe_loader import build_universe

    symbols = build_universe()

    print("RAW SYMBOLS:", len(symbols))

    valid = []

    batches = list(chunk(symbols, BATCH_SIZE))
    total = len(batches)

    for i, batch in enumerate(batches):
        print(f"Batch {i+1}/{total} | size={len(batch)}")

        good = is_valid_batch(batch)
        valid.extend(good)

        time.sleep(0.3)

    valid = sorted(list(set(valid)))

    print("\nVALID SYMBOLS:", len(valid))

    df = pd.DataFrame(valid, columns=["symbol"])
    df.to_csv("data/cache/valid_symbols.csv", index=False)

    print("Saved → data/cache/valid_symbols.csv")


if __name__ == "__main__":
    run()