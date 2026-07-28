from app.model_loader import (
    get_best_model,
    get_best_model_info
)


from app.historical_model_loader import (
    load_historical_model
)



# ==================================================
# v27 Scanner ML Features
# ==================================================

FEATURE_COLUMNS = [

    "RSI",

    "Return_5D",

    "Return_20D",

    "Distance_From_High_%",

    "Above_SMA20",

    "Above_SMA50",

    "Breakout",

    "Overextended",

    "Rank_Score",

    "Momentum_Score",

    "Trend_Score",

    "Relative_Strength",

    "Risk_Reward"

]



# ==================================================
# Historical ML Features
# ==================================================

HISTORICAL_FEATURE_COLUMNS = [

    "Return_5D",

    "Return_10D",

    "Return_20D",

    "RSI",

    "RSI_Change",

    "SMA20",

    "SMA50",

    "Above_SMA20",

    "Above_SMA50",

    "SMA_Gap",

    "Momentum_Acceleration",

    "Average_Volume",

    "RVOL",

    "Volatility_20D",

    "ATR",

    "ATR_Percent",

    "Range_Position",

    "Distance_From_52W_High",

    "Volume_Trend"

]



# ==================================================
# Model Cache
# ==================================================

_MODEL = None

_MODEL_INFO = None

_HISTORICAL_MODEL = None



# ==================================================
# Load Scanner ML Model (model_v27)
# ==================================================

def load_model():

    global _MODEL
    global _MODEL_INFO


    if _MODEL is None:

        _MODEL = get_best_model()

        _MODEL_INFO = get_best_model_info()


        print(
            "\nScanner ML Model Loaded:"
        )

        print(
            _MODEL_INFO
        )


    return _MODEL





# ==================================================
# Load Historical ML Model
# ==================================================

def load_historical_ml_model():

    global _HISTORICAL_MODEL


    if _HISTORICAL_MODEL is None:


        _HISTORICAL_MODEL = load_historical_model()


        print(
            "\nHistorical ML Model Loaded"
        )


    return _HISTORICAL_MODEL





# ==================================================
# Add Scanner ML Predictions
# ==================================================

def add_ml_predictions(df):


    df = df.copy()


    model = load_model()



    # -----------------------------
    # Validate features
    # -----------------------------

    missing = (

        set(FEATURE_COLUMNS)

        -

        set(df.columns)

    )


    if missing:

        raise ValueError(
            f"Missing ML features: {missing}"
        )



    # -----------------------------
    # Prepare input
    # -----------------------------

    X = df[
        FEATURE_COLUMNS
    ]



    # -----------------------------
    # Probability
    # -----------------------------

    probabilities = (

        model.predict_proba(X)[:,1]

    )


    df["ML_Probability"] = (

        probabilities * 100

    ).round(2)



    # -----------------------------
    # Prediction
    # -----------------------------

    df["ML_Prediction"] = (

        model.predict(X)

    )



    # -----------------------------
    # Metadata
    # -----------------------------

    df["ML_Model"] = (

        _MODEL_INFO["Model"]

    )


    df["ML_Accuracy"] = (

        _MODEL_INFO["Accuracy"]

    )


    df["ML_F1"] = (

        _MODEL_INFO["F1"]

    )


    df["ML_Features"] = (

        len(FEATURE_COLUMNS)

    )



    return df





# ==================================================
# Add Historical ML Predictions
# ==================================================

def add_historical_ml_predictions(df):


    df = df.copy()


    model = load_historical_ml_model()



    # -----------------------------
    # Validate features
    # -----------------------------

    missing = (

        set(HISTORICAL_FEATURE_COLUMNS)

        -

        set(df.columns)

    )


    if missing:

        raise ValueError(
            f"Missing historical ML features: {missing}"
        )



    # -----------------------------
    # Prepare input
    # -----------------------------

    X = df[
        HISTORICAL_FEATURE_COLUMNS
    ]



    # -----------------------------
    # Probability
    # -----------------------------

    probabilities = (

        model.predict_proba(X)[:,1]

    )


    df["Historical_ML_Probability"] = (

        probabilities * 100

    ).round(2)



    return df