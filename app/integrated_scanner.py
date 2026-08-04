import os
import pandas as pd


from app.setup_quality import calculate_setup_quality
from app.feature_engineering import add_features
from app.regime_controller import get_current_regime
from app.trade_setup import generate_trade_setup
from app.position_sizing import calculate_position_size
from app.ranking import calculate_rank_score
from app.relative_strength import calculate_relative_strength
from app.sector_cache import get_sector_cached
from app.providers.yahoo import get_history
from app.trade_signal import generate_trade_signal
from app.trade_explanation import generate_trade_reason
from app.signal_explanation import generate_signal_explanation
from app.score_explanation import generate_score_breakdown

from app.history_manager import save_history
from app.profile_manager import get_active_profile
from app.profile_filters import apply_profile_filters


from app.ml_predictor import (
    add_ml_predictions,
    add_historical_ml_predictions
)


from app.ai_ranker import add_ai_score
from app.model_info import get_current_model_info
from app.model_run_tracker import save_model_run
from app.model_performance_tracker import save_prediction_performance


from app.ai_learning_adjustment import apply_learning_adjustment
from app.ai_confidence import add_ai_confidence
from app.ai_explanation import add_ai_explanation
from app.ai_decision_engine import add_ai_decisions
from app.ai_portfolio_selector import add_portfolio_selection
from app.ai_portfolio_report import generate_portfolio_report
from app.trade_quality_filter import apply_trade_quality_filter
from app.ai_investment_analyst import analyze_stocks


INPUT_FILE = "data/cache/market_snapshot.csv"

RESULTS_FOLDER = "data/results"





def run():


    df = pd.read_csv(INPUT_FILE)


    profile = get_active_profile()



    print(
        "ACTIVE PROFILE:",
        profile["name"]
    )



    # -------------------------
    # Liquidity Filter
    # -------------------------

    df = df[
        (df["Price"] >= profile["min_price"]) &
        (df["Price"] <= profile["max_price"]) &
        (df["Average_Volume"] >= profile["min_average_volume"]) &
        (df["Dollar_Volume"] >= profile["min_dollar_volume"]) &
        (df["RVOL"] >= profile["min_rvol"]) &
        (df["Change_%"] >= profile["min_change"])
    ]



    print(
        "Stocks after liquidity filter:",
        len(df)
    )



    results = []



    print("\nRunning integrated scanner...\n")



    model_info = get_current_model_info()



    print("\n================================")
    print("AI MODEL STATUS")
    print("================================")


    print(
        "Model:",
        model_info["Model"]
    )


    print(
        "Accuracy:",
        model_info["Accuracy"],
        "%"
    )


    print(
        "F1 Score:",
        model_info["F1"],
        "%"
    )


    print(
        "Trained:",
        model_info["Date"]
    )


    print("================================\n")





    # -------------------------
    # Market Regime
    # -------------------------


    market_regime = get_current_regime()


    print(
        "Market Regime:",
        market_regime["Market_Regime"]
    )


    print(
        "Market Exposure:",
        market_regime["Exposure"],
        "%"
    )




    # -------------------------
    # Stock Processing
    # -------------------------


    for _, row in df.iterrows():


        symbol = row["Symbol"]


        history = get_history(symbol)



        if history is None:

            continue



        try:


            features = add_features(history)



            if not apply_profile_filters(
                features,
                profile
            ):

                continue




            if profile.get("require_breakout"):


                if not features["Breakout"]:

                    continue





            row = row.copy()


            row["Price"] = features["Close"]

            row["History"] = history

            trade = generate_trade_setup(row)



            setup_quality = calculate_setup_quality(
                features
            )


            position = calculate_position_size(
                trade["Entry"],
                trade["Stop_Loss"],
                setup_quality
            )





            results.append({


                "Symbol": symbol,


                "Sector":
                    get_sector_cached(symbol),



                "Market_Regime":

                    market_regime["Market_Regime"]

                    if market_regime

                    else None,



                "Market_Regime_Score":

                    market_regime["Score"]

                    if market_regime

                    else 0,



                "Price":
                    features["Close"],



                "Change_%":
                    row["Change_%"],



                "Return_5D":
                    features["Return_5D"],



                "Return_10D":
                    features["Return_10D"],



                "Return_20D":
                    features["Return_20D"],



                "RSI":
                    features["RSI"],



                "RSI_Change":
                    features["RSI_Change"],



                "SMA20":
                    features["SMA20"],



                "SMA50":
                    features["SMA50"],



                "Above_SMA20":
                    features["Above_SMA20"],



                "Above_SMA50":
                    features["Above_SMA50"],



                "SMA_Gap":
                    features["SMA_Gap"],



                "Momentum_Acceleration":
                    features["Momentum_Acceleration"],



                "RVOL":
                    row["RVOL"],



                "Volume":
                    row["Volume"],



                "Average_Volume":
                    features["Average_Volume"],



                "Dollar_Volume":
                    features["Dollar_Volume"],



                "Volume_Trend":
                    features["Volume_Trend"],



                "Volatility_20D":
                    features["Volatility_20D"],



                "ATR":
                    features["ATR"],



                "ATR_Percent":
                    features["ATR_Percent"],



                "Range_Position":
                    features["Range_Position"],



                "Distance_From_52W_High":
                    features["Distance_From_52W_High"],



                "Breakout":
                    features["Breakout"],



                "Distance_From_High_%":
                    features["Distance_From_High_%"],



                "Overextended":
                    features["Overextended"],



                "Entry":
                    trade["Entry"],



                "Stop_Loss":
                    trade["Stop_Loss"],



                "Target_1":
                    trade["Target_1"],



                "Target_2":
                    trade["Target_2"],



                "Risk_Reward":
                    trade["Risk_Reward"],



                "Momentum_Score": 0,

                "Trend_Score": 0,

                "Relative_Strength": 0,



                "Setup_Quality":
                    setup_quality,



                "Risk_Per_Share":
                    position["Risk_Per_Share"]
                    if position else None,



                "Shares":
                    position["Shares"]
                    if position else None,



                "Capital_Required":
                    position["Capital_Required"]
                    if position else None


            })



            print(symbol, "processed")



        except Exception as e:


            print(
                symbol,
                "ERROR:",
                e
            )



# -------------------------
# Ranking Layers
# -------------------------

    results_df = pd.DataFrame(results)

    if results_df.empty:

        print(
            "No valid trade setups generated."
        )

        return


    print(
        results_df[
            [
                "Symbol",
                "Risk_Reward"
            ]
        ]
    )



    results_df = calculate_relative_strength(
        results_df
    )



    if "Relative_Strength" not in results_df.columns:

        results_df["Relative_Strength"] = 0



    results_df = calculate_rank_score(
        results_df
    )



    if "Momentum_Score" not in results_df.columns:

        results_df["Momentum_Score"] = 0



    if "Trend_Score" not in results_df.columns:

        results_df["Trend_Score"] = 0





    # -------------------------
    # ML Prediction
    # -------------------------

    results_df = add_ml_predictions(
        results_df
    )



    results_df = add_historical_ml_predictions(
        results_df
    )





    # -------------------------
    # AI Score Layer
    # -------------------------

    results_df["Research_Score"] = (
        results_df["Setup_Quality"]
    )



    results_df["Risk_Adjustment"] = (
        results_df["Risk_Reward"]
        .clip(0,10)
    )



    results_df["Risk_Penalty"] = 0





    results_df = add_ai_score(
        results_df
    )





    # -------------------------
    # Learning Adjustment
    # -------------------------

    results_df = apply_learning_adjustment(
       results_df
    )


    if "AI_Final_Score_Adjusted" not in results_df.columns:

        results_df["AI_Final_Score_Adjusted"] = (
            results_df["AI_Learned_Score"]
        )



    # -------------------------
    # AI Confidence
    # -------------------------

    results_df = add_ai_confidence(
        results_df
    )


    # -------------------------
    # Trade Quality Filter
    # -------------------------

    results_df = apply_trade_quality_filter(
        results_df
    )



    # -------------------------
    # AI Rating
    # -------------------------

    def classify_ai_rating(row):


        score = row.get(
            "AI_Final_Score_Adjusted",
            0
        )


        confidence = row.get(
            "AI_Confidence",
            0
        )


        ml_probability = row.get(
            "ML_Probability",
            0
        )


        # ---------------------------------
        # ML safety filter
        # ---------------------------------

        if ml_probability < 15:

            return "PASS"



        if (
            ml_probability < 20
            and score < 50
        ):

            return "PASS"



        if (
            score >= 75
            and confidence >= 60
        ):

            return "STRONG BUY"



        elif (
            score >= 60
            and confidence >= 45
        ):

            return "BUY"



        elif (
            score >= 40
            and confidence >= 35
        ):

            return "WATCHLIST"



        elif (
            score >= 30
            and confidence >= 25
        ):

            return "WATCH"



        else:

            return "PASS"



    results_df["AI_Rating"] = results_df.apply(
        classify_ai_rating,
        axis=1
    )



    # -------------------------
    # AI Explanation
    # -------------------------

    results_df = add_ai_explanation(
        results_df
    )



    # -------------------------
    # AI Decision Engine
    # -------------------------

    print(
        results_df[
            [
                "Symbol",
                "AI_Rating",
                "AI_Final_Score_Adjusted",
                "AI_Confidence",
                "ML_Probability",
                "Historical_ML_Probability",
                "Risk_Reward"
            ]
        ].to_string(index=False)
    )


    results_df = add_ai_decisions(
        results_df
    )



    # -------------------------
    # AI Investment Analyst
    # -------------------------

    results_df = analyze_stocks(
        results_df
    )



    # -------------------------
    # Portfolio Selection
    # -------------------------

    results_df = add_portfolio_selection(
        results_df
    )



    # -------------------------
    # AI Portfolio Report
    # -------------------------

    generate_portfolio_report(

        results_df,

        market_regime["Market_Regime"]

        if market_regime

        else None

    )
    

    # -------------------------
    # Signal Explanations
    # -------------------------

    results_df["Signal"] = results_df.apply(
        generate_trade_signal,
        axis=1
    )



    results_df["Trade_Reason"] = results_df.apply(
        generate_trade_reason,
        axis=1
    )



    results_df["Signal_Explanation"] = results_df.apply(
        generate_signal_explanation,
        axis=1
    )



    results_df["Score_Breakdown"] = results_df.apply(
        generate_score_breakdown,
        axis=1
    )





    print("\n🔥 AI RANKED STOCKS\n")


    print(
        results_df.head(20)
    )





    # -------------------------
    # Save Results
    # -------------------------

    os.makedirs(
        RESULTS_FOLDER,
        exist_ok=True
    )



    profile_name = (
        profile["name"]
        .lower()
        .replace(" ","_")
    )



    output_file = os.path.join(
        RESULTS_FOLDER,
        f"{profile_name}_results.csv"
    )





    save_history(
        results_df
    )



    save_prediction_performance(
        results_df,
        model_info
    )



    save_model_run(

        model_info,

        results_df,

        market_regime["Market_Regime"]
        if market_regime
        else None

    )


    


    results_df.to_csv(
        output_file,
        index=False
    )


    print(
        results_df[["Symbol", "Risk_Reward"]]
    )


    display_columns = [

        "Symbol",

        "AI_Final_Score_Adjusted",

        "AI_Confidence",

        "AI_Decision",

        "Portfolio_Score",

        "Portfolio_Category",

        "ML_Probability",

        "Historical_ML_Probability",

        "Rank_Score"

    ]



    available_columns = [

        c for c in display_columns

        if c in results_df.columns

    ]




    print(
        results_df[
            available_columns
        ].head(10)
    )



    print("\nSaved:")
    print(output_file)





if __name__ == "__main__":

    run()            