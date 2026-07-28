from app.providers.yahoo import get_history
from app.breakout import detect_breakout

symbols = [
    "NVVE",
    "AAPL",
    "MU",
    "PLUG",
    "AARD"
]

for symbol in symbols:

    print("\n", symbol)

    history = get_history(symbol)

    result = detect_breakout(history)

    print(result)
