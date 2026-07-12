import requests

from config.finnhub_key import FINNHUB_API_KEY


BASE_URL = "https://finnhub.io/api/v1"


def get_quote(symbol):

    url = f"{BASE_URL}/quote"

    params = {
        "symbol": symbol,
        "token": FINNHUB_API_KEY
    }

    try:

        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        data = response.json()


        return {
            "Symbol": symbol,
            "Price": data.get("c"),
            "Change_%": data.get("dp"),
            "High": data.get("h"),
            "Low": data.get("l"),
            "Open": data.get("o"),
            "Previous_Close": data.get("pc")
        }


    except Exception as e:

        return {
            "Symbol": symbol,
            "Error": str(e)
        }