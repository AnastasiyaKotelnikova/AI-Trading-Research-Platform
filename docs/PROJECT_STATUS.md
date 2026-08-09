# AI Trading Research Platform — Project Status

Repository:

AI-Trading-Research-Platform

GitHub:

https://github.com/AnastasiyaKotelnikova/AI-Trading-Research-Platform

Local Path:

C:\Users\anast\scanner-project

Last Updated:

2026-08-08

# Project Goal

Build an AI-assisted quantitative stock research platform for personal trading research.

The system is designed to:

* collect market data
* generate technical features
* train machine learning models
* evaluate historical market patterns
* generate current-market ML predictions
* rank trading opportunities
* combine multiple research intelligence layers
* analyze risk
* generate structured trade plans
* track approved trades
* monitor open trades
* evaluate completed trades
* provide model-performance feedback
* evaluate model quality using both ML metrics and trading performance
* manage the current champion model

The platform is a quantitative research and paper-trading development system.

It is not a guaranteed market prediction system.

It is not currently approved for automated real-money trading.

Before any future live trading consideration, the platform requires additional validation including:

* extended paper trading
* walk-forward validation
* realistic transaction-cost modeling
* portfolio-level risk controls
* execution monitoring
* model monitoring
* rollback procedures
* operational reliability testing

---

# Current Overall Status

Platform Completion:

Approximately 85%

Current Development Phase:

## Phase 3 — AI Research Engine

Status:

Advanced Development 🚧

The core AI research architecture is substantially implemented.

The primary focus has now shifted from adding basic pipeline components toward:

* validation
* model governance
* professional backtesting
* confidence calibration
* portfolio intelligence
* model monitoring

The project is moving toward the milestone:

**Reliable AI Research Validation**

---

# Current Architecture Overview

The platform now consists of multiple connected intelligence layers:

```text
Market Data
        ↓
Feature Engineering
        ↓
Integrated Scanner
        ↓
Research Ranking
        ↓
Scanner ML Prediction
        ↓
Historical ML Evidence
        ↓
AI Scoring
        ↓
AI Confidence
        ↓
Risk Evaluation
        ↓
Portfolio Decision
        ↓
Trade Management
        ↓
Approved Trade
        ↓
Trade History
        ↓
Open Trade Monitoring
        ↓
Exit / Completed Trade
        ↓
Trade Performance
        ↓
Model Feedback
        ↓
Model Quality Evaluation
        ↓
Champion Management
        ↓
Current Champion
```

The architecture now contains both a forward decision path and a feedback path.

---

# Data Engineering Status

## Phase 1 — Data Engineering

Status:

COMPLETE ✅

Implemented:

✓ Market data collection

✓ Historical price storage

✓ Stock universe management

✓ Technical indicator generation

✓ Feature generation

✓ Historical feature storage

✓ ML dataset generation

✓ Historical dataset expansion

✓ Daily pipeline foundation

Main components include:

```text
price_history_collector.py
feature_history_builder.py
historical_ml_builder.py
daily_pipeline.py
```

The data-engineering layer provides the foundation for historical ML research and current-market scanning.

---

# Historical ML Dataset

Current historical dataset:

```text
data/historical_ml_dataset.csv
```

Purpose:

Train and evaluate machine-learning models using historical market behavior.

Typical features include:

* Return_5D
* Return_10D
* Return_20D
* RSI
* RSI_Change
* SMA20
* SMA50
* Above_SMA20
* Above_SMA50
* SMA_Gap
* Momentum_Acceleration
* Average_Volume
* RVOL
* Volatility_20D
* ATR
* ATR_Percent
* Range_Position
* Distance_From_52W_High
* Volume_Trend

Historical ML validation must use chronological validation.

Random splitting should not be used as the primary validation method for time-series trading research.

---

# Machine Learning Status

## Phase 2 — Machine Learning Foundation

Status:

COMPLETE ✅

Implemented:

✓ Historical ML dataset creation

✓ Feature engineering pipeline

✓ Model training

✓ Model versioning

✓ Model registry

✓ Prediction pipeline

✓ Chronological validation

✓ Historical backtesting integration

✓ Model quality evaluation

✓ Trading-performance evaluation

✓ Champion management

The ML architecture now distinguishes between:

1. historical model research
2. current scanner ML prediction
3. trading-performance evidence
4. model governance

---

# Retired Model — model_v27

Status:

RETIRED ❌

`model_v27` is permanently excluded from current model comparison and champion selection.

Previously reported metrics:

Accuracy:

98.3%

F1:

96.1%

Reason for retirement:

* insufficient dataset
* possible data leakage
* unrealistic validation
* biased historical representation
* overly optimistic classification results

Important rule:

`model_v27` must not be used as a benchmark for future model development.

Its historical metrics must not be treated as a target.

The retirement of `model_v27` is a major model-governance decision.

The project prioritizes credible validation over impressive historical classification metrics.

---

# Current Champion Model

## model_v33

Status:

CURRENT RESEARCH CHAMPION ✅

Algorithm:

Random Forest

Configuration used in the original historical acceptance experiment:

* n_estimators: 500
* max_depth: 20
* min_samples_leaf: 10
* max_features: sqrt
* class_weight: balanced

Historical acceptance experiment:

ROC-AUC:

0.669

F1:

0.467

Historical backtest:

Trades:

210

Win Rate:

46.7%

Average Return:

0.448%

These historical acceptance results are distinct from the later recorded trade-history results.

---

# Current Recorded Trading Performance

The current model feedback system records completed trades associated with `model_v33`.

Source:

```text
data/models/model_feedback_report.csv
```

Current recorded results:

Completed Trades:

272

Winning Trades:

84

Losing Trades:

188

Win Rate:

30.88%

Average Return:

2.65%

Best Trade:

70.30%

Worst Trade:

-9.96%

Stored model metrics include historical classification metrics such as:

Accuracy:

98.3%

F1:

96.1%

These stored classification metrics must not be confused with current trading performance.

The current trading evidence is more relevant to evaluating trading usefulness, but the current sample is still insufficient to establish long-term model superiority.

Therefore:

`model_v33` remains the current research champion for continued validation.

It is not a production-ready live trading model.

---

# Model Quality Evaluation

Module:

```text
app/model_quality_evaluator.py
```

Output:

```text
data/models/model_quality_report.csv
```

Recommended champion:

```text
data/models/recommended_champion.txt
```

The evaluator combines:

* F1
* Win Rate
* Average Return
* Completed Trades

Current trading-quality weighting:

* F1: 40%
* Win Rate: 30%
* Average Return: 20%
* Completed-trade evidence: 10%

Models without completed trades receive:

```text
Trading_Quality_Score = 0
```

and:

```text
Trading_Eligible = False
```

The system therefore distinguishes between:

1. predictive quality
2. trading eligibility
3. trading quality
4. champion status

A model cannot become the recommended champion solely because it has a high classification metric.

---

# Champion Management

Module:

```text
app/champion_manager.py
```

Purpose:

Compare the recommended model against the current champion and determine whether champion status should change.

Current result:

```text
Best model: model_v33
Current champion: model_v33

Champion unchanged.
```

Current champion state is therefore:

```text
model_v33
```

Champion replacement requires evidence beyond a single high ML metric.

Future replacement decisions should consider:

* realistic validation
* trading eligibility
* sufficient trading evidence
* risk
* stability
* out-of-sample performance

---

# Champion Tracking

Module:

```text
app/model_champion_tracker.py
```

Output:

```text
data/models/model_champion_status.csv
```

Current champion tracking record:

Model:

`model_v33`

Active Model:

`model_v33`

Accuracy:

approximately 55.14%

F1:

approximately 46.74%

Completed Trades:

272

Win Rate:

30.88%

Average Return:

2.65%

Status:

`CHAMPION`

This record represents the current model-governance state.

---

# ML Architecture — Two Separate Paths

The platform maintains two logically separate ML paths.

These paths must remain separated unless an architectural review determines otherwise.

---

# Historical ML Path

Purpose:

Learn from historical market behavior and provide historical evidence for current research opportunities.

Training module:

```text
app/train_model.py
```

Dataset:

```text
data/historical_ml_dataset.csv
```

Current historical research model:

```text
model_v33
```

Output:

```text
Historical_ML_Probability
```

Used for:

* historical validation
* pattern confirmation
* historical evidence
* research confidence
* AI decision support

---

# Scanner ML Path

Purpose:

Evaluate current scanner candidates.

Modules:

```text
app/ml_predictor.py
app/model_loader.py
```

Outputs include:

```text
ML_Probability
ML_Prediction
ML_Model
ML_F1
ML_Accuracy
```

Used for:

* current opportunity evaluation
* ranking support
* AI scoring
* confidence assessment

The historical ML probability and scanner ML probability represent different types of evidence and must not be treated as interchangeable.

---

# AI Research Engine Status

## Phase 3 — AI Research Engine

Status:

Advanced Development 🚧

Completion:

Approximately 95%

Completed:

✓ AI ranking engine

✓ Research score normalization

✓ Research ranking

✓ Scanner ML integration

✓ Historical ML comparison

✓ AI confidence framework

✓ AI final scoring

✓ AI decision engine

✓ AI Final Decision Controller

✓ Risk-aware approval logic

✓ Trade explanation system

✓ Automated research reports

✓ Dashboard integration

✓ Portfolio scoring foundation

✓ Trade management integration

✓ Trade feedback foundation

✓ Model feedback loop

✓ Model quality evaluator

✓ Trading eligibility filtering

✓ Recommended champion generation

✓ Champion manager

The core AI research architecture is now substantially implemented.

The next focus is validation rather than adding additional basic decision layers.

---

# AI Decision Pipeline

Current conceptual flow:

```text
Market Data
        ↓
Technical Features
        ↓
Scanner ML Prediction
        ↓
Historical ML Evidence
        ↓
Research Ranking
        ↓
AI Final Score
        ↓
AI Confidence
        ↓
Risk Evaluation
        ↓
Portfolio Decision
        ↓
Trade Management
        ↓
Final AI Decision
```

Possible AI research decisions include:

```text
HIGH CONVICTION
STRONG CANDIDATE
CANDIDATE
WATCHLIST
PASS
```

The final approval controller also produces:

```text
BUY
WATCH
REJECT
```

with confidence levels:

```text
HIGH
MEDIUM
LOW
```

The AI decision system provides explanations for decisions.

It is not a guaranteed prediction engine.

---

# AI Final Decision Controller

Module:

```text
app/ai_final_decision_controller.py
```

Purpose:

Provide the final approval layer before trade management.

Current conceptual conviction weighting:

Risk Component:

25%

Ranking Component:

45%

ML Confidence Component:

20%

Strategy Component:

10%

Final decision outputs:

* BUY
* WATCH
* REJECT

Confidence:

* HIGH
* MEDIUM
* LOW

Risk filtering remains mandatory.

---

# Risk Management Status

Implemented foundation:

✓ Risk scoring

✓ Portfolio risk filtering

✓ Position sizing

✓ Stop-loss calculation

✓ Target calculation

✓ Reward/risk analysis

✓ Expected value calculation

✓ Capital allocation

✓ Trade approval logic

Trade approval requires appropriate:

* AI approval
* portfolio approval
* risk approval

Future improvements include:

* volatility targeting
* correlation analysis
* sector exposure limits
* dynamic position sizing
* portfolio risk budgeting

---

# Trade Management Status

Module:

```text
app/trade_management.py
```

Trade plans can include:

* Entry Price
* Stop Loss
* Target 1
* Target 2
* Risk Per Share
* Recommended Shares
* Capital Allocation
* Trade Grade
* Execution Status
* Reward/Risk
* Expected Value

Position sizing considers:

* account size
* maximum risk percentage
* allocation percentage
* stop distance

Approved trades are passed into trade tracking.

---

# Trade History Status

Central trade database:

```text
data/trade_history.csv
```

The trade-history system stores:

* Trade_ID
* Symbol
* Entry_Date
* Entry_Price
* Current_Price
* Stop_Loss
* Target_1
* Target_2
* Strategy
* AI_Decision
* Final_AI_Status
* Final_AI_Reason
* Final_Conviction_Score
* Combined_ML_Probability
* ML_Probability
* AI_Confidence
* AI_Confidence_Level
* AI_Rating
* AI_Action
* Expected_Value
* Trade_Grade
* Trade_Execution_Status
* Portfolio_Action
* Portfolio_Allocation_%
* Risk_Status
* Recommended_Shares
* Capital_Allocation_$
* Model_Name
* Model_Accuracy
* Model_F1
* Status
* Exit_Date
* Exit_Price
* Return_%
* Profit_$
* Days_Held
* Outcome
* Last_Updated

---

# Trade Creation

Function:

```text
add_new_trades()
```

Only rows with:

```text
Final_AI_Status == "APPROVED TRADE"
```

are added as new trades.

The system prevents duplicate open trades for the same symbol.

Initial trade status:

```text
OPEN
```

New trades record:

* entry information
* risk levels
* AI decision information
* ML information
* model information
* portfolio allocation
* position size
* capital allocation

---

# Open Trade Monitoring

Module:

```text
app/live_trade_monitor.py
```

The monitor reads:

```text
data/analysis/final_ai_signals.csv
```

Required current-price fields include:

* Symbol
* Close

For each open trade it tracks:

* Entry Price
* Current Price
* Stop Loss
* Target 1
* Days Held

The monitor updates open trades using current scanner prices.

---

# Trade Exit Logic

Module:

```text
app/trade_history.py
```

Open trades are evaluated against:

* Stop Loss
* Target 1
* Target 2
* Maximum holding period

Maximum holding period:

30 days

Possible outcomes:

* STOP LOSS
* TARGET 1 HIT
* TARGET 2 HIT
* TIME EXIT

When a trade closes, the system records:

* Status
* Outcome
* Exit Date
* Exit Price
* Return_%
* Profit_$
* Days Held
* Last Updated

This creates the completed-trade evidence used by model feedback.

---

# Trade Performance Calculation

For a closed trade:

```text
Return_% =
(Exit_Price - Entry_Price) / Entry_Price * 100
```

Profit is calculated from:

```text
Return_% × Capital_Allocation_$
```

This creates a direct connection between trade outcomes and recorded capital allocation.

---

# Model Feedback Loop

Module:

```text
app/model_feedback_loop.py
```

Input:

```text
data/trade_history.csv
```

Output:

```text
data/models/model_feedback_report.csv
```

The feedback loop:

1. loads trade history
2. selects closed trades
3. groups completed trades by Model_Name
4. calculates trading performance
5. records model metrics
6. produces the model feedback report

Current metrics include:

* Completed Trades
* Winning Trades
* Losing Trades
* Win Rate
* Average Return
* Best Trade
* Worst Trade
* Model Accuracy
* Model F1

The feedback loop provides the foundation for outcome-based model monitoring.

It does not independently prove model profitability.

---

# Daily Pipeline Status

Controller:

```text
app/daily_pipeline.py
```

Current stages:

```text
Integrated Scanner
        ↓
Signal History
        ↓
Forward Test
        ↓
Trade Database
        ↓
AI Rankings
        ↓
AI Decisions
        ↓
AI Report
        ↓
Model Feedback Loop
        ↓
Champion Tracker
```

The daily pipeline records:

* current status
* current step
* completed steps
* failed step
* start time
* end time
* duration

Status:

```text
data/logs/pipeline_status.json
```

Log:

```text
data/logs/daily_pipeline.log
```

If a pipeline step fails, the pipeline stops and records the failed step.

Model feedback and champion tracking are now part of the normal research workflow.

---

# Current Known Limitations

## Model Validation

Still required:

* walk-forward validation
* longer out-of-sample testing
* market-regime testing
* realistic transaction-cost modeling
* benchmark comparison

---

## Probability Calibration

Still required:

* probability calibration
* confidence reliability analysis
* threshold validation
* false-positive analysis

---

## Professional Backtesting

Still required:

* equity curves
* maximum drawdown
* Sharpe ratio
* Sortino ratio
* CAGR
* transaction costs
* benchmark comparison
* realistic entry/exit assumptions

---

## Portfolio Intelligence

Still required:

* correlation analysis
* sector exposure management
* risk budgeting
* volatility targeting
* portfolio optimization
* concentration controls

---

## Model Monitoring

Still required:

* feature drift detection
* prediction drift
* rolling model performance
* model health scoring
* champion/challenger monitoring
* retraining triggers
* rollback system

---

# Current Development Priorities

## Priority 1 — Model Governance & Validation

Develop:

* larger trading samples
* rolling model evaluation
* walk-forward testing
* benchmark comparison
* model degradation detection
* champion/challenger validation

---

## Priority 2 — Professional Backtesting

Develop:

* equity curves
* maximum drawdown
* transaction costs
* benchmark comparison
* Sharpe ratio
* Sortino ratio
* CAGR
* market-regime analysis

---

## Priority 3 — Confidence Calibration

Develop:

* probability calibration
* confidence reliability scoring
* false-positive reduction
* threshold optimization

---

## Priority 4 — Portfolio Intelligence

Develop:

* correlation analysis
* sector exposure controls
* portfolio risk budgeting
* volatility targeting
* portfolio-level optimization

---

## Priority 5 — Explainable AI

Develop:

* SHAP analysis
* feature importance explanations
* clearer AI reasoning
* model decision diagnostics

---

## Priority 6 — Continuous Learning

Develop:

* rolling performance monitoring
* trade feedback integration
* model health scoring
* retraining triggers
* controlled model replacement

---

# Current Development Sequence

The current development sequence is:

```text
1. Stabilize current model governance
        ↓
2. Expand model_v33 trading evidence
        ↓
3. Build professional backtesting
        ↓
4. Implement walk-forward validation
        ↓
5. Add risk-adjusted performance metrics
        ↓
6. Improve confidence calibration
        ↓
7. Strengthen model monitoring
        ↓
8. Connect feedback to retraining decisions
        ↓
9. Begin controlled paper trading
        ↓
10. Evaluate whether live trading is justified
```

No live trading should be introduced simply because a model produces a high classification score.

---

# Development Philosophy

The platform follows quantitative research principles.

Optimize for:

✓ realistic performance

✓ reproducibility

✓ transparency

✓ controlled risk

✓ repeatable evidence

✓ continuous improvement

Avoid:

✗ unrealistic prediction accuracy

✗ overfitting

✗ data leakage

✗ curve fitting

✗ misleading metrics

✗ unsupported automation

✗ automatic champion replacement without evidence

✗ treating small trading samples as proof of profitability

The goal is not perfect market prediction.

The goal is to determine whether the complete research system can consistently improve decision quality through:

* historical evidence
* machine learning
* quantitative validation
* AI reasoning
* risk analysis
* trade outcome feedback
* controlled model evolution

---

# Documentation Requirements

Every major change must update:

```text
docs/AI_PROJECT_MEMORY.md
docs/MODEL_HISTORY.md
docs/EXPERIMENT_LOG.md
docs/ARCHITECTURE.md
docs/ROADMAP.md
docs/DEVELOPMENT_RULES.md
docs/NEXT_CHAT_START_GUIDE.md
docs/PROJECT_STATUS.md
docs/CHANGELOG.md
```

Documentation must reflect actual implementation.

Do not document planned functionality as completed.

---

# Git Workflow

Before major changes:

```powershell
git status
```

Review:

* modified files
* untracked files
* generated data changes
* unexpected files
* duplicate modules

Test changed modules individually:

```powershell
python -m app.module_name
```

Then run the relevant pipeline or evaluator.

Review generated outputs.

After documentation and code are verified:

```powershell
git add .
git commit -m "Description of change"
git push
```

---

# Current Milestone

## Reliable AI Research Validation

Status:

IN PROGRESS 🚧

The platform has progressed from:

```text
Stock Scanner
        ↓
ML Prediction System
        ↓
AI Research Engine
        ↓
Risk-Aware Research Platform
        ↓
Model Feedback & Governance
        ↓
Professional Validation
```

The next milestone is not live trading.

The next milestone is demonstrating that the current research system produces repeatable, risk-aware results through professional validation.

Success criteria:

* reproducible model evaluation
* sufficient trading sample
* realistic out-of-sample testing
* walk-forward validation
* risk-adjusted performance
* stable champion selection
* functioning feedback loop
* controlled paper-trading readiness

---

# Final Project Direction

The platform is evolving into a quantitative research assistant rather than a simple stock prediction system.

The system should answer:

* Which opportunities have historical support?
* Which current opportunities have ML confirmation?
* Which opportunities have favorable risk/reward?
* Which decisions are supported by multiple independent intelligence layers?
* How do actual trade outcomes affect model evaluation?
* Does model performance remain stable across time and market regimes?
* When should a model remain champion, be challenged, or be retired?

The ultimate objective is:

**credible evidence over impressive metrics.**

The platform should progress toward paper trading only after professional validation demonstrates that the complete research architecture is reliable, reproducible, and risk-aware.
