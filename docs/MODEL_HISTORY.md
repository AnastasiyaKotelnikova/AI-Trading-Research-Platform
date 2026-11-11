AI Trading Research Platform — Model History

Last Updated:

Last Updated:

2026-11-10

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

### Dataset Provenance Verification — November 2026

The historical dataset expansion records approximately:

- 3,504,289 training observations
- 98,034 testing observations

These figures are preserved as historical experiment records.

A separate project checkpoint identifies approximately 220,849 rows in `data/historical_ml_dataset.csv`.

The relationship between these dataset sizes has not yet been verified.

Before retraining or comparing future models:

1. Identify the exact dataset version used for each experiment.
2. Confirm the source files and generation method.
3. Verify row counts and feature counts.
4. Confirm training and testing date ranges.
5. Check for duplicate observations and data leakage.
6. Record the dataset version associated with each model.

Do not silently replace historical dataset figures or assume that different dataset sizes describe the same training run.

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

model_v33 was accepted as the historical research champion under the documented model-selection framework. Its historical scores and trading results require continued validation before any production-readiness decision.

Status: CURRENT HISTORICAL RESEARCH CHAMPION, NOT PRODUCTION APPROVED.

## Model Governance Development — August 2026

During August 2026, the project expanded model evaluation beyond classification metrics.

### Model Quality Evaluator

Module:

`app/model_quality_evaluator.py`

The evaluator was developed to combine:

- F1 score
- Win rate
- Average return
- Completed-trade count

The documented eligibility rule is:

`Completed_Trades > 0`

Models without completed trading records are excluded from recommended champion selection under this rule.

This is a minimum software eligibility requirement, not proof of sufficient trading evidence.

### Historical Model Feedback Snapshot

The August model-feedback evaluation reported the following values for `model_v33`:

| Metric | Historical result |
|---|---|
| Completed trades | 272 |
| Winning trades | 84 |
| Losing trades | 188 |
| Win rate | 30.88% |
| Average return | 2.65% |
| Best trade | 70.30% |
| Worst trade | -9.96% |
| F1 score | 0.4674 |

These figures are separate from the original 210-trade historical backtest recorded in the `model_v33` development section.

The two sets of results must not be combined or treated as identical evaluation samples.

### Champion Governance

Relevant modules:

- `app/model_quality_evaluator.py`
- `app/champion_manager.py`
- `app/model_champion_tracker.py`
- `app/model_feedback_loop.py`

The model-quality evaluator and champion-management components were developed during August.

The historical research champion remains `model_v33`.

`model_v27` remains retired and excluded from active model evaluation.

The provenance of the 272 completed trades and the end-to-end integration of model governance require additional verification.

No automatic champion promotion should occur solely because a challenger has higher classification metrics.

## Research Pipeline Integration — August 2026

During August 2026, the machine learning architecture was connected to the broader AI research pipeline.

The intended integration supports propagation of model predictions and metadata through downstream components.

Model-related fields include:

- `ML_Model`
- `ML_Accuracy`
- `ML_F1`
- `Combined_ML_Probability`

These fields support:

- AI Research Engine
- AI Decision Engine
- Portfolio Manager
- Risk Manager
- Trade Management
- Trade History Database
- Model Feedback Loop

The architecture is designed to preserve model identity and evaluation metadata so that research outcomes can be associated with their originating model.

### Integration Validation Status

As of November 10, 2026:

- The core research integration architecture has been implemented.
- End-to-end validation remains incomplete.
- Model-governance execution order requires verification.
- Downstream metadata consistency must be checked.
- Error handling and missing-data behavior require testing.

The existence of integration code does not establish that every execution path has been validated.

This remains a research pipeline, not an approved automated live-trading system.


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

Evaluate recorded research-trade outcomes and model-level performance by model version.

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

This infrastructure supports future comparison between model versions using verified trade-outcome records. Historical simulations, research trades, paper trades, and actual broker executions must be distinguished when interpreting performance.

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


## November 10, 2026 — Model Development Checkpoint

**Current phase:** Phase 3 — AI Research Engine

**Implementation estimate:** Approximately 95%

**Current historical research champion:** `model_v33`

**Retired model:** `model_v27`

### Development Review

Development resumed after approximately 2.5 months.

The review identified unfinished model-governance integration and validation tasks.

No new model training experiment or replacement champion was verified during this checkpoint.

### Historical Research Champion

`model_v33` remains the accepted historical research champion.

Its original historical evaluation recorded:

- ROC-AUC: 0.669
- F1: approximately 0.467
- Historical backtest: 210 trades
- Historical backtest win rate: 46.7%
- Historical backtest average return: 0.448%

A separate August model-feedback snapshot recorded:

- Completed trades: 272
- Win rate: 30.88%
- Average return: 2.65%

These are distinct historical evaluation records.

The relationship between the two trade populations and their underlying source data requires verification.

### Current Trade-History State

The November review identified three OPEN research trades:

- KOD
- CNMD
- REZI

Their exit outcomes require historical reconciliation using original entry information, historical market prices, and documented exit rules.

No arbitrary current-price exits or retrospective selection of favorable exit prices should be used.

### Outstanding Model-Governance Tasks

1. Verify `app/model_quality_evaluator.py`.
2. Verify `app/champion_manager.py`.
3. Validate their integration with `app/daily_pipeline.py`.
4. Confirm retired-model exclusions.
5. Verify model-feedback data provenance.
6. Validate champion recommendation and active champion consistency.
7. Test failure handling and downstream outputs.
8. Reconcile outstanding research trades.
9. Confirm historical dataset versions and feature consistency.

### Development Decision

Retain `model_v33` as the historical research champion.

Do not promote another model until its evaluation and trading evidence have been validated.

Do not treat historical model-feedback metrics as proof of real-money profitability.

### Next Model Development Stage

After Phase 3 integration validation:

- Professional historical backtesting
- Walk-forward validation
- Probability calibration
- Risk-adjusted performance evaluation
- Champion/challenger governance improvements
- Controlled model monitoring and retraining

**Status:** Research development continues. The platform is not approved for automated real-money trading.

---


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
