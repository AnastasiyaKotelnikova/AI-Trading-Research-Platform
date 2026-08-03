# AI Trading Research Platform — Architecture & Development Update

Last Updated:

2026-08-03

# Purpose

This document records the latest architecture changes and development decisions for the AI Trading Research Platform.

The platform is an AI-assisted quantitative stock research system designed to:

* collect market data
* generate technical features
* train machine learning models
* rank trading opportunities
* evaluate historical performance
* combine ML probability with research scoring
* apply risk management
* generate explainable AI decisions

The platform is a research system.

It is not approved for automated real-money trading.

Future live trading requires:

* extended paper trading
* walk-forward validation
* risk controls
* execution monitoring

---

# Major Architecture Update

The platform now contains two separate ML paths.

This separation was introduced because the system performs two different tasks:

1. Historical research validation
2. Current market scanning and opportunity ranking

The two ML systems must not be confused.

---

# ML Path 1 — Historical ML Prediction System

Purpose:

Train and evaluate models using historical market data.

Main file:

app/train_model.py

Dataset:

data/historical_ml_dataset.csv

Features include:

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

Training process:

* chronological train/test split
* future leakage prevention
* model comparison
* backtesting
* champion evaluation

Evaluation metrics:

Required:

* Accuracy
* Precision
* Recall
* F1
* ROC-AUC

Trading evaluation:

* number of trades
* win rate
* average return
* risk metrics

---

# Model v27 Decision

Previous champion:

model_v27

Status:

RETIRED

Reason:

model_v27 is no longer considered a reliable benchmark.

Problems identified:

* smaller training dataset
* possible data leakage
* unrealistic validation results
* biased historical representation
* overly optimistic accuracy metrics

Reported old metrics:

Accuracy:

98.3%

F1:

96.1%

Decision:

Remove model_v27 from champion comparison.

Future models must be evaluated using realistic validation and trading performance.

Important lesson:

High classification metrics do not automatically produce a useful trading model.

---

# Current Historical ML Model

Current accepted model:

model_v33

Saved as:

data/models/champion_model.pkl

Algorithm:

Random Forest

Configuration:

* n_estimators: 500
* max_depth: 20
* min_samples_leaf: 10
* max_features: sqrt
* class_weight: balanced

Dataset:

Expanded historical ML dataset

Validation:

Chronological split:

Training:

Before 2026-05-15

Testing:

After 2026-05-15

Metrics:

ROC-AUC:

0.669

F1:

0.467

Backtest:

Trades:

210

Win Rate:

46.7%

Average Return:

0.448%

Acceptance decision:

model_v33 replaced previous unreliable models because it demonstrated more realistic performance.

---

# ML Path 2 — Scanner ML Prediction System

Purpose:

Provide current market scanner predictions.

Main file:

app/ml_predictor.py

This path operates on current scanner candidates.

It uses:

* current technical ranking
* momentum features
* trend features
* risk/reward features

Scanner features include:

* RSI
* Return_5D
* Return_20D
* Distance_From_High_%
* Above_SMA20
* Above_SMA50
* Breakout
* Overextended
* Rank_Score
* Momentum_Score
* Trend_Score
* Relative_Strength
* Risk_Reward

Output:

* ML_Probability
* ML_Prediction
* ML_Model
* ML_F1
* ML_Accuracy

This path is used by the live research pipeline.

---

# Historical ML Integration

Historical ML predictions are loaded separately.

Function:

add_historical_ml_predictions()

Output:

Historical_ML_Probability

Purpose:

Compare current opportunities with historical patterns.

The system now combines:

* current scanner ML probability
* historical ML probability

This creates a more complete research signal.

---

# Model Registry Update

File:

app/model_registry.py

Purpose:

Automatically compare new models against the current champion.

Champion selection uses:

* F1 score
* ROC-AUC
* Average Return
* Win Rate

The platform no longer accepts models only because of:

* accuracy
* training score
* unrealistic validation

A model must demonstrate:

* realistic performance
* stability
* trading usefulness

---

# AI Decision Pipeline Update

The AI decision pipeline now contains multiple intelligence layers.

Flow:

Market Data

↓

Technical Features

↓

Research Ranking

↓

ML Predictions

↓

AI Final Score

↓

Risk Evaluation

↓

Portfolio Decision

↓

Trade Management

↓

Final AI Decision

---

# AI Decision Engine

File:

app/ai_decision.py

Purpose:

Create AI research decisions using:

* AI Final Score
* AI Confidence
* ML Probability
* Historical ML Probability
* Risk Reward
* Market Regime

Possible outputs:

* HIGH CONVICTION
* STRONG CANDIDATE
* CANDIDATE
* WATCHLIST
* PASS

The engine also generates explanations.

Example:

* Strong technical ranking
* Strong current ML confirmation
* Historical patterns support setup
* Positive risk/reward

---

# AI Final Decision Controller

File:

app/ai_final_decision_controller.py

Purpose:

Final approval layer before trade management.

Inputs:

* optimized rankings
* portfolio risk decisions

Calculates:

Final Conviction Score

Components:

Risk Component:

25%

Ranking Component:

45%

ML Confidence Component:

20%

Strategy Component:

10%

Final outputs:

* BUY
* WATCH
* REJECT

Confidence:

* HIGH
* MEDIUM
* LOW

---

# Trade Management Update

File:

app/trade_management.py

Purpose:

Convert approved research opportunities into structured trade plans.

Adds:

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

Trades are blocked unless approval conditions are met.

Required approvals:

* Approved Trade status
* Portfolio allows entry
* Risk approved
* Portfolio approval flag

---

# Risk Management Direction

Risk management is now integrated into final decision making.

The system evaluates:

* portfolio risk
* position sizing
* trade approval
* downside protection

Future improvements:

* volatility targeting
* correlation analysis
* sector exposure limits
* dynamic position sizing

---

# Documentation Updates Required

After major changes update:

docs/AI_PROJECT_MEMORY.md

docs/MODEL_HISTORY.md

docs/EXPERIMENT_LOG.md

docs/ARCHITECTURE.md

docs/ROADMAP.md

docs/DEVELOPMENT_RULES.md

---

# Current Development Priority

Phase 3 — AI Research Engine

Current focus:

1. AI Final Score optimization

2. Confidence calibration

3. Historical score validation

4. False positive reduction

5. Walk-forward validation

6. Professional backtesting

---

# Development Philosophy

The system optimizes for:

* realistic performance
* repeatability
* risk control
* transparent decisions
* reproducible experiments

Avoid:

* unrealistic accuracy
* data leakage
* overfitting
* curve fitting

The goal is not perfect prediction.

The goal is an AI research assistant that improves trading decisions through:

* historical evidence
* machine learning
* quantitative validation
* risk analysis
* continuous improvement


# Experiment Log Updates

## EXP-015 — Two ML Path Architecture Separation

Date:

2026-08-03

Objective:

Separate historical ML research predictions from current scanner ML predictions.

Problem:

The previous architecture mixed two different ML purposes:

* historical market research
* current candidate scanning

This created confusion about:

* which model was active
* which features were expected
* how predictions should be interpreted

Changes:

Created two distinct ML paths.

Historical ML Path:

Purpose:

Historical validation and model research.

Files:

* app/train_model.py
* app/historical_model_loader.py

Dataset:

data/historical_ml_dataset.csv

Output:

Historical_ML_Probability

Scanner ML Path:

Purpose:

Current opportunity evaluation.

Files:

* app/ml_predictor.py
* app/model_loader.py

Output:

* ML_Probability
* ML_Prediction
* ML_Model

Result:

The architecture now clearly separates:

Historical evidence

from

Current market prediction.

Decision:

Accepted.

Future development must maintain this separation.

---

# EXP-016 — Model v27 Retirement Documentation Update

Date:

2026-08-03

Objective:

Clarify model history and prevent reuse of unreliable metrics.

Finding:

model_v27 produced exceptional metrics:

Accuracy:

98.3%

F1:

96.1%

However, investigation identified:

* insufficient dataset size
* possible leakage
* unrealistic validation
* poor representation of future market conditions

Decision:

model_v27 permanently retired.

Replacement:

model_v33

Lesson:

Trading ML models must be evaluated by:

* realistic validation
* trading performance
* stability

not only classification metrics.

Status:

Completed.

---

# EXP-017 — AI Decision Pipeline Integration

Date:

2026-08-03

Objective:

Improve final trade evaluation by combining research, ML, and risk layers.

Updated components:

* app/ai_decision.py
* app/ai_final_decision_controller.py
* app/trade_management.py

New decision flow:

Technical Ranking

↓

Research Score

↓

ML Probability

↓

Historical ML Probability

↓

AI Confidence

↓

Risk Evaluation

↓

Final Conviction Score

↓

Trade Management

Result:

The platform moved from simple signal generation toward multi-layer decision research.

Decision:

Accepted.

---

# EXP-018 — Risk-Aware Trade Management

Date:

2026-08-03

Objective:

Add structured trade planning after AI approval.

Implemented:

Entry calculation

Stop loss calculation using ATR:

Entry - ATR × multiplier

Profit targets:

Target 1

Target 2

Position sizing:

Based on:

* account size
* maximum risk percentage
* allocation percentage

Added outputs:

* Trade Grade
* Execution Status
* Reward/Risk
* Expected Value

Decision:

Accepted.

Future improvements:

* dynamic risk sizing
* portfolio constraints
* volatility adjustment

---

# Model History Update

## Current Model Architecture

The platform now maintains two separate model roles.

# Historical Research Model

Purpose:

Research and validation.

Current model:

model_v33

File:

data/models/champion_model.pkl

Algorithm:

Random Forest

Evaluation:

* F1
* ROC-AUC
* Backtest Return
* Win Rate

Status:

Accepted Champion.

---

# Scanner Prediction Model

Purpose:

Current market candidate scoring.

Loaded through:

app/model_loader.py

Used by:

app/ml_predictor.py

Outputs:

ML_Probability

This prediction is combined with:

* Research Score
* AI Confidence
* Risk analysis

Status:

Active research component.

---

# Model Governance Rules

Every future model must record:

Dataset:

* file
* size
* date range
* features

Training:

* algorithm
* parameters
* training date

Evaluation:

* Accuracy
* Precision
* Recall
* F1
* ROC-AUC

Trading:

* trades
* win rate
* return
* drawdown
* risk metrics

Decision:

One of:

* Accepted
* Rejected
* Retired

Reason must be documented.

---

# Architecture Update

## Complete AI Research Pipeline

Current architecture:

## Layer 1 — Data Engineering

Responsibilities:

* market data collection
* historical storage
* feature generation

Status:

Complete.

---

## Layer 2 — Machine Learning

Responsibilities:

Historical:

* model training
* validation
* backtesting

Scanner:

* probability prediction
* candidate scoring

Status:

Complete foundation.

---

## Layer 3 — Research Intelligence

Components:

* research_ranker.py
* ai_score_engine.py
* ai_decision.py
* ai_final_decision_controller.py

Responsibilities:

* opportunity ranking
* confidence evaluation
* decision explanation

Status:

Active development.

---

## Layer 4 — Risk Intelligence

Responsibilities:

* portfolio filtering
* risk approval
* position sizing

Components:

* trade_management.py
* portfolio risk modules

Status:

Developing.

---

## Layer 5 — Execution Research

Responsibilities:

* trade tracking
* feedback
* performance learning

New modules:

* trade_history.py
* trade_feedback.py
* trade_performance_tracker.py
* live_trade_monitor.py

Status:

Early development.

---

# Roadmap Update

## Phase 3 — AI Research Engine

Previous:

Approximately 92% complete

Updated:

Approximately 95% complete

Completed additions:

✓ Two ML path separation

✓ AI decision integration

✓ Risk-aware trade management

✓ Trade execution preparation

✓ Feedback architecture foundation

Remaining:

* confidence calibration
* false positive reduction
* SHAP explainability
* historical validation improvement

---

# Phase 4 — Professional Backtesting

Priority increased.

Required:

* walk-forward validation
* benchmark comparison
* transaction cost simulation
* equity curves
* maximum drawdown
* Sharpe ratio
* Sortino ratio
* CAGR

Reason:

Before any paper trading, performance must be validated under realistic conditions.

---

# Phase 5 — Portfolio Intelligence

Future improvements:

* correlation analysis
* sector limits
* portfolio optimization
* risk budgeting

---

# Phase 6 — Model Monitoring

Planned:

* feature drift detection
* prediction drift
* model health scoring
* automatic retraining triggers
* rollback system

---

# Development Rules Update

Before changing ML:

Always check:

* MODEL_HISTORY.md
* EXPERIMENT_LOG.md
* ARCHITECTURE.md

Never:

* compare against model_v27
* optimize only for accuracy
* accept unrealistic metrics

---

# Coding Rules

New modules must:

* have one clear purpose
* avoid duplicate functionality
* include documentation
* connect to existing architecture

Before commit:

Run:

git status

Test:

python -m app.module_name

Update documentation.

Commit:

git add .

git commit -m "Description of change"

Push:

git push

---

# Current Git Development State

Recent commits:

d765bfe

Fix AI decision pipeline risk management and trade execution logic

aef7a0c

Align trade management with research EV and execution pipeline

5246f2b

Align execution engine with AI decision pipeline

f1f4f0f

Align AI decision pipeline, trade management, and scoring engines

447066f

Research Ranker V3: normalize Research Score

---

# Current Uncommitted Development

Modified:

* app/ai_decision.py
* app/backtester.py
* app/config.py
* app/html_report.py
* app/ml_predictor.py
* app/model_loader.py
* app/performance_metrics.py
* app/trade_management.py
* data/models/model_monitoring.csv
* data/models/model_predictions.csv

New modules:

* app/ai_learning_engine.py
* app/daily_ai_pipeline.py
* app/live_trade_monitor.py
* app/trade_exit_manager.py
* app/trade_feedback.py
* app/trade_history.py
* app/trade_history_manager.py
* app/trade_performance.py
* app/trade_performance_tracker.py

These should be documented before the next milestone commit.

---

# Current Project State Summary

The platform has evolved from:

Stock Scanner

↓

ML Prediction System

↓

AI Research Engine

↓

Risk-Aware Trading Research Platform

Current strengths:

✓ Data pipeline

✓ Historical ML foundation

✓ Model registry

✓ Research ranking

✓ AI scoring

✓ Decision explanation

✓ Risk-aware trade planning

✓ Trade feedback foundation

Next major milestone:

Complete professional validation before paper trading.

---

# Final Development Principle

The system should behave like a quantitative research platform.

Success is measured by:

* realistic validation

* repeatable experiments

* controlled risk

* transparent decisions

* continuous improvement

The objective is not perfect prediction.

The objective is better decision quality supported by data and evidence.

