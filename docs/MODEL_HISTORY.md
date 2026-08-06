AI Trading Research Platform — Model History

Last Updated:

2026-08-06

Purpose

This document records the evolution of every machine learning model used by the AI Trading Research Platform.

For each model version we document:

training dataset
feature set
algorithm
hyperparameters
validation methodology
evaluation metrics
historical backtesting
production deployment
retirement decisions
lessons learned

The objective is to ensure every model decision is reproducible, transparent, and supported by quantitative evidence.

Machine Learning Architecture Overview

The platform currently contains two independent machine learning paths.

These systems solve different problems and are evaluated separately.

They must never be merged without a documented experiment.

ML Path 1 — Historical Prediction Model
Purpose

Predict the probability that historical market conditions lead to successful trades.

Primary training module:

app/train_model.py

Dataset:

data/historical_ml_dataset.csv

Target variable:

Successful_Trade

Validation:

Chronological split.

Training:

Before 2026-05-15

Testing:

After 2026-05-15

This prevents future information leakage and better simulates real-world deployment.

Historical Feature Set

The current historical model uses approximately twenty technical features including:

Return_5D
Return_10D
Return_20D
RSI
RSI_Change
SMA20
SMA50
Above_SMA20
Above_SMA50
SMA_Gap
Momentum_Acceleration
Average_Volume
RVOL
ATR
ATR_Percent
Volatility_20D
Range_Position
Distance_From_52W_High
Volume_Trend
Relative Strength
ML Path 2 — Scanner Prediction Model
Purpose

Evaluate current market opportunities during daily scanning.

Primary module:

app/ml_predictor.py

Outputs:

ML_Probability
ML_Prediction
ML_Model
ML_Accuracy
ML_F1

This model supports:

AI Research Ranking
Confidence scoring
Portfolio evaluation
Trade approval
Final AI decisions

It is not the historical training model.

Model Development Timeline
Early Models (v1 – v6)

Status:

RETIRED

Purpose:

Initial proof-of-concept models.

Characteristics:

small datasets
limited features
basic validation
simple classifiers

Problems:

insufficient historical data
unstable performance
weak validation

Decision:

Retired.

model_v7

Status:

REJECTED

Improvements:

improved evaluation metrics
F1 score
Precision
Recall

Reason:

Did not outperform previous baseline.

model_v8

Status:

REJECTED

Reason:

Marginal improvement.

Insufficient trading value.

model_v9

Status:

REJECTED

Reason:

Failed champion comparison.

model_v10 – model_v26

Status:

RETIRED

General improvements:

additional technical indicators
larger datasets
improved preprocessing
better training pipeline

Limitations:

dataset size still limited
possible leakage
unrealistic validation

Decision:

Retired.

model_v27

Status:

RETIRED

Previous Champion:

Yes

Reported Metrics:

Accuracy:

98.3%

F1:

96.1%

Why model_v27 Was Retired

Although model_v27 reported extremely high classification metrics, the results were determined to be unrealistic.

Issues discovered:

small historical dataset
potential information leakage
optimistic validation
unrealistic market performance

Conclusion:

Classification accuracy alone is not sufficient for selecting production trading models.

The model was permanently retired.

Dataset Expansion Phase

The historical training dataset was expanded substantially.

Improvements:

significantly more historical examples
additional market regimes
additional stocks
improved chronological validation
reduced leakage risk

Dataset:

data/historical_ml_dataset.csv

Training observations:

Approximately 3.5 million

Testing observations:

Approximately 98 thousand

model_v32

Status:

REJECTED

Algorithm:

Random Forest

Configuration:

n_estimators = 500
max_depth = 20
min_samples_leaf = 10

Results:

ROC-AUC:

0.669

F1:

0.467

Decision:

Rejected.

model_v33

Status:

CURRENT CHAMPION

Accepted:

2026-07-28

Algorithm:

Random Forest

Configuration:

n_estimators = 500

max_depth = 20

min_samples_leaf = 10

max_features = sqrt

class_weight = balanced

Dataset:

Expanded historical ML dataset.

Validation Results

Accuracy:

0.551

F1:

0.467

ROC-AUC:

0.669

Trading Backtest

Historical Trades:

210

Win Rate:

46.7%

Average Return:

0.448%

These metrics were evaluated together rather than relying solely on classification accuracy.

Champion Selection Logic

Models are ranked using multiple evaluation criteria.

Current weighting:

ROC-AUC
30%

Average Return
30%

F1
20%

Win Rate
20%

model_v33 achieved the highest combined production score and became the current champion.

Production Integration (2026-08)

During the August development cycle, the machine learning system was fully integrated into the production research pipeline.

The deployed model now propagates through every downstream component.

The following fields are automatically preserved:

ML_Model

ML_Accuracy

ML_F1

Combined_ML_Probability

These values flow into:

AI Research Engine
AI Decision Engine
Portfolio Manager
Risk Manager
Trade Management
Trade History Database
Model Feedback Loop

Every approved trade now records exactly which model generated the prediction.

This establishes full traceability between model versions and future trading performance.

Trade History Integration

The trade history database now permanently stores model metadata for every approved trade.

Tracked fields include:

Model_Name

Model_Accuracy

Model_F1

Additional AI metadata stored with every trade:

Final_AI_Status

Final_AI_Reason

Final_Conviction_Score

Expected_Value

Trade_Grade

Trade_Execution_Status

Portfolio_Action

Risk_Status

This allows historical trades to be linked directly back to the originating model version.

Model Feedback Loop

A new evaluation component has been implemented.

Primary module:

app/model_feedback_loop.py

Purpose:

Evaluate actual trading performance by model version.

Completed trades are grouped by:

Model_Name

Current metrics include:

completed trades
winning trades
losing trades
win rate
average return
best trade
worst trade

The report also preserves:

Model_Accuracy

Model_F1

Output:

data/models/model_feedback_report.csv

This infrastructure enables future comparison between successive model versions using real trading outcomes.

Current Model Files

Champion model:

data/models/champion_model.pkl

Metrics history:

data/models/model_metrics.csv

Feature importance:

data/models/feature_importance.csv

Prediction history:

data/models/model_predictions.csv

Monitoring:

data/models/model_monitoring.csv

Feedback report:

data/models/model_feedback_report.csv
Current Production Usage

The champion model is now integrated into:

market scanner
AI Research Engine
confidence scoring
portfolio evaluation
trade approval
trade management
trade history
model feedback reporting

It remains research only and is not approved for automated live trading.

Future Model Experiments

Planned research includes:

XGBoost

Compare gradient boosting against Random Forest.

LightGBM

Evaluate high-performance tree ensembles.

CatBoost

Compare categorical boosting performance.

Neural Networks

Investigate deep learning after additional historical validation.

Planned Evaluation Improvements

Future validation work includes:

Probability Calibration

Ensure predicted probabilities match observed success frequency.

Walk-Forward Validation

Repeated chronological retraining rather than a single train/test split.

Risk Metrics

Add:

Sharpe Ratio
Sortino Ratio
Maximum Drawdown
Profit Factor
Expectancy
CAGR
Model Training Requirements

Every future model must record:

training date
dataset size
feature count
added features
removed features
algorithm
hyperparameters
validation method
evaluation metrics
backtest performance
deployment decision
retirement reason (if applicable)
Model Evaluation Philosophy

The platform does not optimize for the highest classification accuracy.

Models are selected using a combination of:

predictive performance
historical trading results
realistic validation
reproducibility
robustness across market conditions
transparent decision making

The objective is to build machine learning models that continue to perform under realistic market conditions rather than models that only achieve impressive offline metrics.
