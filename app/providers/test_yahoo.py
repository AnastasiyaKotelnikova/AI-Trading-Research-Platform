from app.providers.yahoo import get_daily_data


for symbol in ["MU", "PLUG", "AAPL", "ACHR"]:

    print(get_daily_data(symbol))