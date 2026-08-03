# AI Trading Research Platform — Project Memory

Last Updated:

2026-08-03

# Repository Information

Repository:

AI-Trading-Research-Platform

GitHub:

https://github.com/AnastasiyaKotelnikova/AI-Trading-Research-Platform

Local Development Path:

C:\Users\anast\scanner-project

Development Environment:

Python:

3.11.9

Virtual Environment:

venv

Operating System:

Windows PowerShell

Run modules using:

python -m app.module_name

Repository Purpose:

This repository contains the complete AI Trading Research Platform codebase.

It includes:

* market data collection

* feature engineering

* historical ML training

* scanner prediction pipeline

* AI research ranking

* decision engines

* risk evaluation

* trade management

* backtesting

* performance monitoring

* experiment documentation

The GitHub repository is the version-controlled source of truth for project history and documentation.

---

# Project Goal

The AI Trading Research Platform is an AI-assisted quantitative stock research system.

The goal is not perfect market prediction.

The goal is to create a research assistant that improves trading decisions through:

* historical evidence

* machine learning

* technical analysis

* risk evaluation

* quantitative validation

* continuous improvement

The system is designed to:

* collect market data

* generate technical features

* train ML models

* rank opportunities

* evaluate historical performance

* explain decisions

* monitor outcomes

* prepare for future paper trading

The platform is not approved for automatic real-money trading.

---

# Current Development Phase

Current Phase:

Phase 3 — AI Research Engine

Overall Progress:

Approximately 95% complete

Recent completed improvements:

✓ Research Score normalization

✓ AI Final Decision Controller

✓ Risk-aware trade management

✓ Two-path ML architecture

✓ Trade history foundation

✓ Trade feedback foundation

✓ Performance tracking foundation

Current priorities:

1. Improve validation quality

2. Improve confidence calibration

3. Reduce false positives

4. Build professional backtesting

5. Prepare paper trading infrastructure

---

# Current Architecture Overview

## Layer 1 — Data Engineering

Status:

COMPLETE ✅

Responsibilities:

* market data collection

* historical price storage

* technical feature generation

* ML dataset creation

* daily pipeline automation

Main components:

* price_history_collector.py

* feature_history_builder.py

* historical_ml_builder.py

* daily_pipeline.py

---

# Layer 2 — Machine Learning System

Status:

ACTIVE ✅

The ML system contains two separate paths.

IMPORTANT:

The two ML paths serve different purposes and must not be merged without a documented experiment.

---

# ML Path 1 — Historical ML Research Model

Purpose:

Train and evaluate historical market pattern recognition.

Training file:

app/train_model.py

Dataset:

data/historical_ml_dataset.csv

Purpose:

Predict whether historical market conditions resemble successful trade setups.

Historical features include:

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

Validation:

Chronological train/test split.

Training:

Before:

2026-05-15

Testing:

After:

2026-05-15

Purpose:

Simulate future prediction instead of random historical validation.

---

# Model v27 Retirement

Previous Champion:

model_v27

Status:

RETIRED ❌

Reported metrics:

Accuracy:

98.3%

F1:

96.1%

Reason retired:

The performance was considered unreliable.

Problems identified:

1. Training dataset was too small.

2. Possible data leakage existed.

3. Validation was not realistic enough.

4. Metrics did not represent expected market difficulty.

Decision:

model_v27 is no longer used as a benchmark.

Lesson:

High classification metrics do not automatically create a useful trading model.

---

# Current Historical ML Champion

Model:

model_v33

Status:

CURRENT CHAMPION

Storage:

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

Validation Metrics:

ROC-AUC:

0.669

F1:

0.467

Trading Backtest:

Trades:

210

Win Rate:

46.7%

Average Return:

0.448%

Champion selection considers:

* F1

* ROC-AUC

* historical return

* win rate

* reliability

Models are not accepted based only on accuracy.

---

# ML Path 2 — Scanner Prediction Model

Purpose:

Evaluate current market opportunities during scanning.

Main files:

* app/ml_predictor.py

* app/model_loader.py

Output fields:

* ML_Probability

* ML_Prediction

* ML_Model

* ML_Accuracy

* ML_F1

Used by:

* scanner pipeline

* AI ranking

* confidence scoring

* final decision logic

This path focuses on current market candidates.

It is separate from the historical research model.

---

# Layer 3 — AI Research Engine

Status:

IN PROGRESS 🚧

Purpose:

Transform technical signals and ML predictions into research decisions.

Main components:

* research_ranker.py

* ai_score_engine.py

* ai_decision.py

* ai_final_decision_controller.py

* ai_investment_analyst.py

* historical_threshold_optimizer.py

Capabilities:

✓ opportunity ranking

✓ score normalization

✓ confidence calculation

✓ historical validation

✓ decision explanations

✓ automated reports

---

# AI Decision Pipeline

Current architecture:

Market Scanner

↓

Technical Features

↓

Research Ranking

↓

AI Final Score

↓

Current Scanner ML Probability

↓

Historical ML Probability

↓

Risk Evaluation

↓

Final Conviction Score

↓

BUY / WATCH / REJECT

↓

Trade Management

---

# AI Final Decision Controller

File:

app/ai_final_decision_controller.py

Purpose:

Final research approval layer before trade planning.

Inputs:

* optimized rankings

* portfolio risk decisions

Final Conviction Score components:

Risk Component:

25%

Ranking Component:

45%

ML Confidence Component:

20%

Strategy Component:

10%

Outputs:

* BUY

* WATCH

* REJECT

---

# Trade Management System

File:

app/trade_management.py

Purpose:

Convert approved research opportunities into structured trade plans.

Implemented:

* entry price

* ATR-based stop loss

* profit targets

* position sizing

* reward/risk calculation

* expected value

* trade grading

Risk controls:

* account size

* maximum risk percentage

* allocation limits

---

# Trade Intelligence Foundation

New modules added:

* trade_history.py

* trade_history_manager.py

* trade_feedback.py

* trade_performance.py

* trade_performance_tracker.py

* trade_exit_manager.py

* live_trade_monitor.py

* ai_learning_engine.py

Purpose:

Create future capability for:

* tracking trade outcomes

* analyzing decisions

* learning from results

* improving future recommendations

Current status:

Foundation implemented.

Future work:

Connect outcomes to model monitoring and optimization.

---

# Current Data Structure

Important locations:

Models:

data/models/

Contains:

* champion_model.pkl

* model_metrics.csv

* feature_importance.csv

* model_predictions.csv

* model_monitoring.csv

Historical dataset:

data/historical_ml_dataset.csv

Research outputs:

data/results/

Analysis:

data/analysis/

Trade history:

data/trade_history.csv

---

# Current Development Priorities

## 1. Professional Validation

Develop:

* walk-forward validation

* benchmark comparison

* transaction cost simulation

* equity curves

* drawdown analysis

* Sharpe ratio

* Sortino ratio

---

## 2. Probability Calibration

Improve:

* ML probability reliability

* confidence accuracy

* false positive reduction

---

## 3. Explainable AI

Add:

* SHAP analysis

* feature contribution

* decision explanations

---

## 4. Paper Trading Preparation

Before live trading:

Required:

* longer validation

* stable performance

* monitoring

* risk controls

* execution tracking

---

# Documentation Rules

Every major change must update:

docs/AI_PROJECT_MEMORY.md

docs/MODEL_HISTORY.md

docs/EXPERIMENT_LOG.md

docs/ARCHITECTURE.md

docs/ROADMAP.md

Development principles:

✓ preserve reproducibility

✓ document experiments

✓ avoid duplicate systems

✓ avoid data leakage

✓ prefer realistic validation

✓ compare models fairly

Avoid:

✗ unrealistic accuracy

✗ overfitting

✗ curve fitting

✗ unsupported automation

---

# Final Project Philosophy

The objective is not to build a model that looks impressive.

The objective is to build a reliable AI research assistant that improves decision quality through:

* historical evidence

* machine learning

* risk analysis

* transparent scoring

* continuous improvement
