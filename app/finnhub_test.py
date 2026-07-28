import requests
from config.finnhub_key import FINNHUB_API_KEY


BASE_URL = "https://finnhub.io/api/v1"


stocks = [
    "MU",
    "PLUG",
    "ACHR",
    "ILLR"
]


def get_quote(symbol):

    url = f"{BASE_URL}/quote"

    params = {
        "symbol": symbol,
        "token": FINNHUB_API_KEY
    }

    response = requests.get(
        url,
        params=params
    )

    return response.json()


for stock in stocks:

    data = get_quote(stock)

    print("\n", stock)
    print(data)
