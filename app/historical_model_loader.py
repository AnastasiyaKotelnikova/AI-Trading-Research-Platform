import joblib


MODEL_FILE = (
    "data/models/optimized_trading_model.pkl"
)


_MODEL = None



def load_historical_model():

    global _MODEL


    if _MODEL is None:

        print(
            "\nLoading historical ML model..."
        )


        _MODEL = joblib.load(
            MODEL_FILE
        )


    return _MODEL