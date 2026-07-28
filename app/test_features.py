from app.providers.yahoo import get_history
from app.feature_engineering import add_features


symbol = "MU"


history = get_history(symbol)


if history is None:
    print("No history returned")
else:

    features = add_features(history)

    print("\nFEATURES FOR", symbol)
    print("-------------------")

    for key, value in features.items():
        print(f"{key}: {value}")
