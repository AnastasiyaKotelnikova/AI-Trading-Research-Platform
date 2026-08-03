# AI Trading Research Platform — Model History


Last Updated:

2026-08-03



# Purpose


This document tracks every important machine learning model experiment.


For each model version we record:


- training dataset
- feature set
- algorithm
- training changes
- evaluation metrics
- backtest results
- acceptance/rejection decision
- lessons learned


The purpose is to prevent repeating previous mistakes and maintain transparent model evolution.



---

# Machine Learning Architecture Overview


The platform currently contains **two separate ML paths**.


They serve different purposes and must not be confused.



---


# ML Path 1 — Historical Prediction Model


Purpose:


Train machine learning models using historical market data to estimate the probability of future successful trade outcomes.


Main training module:


```
app/train_model.py
```


Dataset:


```
data/historical_ml_dataset.csv
```


Target:


```
Successful_Trade
```


Validation:


Chronological split:


Training:

Before 2026-05-15


Testing:

After 2026-05-15



Purpose:


Simulate future prediction using unseen historical periods.



Features include:


- Return_5D
- Return_10D
- Return_20D
- RSI
- RSI_Change
- SMA20
- SMA50
- Above_SMA20
- Above_SMA50
- SMA_Gap
- Momentum_Acceleration
- Average_Volume
- RVOL
- Volatility_20D
- ATR
- ATR_Percent
- Range_Position
- Distance_From_52W_High
- Volume_Trend



Current accepted model:


```
model_v33
```



---

# ML Path 2 — Scanner Research Prediction Path


Purpose:


Provide real-time ML confirmation inside the stock scanner and research ranking pipeline.


Main module:


```
app/ml_predictor.py
```


This path is separate from historical model training.


It works with current scanner-generated features:


Examples:


- RSI
- Return_5D
- Return_20D
- Distance_From_High_%
- Above_SMA20
- Above_SMA50
- Breakout
- Overextended
- Rank_Score
- Momentum_Score
- Trend_Score
- Relative_Strength
- Risk_Reward



Outputs:


```
ML_Probability

ML_Prediction

ML_Model

ML_Accuracy

ML_F1
```



Purpose:


Provide additional evidence for:


- research ranking
- AI confidence
- final decision scoring



Important:


The scanner ML path and historical ML path use different feature structures.


They should not be evaluated as the same model system.



---

# Model Development Timeline



# Early Models (v1 - v6)


Status:


RETIRED



Purpose:


Initial ML pipeline experiments.



Characteristics:


- small datasets
- early feature engineering
- limited validation
- basic classification testing



Problems discovered:


- insufficient historical samples
- weak validation
- possible bias



Decision:


Retired.



---

# model_v7


Status:


REJECTED



Reason:


Failed to outperform existing models.



Improvements:


Introduced improved evaluation:


- F1 score
- Precision
- Recall



Decision:


Rejected.



---

# model_v8


Status:


REJECTED



Reason:


Performance improvement was insufficient.



---

# model_v9


Status:


REJECTED



Reason:


Improved metrics but failed champion comparison.



---

# model_v10 - model_v26


Status:


RETIRED



General improvements:


- additional features
- improved training pipeline
- expanded evaluation



Limitations:


Models were still affected by:


- limited historical data
- possible leakage
- insufficient validation



Decision:


Retired.



---

# model_v27


Status:


RETIRED ❌



Previous Champion:


Yes



Reported metrics:


Accuracy:

98.3%



F1:

96.1%



---

# Why model_v27 Was Retired


model_v27 produced extremely strong classification metrics.


However, investigation showed the results were not reliable for trading research.



Problems identified:


## 1. Dataset limitations


The training dataset was too small compared with later expanded datasets.



## 2. Possible data leakage


The validation methodology did not sufficiently protect against future information contamination.



## 3. Unrealistic market prediction performance


A model achieving near-perfect classification accuracy in market prediction requires strong evidence.


The results did not survive realistic validation.



## 4. Poor benchmark quality


High classification metrics alone do not guarantee profitable trading decisions.



Decision:


model_v27 was removed as a performance benchmark.



Important lesson:


A lower-scoring realistic model is more valuable than an unrealistic high-scoring model.



---

# Dataset Expansion Phase


Major improvement:


The historical ML dataset was expanded significantly.



Previous problems addressed:


✓ More historical examples

✓ More stocks

✓ More market conditions

✓ Improved chronological validation

✓ Reduced leakage risk



Current dataset:


File:


```
data/historical_ml_dataset.csv
```



Training records:


3,504,289



Testing records:


98,034



Validation:


Chronological future simulation.



---

# model_v32


Status:


REJECTED



Algorithm:


Random Forest



Configuration:


```
n_estimators = 500

max_depth = 20

min_samples_leaf = 10
```



Results:


ROC-AUC:

0.669



F1:

0.467



Reason:


Did not exceed acceptance criteria.



Decision:


Rejected.



---

# model_v33


Status:


CURRENT CHAMPION ✅



Accepted:


2026-07-28



Algorithm:


Random Forest



Configuration:


```
n_estimators = 500

max_depth = 20

min_samples_leaf = 10

max_features = sqrt

class_weight = balanced
```



Dataset:


Expanded historical ML dataset



Features:


21 technical and market features.



---

# Validation Results


Accuracy:


0.551



F1:


0.467



ROC-AUC:


0.669



---

# Trading Backtest


Trades:


210



Win Rate:


46.7%



Average Return:


0.448%



---

# Champion Selection Logic


The platform does not select models using accuracy alone.



Current scoring:


```
F1:
20%


ROC-AUC:
30%


Average Return:
30%


Win Rate:
20%
```



model_v33 score:


0.430



Previous champion score:


0.192



Decision:


model_v33 accepted as current champion.



---

# Current Model Files


Champion model:


```
data/models/champion_model.pkl
```



Version:


```
model_v33
```



Metrics history:


```
data/models/model_metrics.csv
```



Feature importance:


```
data/models/feature_importance.csv
```



---

# Current Model Usage


The champion model is used for:


- historical probability estimation
- ML confirmation
- research ranking support
- AI decision scoring



It is NOT approved for:


- automatic live trading
- real money execution



Required before live trading:


- walk-forward validation
- longer paper trading
- market regime testing
- risk analysis
- model monitoring



---

# Current Model Evaluation Philosophy


Future models must demonstrate:


## Predictive quality


- F1
- ROC-AUC
- Precision
- Recall
- Calibration



## Trading quality


- number of trades
- win rate
- average return
- drawdown
- risk-adjusted metrics



## Reliability


- no leakage
- realistic validation
- stability across market periods



---

# Future Model Experiments



## XGBoost


Purpose:


Compare gradient boosting performance against Random Forest.



## LightGBM


Purpose:


High-performance tree-based research.



## CatBoost


Purpose:


Alternative boosting approach.



## Neural Networks


Purpose:


Research after dataset and validation systems mature.



---

# Planned Evaluation Improvements


Future improvements:


## Probability Calibration


Predicted probabilities should match historical success frequency.



Example:


A 70% confidence prediction should historically produce approximately 70% successful outcomes.



---


## Walk-Forward Validation


Replace:


Train once → Test once



With:


Train period

↓

Validation

↓

Move forward

↓

Retrain



---


## Risk Metrics


Add:


- Sharpe ratio
- Sortino ratio
- Maximum drawdown
- Profit factor
- Expectancy
- CAGR



---

# Model Training Rules


Every future model must record:


Date:


Dataset size:


Feature count:


Features added:


Features removed:


Algorithm:


Hyperparameters:


Validation method:


Metrics:


Backtest results:


Decision:


Reason:



---

# Important Lesson


The objective is not to create the model with the highest accuracy.


The objective is to create the model that survives realistic market testing.


The platform prioritizes:


✓ realistic performance

✓ reproducibility

✓ risk control

✓ transparent decisions

✓ continuous improvement


