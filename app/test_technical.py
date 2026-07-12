from app.providers.history import get_history
from app.technical_analysis import calculate_technical_indicators


for symbol in [
    "MU",
    "PLUG",
    "AAPL",
    "NVVE"
]:

    print("\n", symbol)

    history = get_history(symbol)

    result = calculate_technical_indicators(history)

    print(result)