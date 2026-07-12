from app.providers.finnhub import get_quote


for symbol in ["MU", "PLUG", "ACHR"]:

    print(get_quote(symbol))