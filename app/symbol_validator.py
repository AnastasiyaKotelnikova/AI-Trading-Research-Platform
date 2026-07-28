import yfinance as yf
import pandas as pd
import time

BATCH_SIZE = 200


def chunk(lst, size):
    for i in range(0, len(lst), size):
        yield lst[i:i + size]


def is_valid_symbol(symbol):
    try:
        data = yf.download(symbol, period="1d", interval="1d", progress=False)
        if data is None or data.empty:
            return False
        return True
    except:
        return False


def pre_filter(symbols):
    filtered = []

    for s in symbols:
        if not isinstance(s, str):
            continue

        # remove obvious non-common stock instruments
        if "$" in s:
            continue

        # remove weird structured tickers (warrants/units/rights)
        if any(x in s for x in [".W", ".U", ".R"]):
            continue

        filtered.append(s)

    return filtered


def validate_symbols(symbols):
    valid = []

    batches = list(chunk(symbols, BATCH_SIZE))
    total = len(batches)

    for i, batch in enumerate(batches):
        print(f"Testing batch {i+1}/{total} | size={len(batch)}")

        for sym in batch:
            if is_valid_symbol(sym):
                valid.append(sym)

        time.sleep(0.5)

    return valid


def run_validator():
    from app.universe_loader import build_universe

    symbols = build_universe()

    symbols = pre_filter(symbols)

    print("Total raw symbols:", len(symbols))

    valid_symbols = validate_symbols(symbols)

    print("\nVALID SYMBOLS:", len(valid_symbols))

    df = pd.DataFrame(valid_symbols, columns=["symbol"])
    df.to_csv("data/cache/valid_symbols.csv", index=False)

    print("Saved → data/cache/valid_symbols.csv")


if __name__ == "__main__":
    run_validator()
