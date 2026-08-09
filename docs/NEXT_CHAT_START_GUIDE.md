# AI Trading Research Platform — Next Chat Start Guide

Repository:

AI-Trading-Research-Platform

GitHub:

https://github.com/AnastasiyaKotelnikova/AI-Trading-Research-Platform

Local Path:

C:\Users\anast\scanner-project

Last Updated:

2026-08-08

---

# How to Continue Work in a New Chat

Before making recommendations, architecture changes, or code modifications:

Read these documents first:

```text
docs/AI_PROJECT_MEMORY.md

docs/MODEL_HISTORY.md

docs/EXPERIMENT_LOG.md

docs/ARCHITECTURE.md

docs/ROADMAP.md

docs/DEVELOPMENT_RULES.md

docs/CHANGELOG.md

docs/PROJECT_STATUS.md

docs/NEXT_CHAT_START_GUIDE.md
```

These documents contain:

* current project status
* completed phases
* architecture decisions
* model history
* experiment history
* development rules
* roadmap
* recent changes
* current validation priorities
* model governance decisions

These documents are the project source of truth.

Do not assume that older chat instructions or older documentation represent the current architecture.

---

# Current Project State

Project:

AI Trading Research Platform

Purpose:

Build an AI-assisted quantitative stock research and paper-trading development system.

The platform is designed to:

* collect market data
* generate technical features
* train machine learning models
* generate current-market ML predictions
* evaluate historical market patterns
* rank trading opportunities
* combine multiple intelligence layers
* evaluate risk
* generate structured trade plans
* track approved trades
* monitor open trades
* calculate completed trade outcomes
* evaluate model performance using trading outcomes
* manage the current champion model
* support continuous model evaluation

The platform is a quantitative research and paper-trading development system.

It is not approved for automated real-money trading.

---

# Current Overall Status

Platform Completion:

Approximately 85%

Current Development Phase:

## Phase 3 — AI Research Engine

Status:

Advanced Development 🚧

Phase 3 is substantially implemented.

The project is now moving from basic architecture construction toward validation and reliability.

The primary objective is no longer simply adding more AI layers.

The next objective is determining whether the existing research system produces reliable and repeatable results.

---

# Current Development Direction

The platform has evolved through:

```text
Stock Scanner

↓

ML Prediction System

↓

AI Research Engine

↓

Risk-Aware Research Platform

↓

Outcome-Based Model Feedback System

↓

Professional Validation
```

The next major milestone is:

**Reliable AI Research Validation**

The immediate focus is:

1. stabilize model governance
2. expand trading evidence
3. build professional backtesting
4. implement walk-forward validation
5. add risk-adjusted performance metrics
6. improve confidence calibration
7. strengthen model monitoring
8. connect feedback to retraining decisions
9. prepare for controlled paper trading

Do not skip directly to live trading.

---

# Development Environment

Local project:

```text
C:\Users\anast\scanner-project
```

Python:

```text
Python 3.11.9
```

Environment:

```text
venv
```

Typical module execution:

```powershell
python -m app.module_name
```

Example:

```powershell
python -m app.train_model
```

Git repository:

```text
AI-Trading-Research-Platform
```

---

# Current Architecture

The platform contains multiple connected intelligence layers.

Current conceptual architecture:

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

Trade Exit / Completed Outcome

↓

Trade Performance

↓

Model Feedback

↓

Model Quality Evaluation

↓

Champion Manager

↓

Current Champion

↓

Future Model Evaluation
```

The architecture is now a feedback-oriented research system rather than a simple forward prediction pipeline.

---

# Two Separate ML Paths

The platform maintains two separate ML paths.

These paths must remain logically separated.

Do not merge them without architectural review.

---

# ML Path 1 — Historical ML

Purpose:

Train and evaluate machine-learning models using historical market behavior.

Primary training module:

```text
app/train_model.py
```

Historical dataset:

```text
data/historical_ml_dataset.csv
```

Historical ML is used for:

* model development
* historical pattern research
* chronological validation
* historical backtesting
* model comparison
* historical evidence

Typical historical features include:

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

Historical model output:

```text
Historical_ML_Probability
```

The historical ML path must use realistic chronological validation.

---

# ML Path 2 — Scanner ML

Purpose:

Evaluate current market opportunities.

Primary modules:

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

Scanner ML is used for:

* current opportunity evaluation
* scanner ranking
* AI scoring
* confidence assessment
* current-market ML confirmation

Scanner ML probability and Historical ML Probability must not automatically be interpreted as identical evidence.

---

# Model Governance

Model governance is now separate from model training.

Relevant modules include:

```text
app/model_registry.py

app/model_quality_evaluator.py

app/champion_manager.py

app/model_champion_tracker.py

app/model_feedback_loop.py
```

Model selection must consider both:

* predictive quality
* trading evidence

High classification metrics alone are insufficient.

---

# Retired Model — model_v27

Status:

```text
RETIRED
```

model_v27 is permanently excluded from current model comparison and champion selection.

Previously reported metrics:

```text
Accuracy: 98.3%

F1: 96.1%
```

These results were later considered unreliable because of concerns including:

* insufficient dataset size
* possible data leakage
* unrealistic validation
* biased historical representation
* overly optimistic classification results

Important rule:

```text
model_v27 must not be used as a benchmark.
```

Do not:

* restore model_v27
* compare future models against its 98.3% accuracy
* use its F1 of 96.1% as a target
* allow its metrics to influence champion selection

The retirement of model_v27 is an important architecture and governance decision.

---

# Current Champion — model_v33

Current champion:

```text
model_v33
```

Champion file:

```text
data/models/champion_model.pkl
```

Current champion manager result:

```text
Best model: model_v33
Current champion: model_v33
Champion unchanged
```

Algorithm:

```text
Random Forest
```

Original historical acceptance experiment:

```text
n_estimators: 500
max_depth: 20
min_samples_leaf: 10
max_features: sqrt
class_weight: balanced
```

Historical evaluation:

```text
ROC-AUC: 0.669

F1: 0.467
```

Historical backtest:

```text
Trades: 210

Win Rate: 46.7%

Average Return: 0.448%
```

These values represent the historical experiment used when model_v33 was initially accepted.

They must not be confused with the later recorded trade-history results.

---

# Current Recorded Trading Evidence — model_v33

Current model feedback report:

```text
data/models/model_feedback_report.csv
```

Current recorded completed-trade results:

```text
Completed Trades: 272

Winning Trades: 84

Losing Trades: 188

Win Rate: 30.88%

Average Return: 2.65%

Best Trade: 70.30%

Worst Trade: -9.96%
```

Stored historical model metrics may also appear in the feedback report:

```text
Accuracy: 98.3%

F1: 96.1%
```

These stored classification metrics are historical model metadata and must remain separate from current trading outcomes.

The current trading results are more relevant when evaluating practical trading usefulness.

However, the current sample is still insufficient to establish long-term strategy superiority.

model_v33 therefore remains the:

```text
Current Research Champion
```

not a production-ready trading model.

---

# Model Quality Evaluation

Primary module:

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

The current evaluation considers:

* F1
* Win Rate
* Average Return
* Completed Trades

Trading Quality Score:

```text
Trading_Quality_Score
```

Trading eligibility requires:

```text
Completed_Trades > 0
```

Models without completed trading history:

```text
Trading_Eligible = False
```

They may remain in the registry for research but cannot automatically become the recommended trading champion.

The architecture therefore distinguishes:

1. predictive quality
2. trading eligibility
3. trading quality
4. champion status

---

# Champion Management

Primary module:

```text
app/champion_manager.py
```

Purpose:

Compare the recommended model with the current champion.

Current state:

```text
Best model: model_v33
Current champion: model_v33
Champion unchanged
```

Future champion replacement must require:

* realistic validation
* no evidence of leakage
* trading eligibility
* meaningful trading performance
* acceptable risk
* sufficient stability
* sufficient evidence

A single high F1 score must never be sufficient for champion replacement.

---

# Champion Tracking

Primary module:

```text
app/model_champion_tracker.py
```

Output:

```text
data/models/model_champion_status.csv
```

Current champion:

```text
model_v33
```

Recorded current tracking information includes approximately:

```text
Accuracy: 55.14%

F1: 46.74%

Completed Trades: 272

Win Rate: 30.88%

Average Return: 2.65%

Status: CHAMPION
```

Champion tracking represents the current governance state.

It must be distinguished from older historical model experiments.

---

# AI Research Engine

Phase:

```text
Phase 3 — AI Research Engine
```

Status:

```text
Advanced Development
```

The research engine includes:

```text
app/research_ranker.py

app/ai_score_engine.py

app/ai_decision.py

app/ai_final_decision_controller.py
```

Responsibilities include:

* opportunity ranking
* technical signal interpretation
* ML confirmation
* historical evidence integration
* confidence evaluation
* risk-aware decision support
* decision explanation

---

# AI Decision Outputs

Current decision levels include:

```text
HIGH CONVICTION
STRONG CANDIDATE
CANDIDATE
WATCHLIST
PASS
```

The final decision controller can produce:

```text
BUY
WATCH
REJECT
```

Confidence levels:

```text
HIGH
MEDIUM
LOW
```

The system generates decision explanations where applicable.

AI confidence must never be treated as certainty.

---

# AI Final Decision Controller

Module:

```text
app/ai_final_decision_controller.py
```

The final conviction score combines:

```text
Risk Component: 25%

Ranking Component: 45%

ML Confidence Component: 20%

Strategy Component: 10%
```

The controller provides the final research approval layer before trade management.

It considers:

* ranking quality
* ML confidence
* historical evidence
* portfolio risk
* strategy information

---

# Trade Management

Primary module:

```text
app/trade_management.py
```

Trade management converts approved research opportunities into structured trade plans.

It can calculate:

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

Risk approval remains mandatory.

---

# Trade History

Primary module:

```text
app/trade_history.py
```

Database:

```text
data/trade_history.csv
```

Trade history is the central recorded-trade database.

It stores information including:

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

Duplicate open trades for the same symbol are prevented.

New trades record:

* entry information
* risk levels
* AI decision information
* ML information
* model information
* portfolio allocation
* position size
* capital allocation

Initial status:

```text
OPEN
```

---

# Open Trade Monitoring

Module:

```text
app/live_trade_monitor.py
```

Input:

```text
data/analysis/final_ai_signals.csv
```

Required current-price fields include:

```text
Symbol
Close
```

The monitor reads trade history and identifies currently open positions.

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

```text
30 days
```

Possible outcomes:

```text
STOP LOSS

TARGET 1 HIT

TARGET 2 HIT

TIME EXIT
```

When a trade closes, the system records:

* Status
* Outcome
* Exit Date
* Exit Price
* Return_%
* Profit_$
* Days Held
* Last Updated

---

# Trade Performance

For a closed trade:

```text
Return_% =
(Exit_Price - Entry_Price) / Entry_Price * 100
```

Profit is calculated using:

```text
Return_% × Capital_Allocation_$
```

This creates a direct connection between recorded trade outcomes and allocated capital.

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

Purpose:

Evaluate model performance using completed recorded trades.

The feedback loop:

1. loads trade history
2. selects closed trades
3. groups trades by Model_Name
4. calculates trading performance
5. records model metrics
6. generates the model feedback report

Current feedback includes:

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

It must not automatically retrain or replace models without explicit governance rules.

---

# Daily Pipeline

Main controller:

```text
app/daily_pipeline.py
```

Current sequence:

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

The pipeline records:

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

Model feedback and champion tracking are now part of the normal downstream research workflow.

---

# Current Development Priorities

The next development sequence is:

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

Do not skip validation stages.

---

# Phase 4 — Professional Backtesting

Status:

```text
Early Development
```

Priority:

```text
HIGH
```

Required capabilities:

* walk-forward validation
* benchmark comparison against SPY/QQQ
* transaction-cost simulation
* equity curves
* maximum drawdown
* Sharpe ratio
* Sortino ratio
* CAGR
* market-regime testing
* position-sizing validation
* realistic entry/exit assumptions

The purpose is to determine whether the complete research strategy remains useful under realistic historical conditions.

---

# Phase 5 — Portfolio Intelligence

Future capabilities:

* correlation analysis
* sector exposure limits
* risk budgeting
* volatility targeting
* portfolio optimization
* multi-strategy allocation
* portfolio-level drawdown controls
* concentration controls

---

# Phase 6 — Model Monitoring

Planned capabilities:

* feature drift detection
* prediction drift
* rolling performance
* model health scoring
* champion/challenger monitoring
* automatic retraining triggers
* model rollback
* monitoring dashboard

The existing trade-feedback architecture provides the foundation for this phase.

---

# Phase 7 — Paper Trading

Paper trading must begin only after sufficient validation.

Required before paper trading:

* professional backtesting
* walk-forward validation
* sufficient model-performance history
* stable risk controls
* validated trade management
* reliable monitoring
* functioning model feedback

Paper trading must remain separate from real-money execution.

---

# Phase 8 — Optional Live Trading

Live trading is a future possibility only.

Before considering it, the system would require:

* extensive backtesting
* successful paper trading
* stable model performance
* validated risk controls
* emergency shutdown procedures
* execution monitoring
* model monitoring
* operational reliability

The current platform is not approved for automated real-money trading.

---

# Important Development Rules

Before changing code:

1. Read the current documentation.
2. Inspect existing related modules.
3. Search for duplicate functionality.
4. Identify existing inputs and outputs.
5. Preserve the current architecture unless a change is justified.
6. Define how the change will be validated.
7. Document material changes.

Do not redesign the platform unnecessarily.

Do not create competing data sources.

Do not create duplicate feedback, performance, model-management, or monitoring systems.

---

# ML Experiment Rules

Every significant ML experiment must record:

* dataset
* date range
* dataset size
* feature set
* algorithm
* hyperparameters
* training date
* validation method
* Accuracy
* Precision
* Recall
* F1
* ROC-AUC
* trading performance
* decision
* next action

Update:

```text
docs/MODEL_HISTORY.md
docs/EXPERIMENT_LOG.md
```

If the experiment changes architecture, also update:

```text
docs/ARCHITECTURE.md
```

---

# Dataset Rules

Never silently replace a research dataset.

Dataset changes must record:

* source
* date range
* number of stocks
* number of rows
* features
* generation method

Changes to:

```text
data/historical_ml_dataset.csv
```

must be treated as meaningful research changes.

Dataset expansion or regeneration must be documented before comparing resulting models with previous versions.

---

# Model Governance Rules

A new model must not become champion simply because it has:

* higher Accuracy
* higher F1
* higher ROC-AUC
* better training results

The model must demonstrate:

* realistic validation
* no evidence of leakage
* trading eligibility
* meaningful trading performance
* acceptable risk
* sufficient stability

Current eligibility:

```text
Completed_Trades > 0
```

Future eligibility may become stricter as the trading sample grows.

---

# Risk Rules

No trade should become approved solely because of:

* high ML probability
* high ranking score
* high historical probability
* high AI confidence

Risk evaluation remains mandatory.

Trade decisions should consider:

* stop loss
* position size
* reward/risk
* expected value
* portfolio exposure
* allocation limits

---

# Testing Rules

Before accepting major changes, run the relevant tests.

Depending on the change, validate:

* training
* scanner
* AI decision
* backtesting
* validation
* trade feedback
* model quality evaluation
* champion manager

For model changes verify:

* dataset
* feature set
* metrics
* trading performance
* output files
* model version
* champion status

Record significant experiment results.

---

# Documentation Rules

After major changes update the relevant documentation.

Core documentation:

```text
docs/AI_PROJECT_MEMORY.md

docs/MODEL_HISTORY.md

docs/EXPERIMENT_LOG.md

docs/ARCHITECTURE.md

docs/ROADMAP.md

docs/DEVELOPMENT_RULES.md

docs/CHANGELOG.md

docs/PROJECT_STATUS.md

docs/NEXT_CHAT_START_GUIDE.md
```

Documentation must reflect the actual current code.

Do not document planned functionality as completed.

---

# Git Workflow

Work from:

```text
C:\Users\anast\scanner-project
```

Before changes:

```powershell
git status
```

Review:

* modified files
* untracked files
* generated data
* unexpected changes
* duplicate modules

After testing:

```powershell
git add .
git commit -m "Description of meaningful change"
git push
```

Good commit examples:

```text
Improve professional backtesting validation

Add walk-forward model evaluation

Improve confidence calibration

Add model drift monitoring

Improve champion governance
```

Avoid vague commits such as:

```text
update
changes
test
stuff
```

---

# Before Coding

Before writing or modifying code:

1. Read the current documentation.
2. Confirm the current architecture.
3. Check related modules.
4. Search for duplicate functionality.
5. Identify existing data sources.
6. Identify existing outputs.
7. Determine the validation method.
8. Determine which documentation must change.

Do not start coding before understanding how the new functionality fits into the existing system.

---

# After Coding

Always:

1. Run the changed module.
2. Run relevant tests.
3. Review generated outputs.
4. Check for unintended changes.
5. Evaluate whether the result is actually an improvement.
6. Update experiment documentation.
7. Update architecture documentation if necessary.
8. Update roadmap/status documentation if necessary.
9. Commit the changes.
10. Push to GitHub.

---

# Current Recommended Next Task

The highest-priority next development task is:

## Professional Backtesting

Do not immediately add another AI layer.

The existing architecture is sufficiently developed to begin serious validation.

The next work should focus on:

```text
Walk-Forward Validation

↓

Benchmark Comparison

↓

Transaction Costs

↓

Equity Curve

↓

Maximum Drawdown

↓

Sharpe Ratio

↓

Sortino Ratio

↓

CAGR

↓

Market Regime Analysis

↓

Position Sizing Validation
```

This should establish whether the existing research system has meaningful historical robustness.

---

# Professional Validation Standard

Backtesting must avoid:

* look-ahead bias
* future information leakage
* survivorship bias where applicable
* unrealistic execution assumptions
* unrealistic transaction costs
* inappropriate random splitting
* excessive parameter optimization
* using future information to determine historical decisions

A profitable backtest alone does not prove that the strategy is ready for live trading.

---

# Current Milestone

## Reliable AI Research Validation

Status:

```text
IN PROGRESS
```

Success criteria:

* reproducible model evaluation
* sufficient trading sample
* realistic out-of-sample testing
* walk-forward validation
* risk-adjusted performance
* stable champion selection
* functioning feedback loop
* controlled paper-trading readiness

The next milestone is not live trading.

The next milestone is proving that the research system produces repeatable, risk-aware results through professional validation.

---

# New Chat Opening Message

Copy this into a new chat:

```text
I am continuing my AI Trading Research Platform project.

First read these documents:

docs/AI_PROJECT_MEMORY.md
docs/MODEL_HISTORY.md
docs/EXPERIMENT_LOG.md
docs/ARCHITECTURE.md
docs/ROADMAP.md
docs/DEVELOPMENT_RULES.md
docs/CHANGELOG.md
docs/PROJECT_STATUS.md
docs/NEXT_CHAT_START_GUIDE.md

Use these documents as the source of truth.

Repository:

AI-Trading-Research-Platform

Local path:

C:\Users\anast\scanner-project

Current platform completion:

Approximately 85%

Current phase:

Phase 3 — AI Research Engine

Current major milestone:

Reliable AI Research Validation

Important model governance:

model_v27 is permanently retired and must never be used as a benchmark.

Current research champion:

model_v33

model_v33 remains the current research champion, not a production-ready trading model.

Current recorded model_v33 trading evidence:

272 completed trades
30.88% win rate
2.65% average return
70.30% best trade
-9.96% worst trade

The platform has two separate ML paths:

1. Historical ML Probability
2. Scanner ML Probability

Do not merge these paths without architectural review.

The platform now includes:

- market data pipeline
- feature engineering
- historical ML
- scanner ML
- research ranking
- AI scoring
- AI confidence
- AI decision engine
- risk evaluation
- trade management
- trade history
- open-trade monitoring
- automated trade exits
- trade performance
- model feedback
- model quality evaluation
- champion management
- daily pipeline status tracking

The next major development priority is professional validation.

Focus next on:

1. professional backtesting
2. walk-forward validation
3. benchmark comparison
4. transaction-cost modeling
5. equity curves
6. maximum drawdown
7. Sharpe ratio
8. Sortino ratio
9. CAGR
10. market-regime analysis
11. confidence calibration
12. model monitoring

Do not redesign the architecture unless necessary.

Do not create duplicate modules or competing systems.

Do not optimize only for classification accuracy.

Do not use model_v27 as a benchmark.

Do not move to live trading without professional validation and controlled paper trading.
```
