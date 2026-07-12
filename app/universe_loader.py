import pandas as pd


# =========================
# LOAD NASDAQ SYMBOLS
# =========================

def load_nasdaq():

    df = pd.read_csv(
        "data/universe/nasdaqlisted.txt",
        sep="|"
    )


    # Remove ETFs and test issues
    df = df[
        (df["ETF"] == "N") &
        (df["Test Issue"] == "N")
    ]


    return df["Symbol"].dropna().tolist()



# =========================
# LOAD OTHER EXCHANGES
# =========================

def load_other():

    df = pd.read_csv(
        "data/universe/otherlisted.txt",
        sep="|"
    )


    # Remove ETFs and test issues
    df = df[
        (df["ETF"] == "N") &
        (df["Test Issue"] == "N")
    ]


    return df["ACT Symbol"].dropna().tolist()



# =========================
# SYMBOL CLEANING
# =========================

def is_valid_stock(symbol):

    if not isinstance(symbol, str):
        return False


    symbol = symbol.strip()


    # Remove test symbols
    bad_symbols = {
        "ZTEST",
        "ZEXIT",
        "ZIEXT",
        "ZAZZT",
        "ZBZZT",
        "ZCZZT",
        "ZJZZT",
        "ZWZZT",
        "ZXIET"
    }


    if symbol in bad_symbols:
        return False



    # Remove special formats
    if "." in symbol or "-" in symbol:
        return False


    # Remove warrants
    if symbol.endswith("W"):
        return False


    # Remove units
    if symbol.endswith("U"):
        return False


    # Remove rights
    if symbol.endswith("R"):
        return False


    return True



def clean_symbols(symbols):

    cleaned = []


    for s in symbols:

        if not isinstance(s, str):
            continue


        s = s.strip()


        if "$" in s:
            continue


        if is_valid_stock(s):
            cleaned.append(s)


    return sorted(list(set(cleaned)))



# =========================
# BUILD FINAL UNIVERSE
# =========================

def build_universe():

    nasdaq = load_nasdaq()

    other = load_other()


    symbols = list(
        set(nasdaq + other)
    )


    symbols = clean_symbols(symbols)


    return symbols



# =========================
# TEST
# =========================

if __name__ == "__main__":

    symbols = build_universe()


    print(
        "Total symbols loaded:",
        len(symbols)
    )


    print(
        "Sample:",
        symbols[:30]
    )