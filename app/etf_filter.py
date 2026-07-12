ETF_BLOCKLIST = {
    "SOXL",
    "SOXS",
    "NVDL",
    "NVDX",
    "TQQQ",
    "SQQQ",
    "SPXL",
    "SPXS",
    "UPRO",
    "SPY",
    "QQQ",
    "IWM"
}


def is_etf(symbol):

    return symbol in ETF_BLOCKLIST