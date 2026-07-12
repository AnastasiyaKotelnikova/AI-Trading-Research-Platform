from app.providers.history import get_history


for symbol in ["MU","PLUG","AAPL"]:

    print("\n",symbol)

    df = get_history(symbol)

    print(df.tail())