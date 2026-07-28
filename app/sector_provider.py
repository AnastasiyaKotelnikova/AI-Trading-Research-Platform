import yfinance as yf


def get_sector(symbol):

    try:

        ticker = yf.Ticker(symbol)

        info = ticker.info

        sector = info.get("sector")


        if sector:
            return sector


        return "Unknown"


    except Exception:

        return "Unknown"
    
