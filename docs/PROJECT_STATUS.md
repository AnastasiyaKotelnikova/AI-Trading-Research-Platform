# AI Trading Research Platform — Project Status


Repository:

AI-Trading-Research-Platform


GitHub:

https://github.com/AnastasiyaKotelnikova/AI-Trading-Research-Platform


Local Path:

C:\Users\anast\scanner-project



Last Updated:

2026-08-03



# Project Goal


Build an AI-assisted quantitative stock research platform for personal trading research.



The system is designed to:


- collect market data

- generate technical features

- train machine learning models

- evaluate historical patterns

- rank trading opportunities

- analyze risk

- generate AI decisions

- manage trade simulations

- learn from performance feedback



The platform is a research and decision-support system.


It is not a guaranteed market prediction system.



---


# Current Overall Status


Platform Completion:


Approximately 75%



Current Development Phase:


## Phase 3 — AI Research Engine


Status:


Advanced / Near Completion 🚧



Main objective:


Transform the platform from a stock scanner into a quantitative AI research decision system.



---


# Current Architecture Overview


The platform now consists of multiple intelligence layers:



```
Market Data

↓

Feature Engineering

↓

Historical ML Analysis

+

Scanner ML Analysis

↓

Research Ranking Engine

↓

AI Final Scoring

↓

Risk Evaluation

↓

AI Decision Controller

↓

Trade Management

↓

Performance Tracking

↓

Feedback Learning
```



---


# Data Engineering Status


## Phase 1 — Data Engineering


Status:


COMPLETE ✅



Implemented:


✓ Market data collection

✓ Historical price storage

✓ Stock universe management

✓ Technical indicators

✓ Feature generation

✓ Historical feature storage

✓ ML dataset generation

✓ Daily pipeline automation



Main components:


```
price_history_collector.py

feature_history_builder.py

historical_ml_builder.py

daily_pipeline.py
```



---


# Historical ML Dataset


Current dataset:


```
data/historical_ml_dataset.csv
```



Purpose:


Train historical market behavior models.



Features include:


- returns

- RSI

- SMA indicators

- volume metrics

- volatility

- ATR

- momentum

- range position

- trend information



Important:


Previous small datasets are considered unreliable.



---


# Machine Learning Status


## Phase 2 — ML Foundation


Status:


COMPLETE ✅



Implemented:


✓ ML training pipeline

✓ Model versioning

✓ Model registry

✓ Feature tracking

✓ Chronological validation

✓ Backtest integration

✓ Champion model selection



---


# Model History


## model_v27


Status:


RETIRED ❌



Previous reported performance:


Accuracy:

98.3%



F1:

96.1%



Reason retired:


- insufficient dataset

- possible data leakage

- unrealistic validation

- misleading metrics



Rule:


model_v27 must not be used as a benchmark.



---


# Current Champion Model


## model_v33


Status:


Current Champion ✅



Algorithm:


Random Forest



Features:


- return features

- RSI

- SMA

- volume

- volatility

- ATR

- momentum

- range position



Validation:


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



Champion selection considers:


- predictive quality

- trading performance

- stability



---


# ML Architecture — Two Separate Paths


The platform now maintains two separate ML intelligence paths.



They serve different purposes.



---


# Historical ML Path


Purpose:


Analyze historical market patterns.



Input:


```
data/historical_ml_dataset.csv
```



Output:


```
Historical_ML_Probability
```



Used for:


- historical similarity

- pattern confirmation

- research confidence



---


# Scanner ML Path


Purpose:


Evaluate current market candidates.



Output:


```
ML_Probability
```



Used for:


- current opportunity evaluation

- ranking support

- AI scoring



Important:


These paths should remain separated.



---


# AI Research Engine Status


## Phase 3 — AI Research Engine


Status:


Advanced 🚧



Completed:


✓ Research ranking engine

✓ Research score normalization

✓ AI final scoring framework

✓ ML probability integration

✓ Historical ML integration

✓ Confidence scoring

✓ AI decision logic

✓ Risk-aware decision pipeline

✓ Trade explanation system

✓ Automated reports



---


# AI Decision Pipeline


Current flow:



```
Research Ranking

↓

Optimized Final Score

↓

AI Confidence

↓

ML Probability

↓

Historical ML Probability

↓

Risk Evaluation

↓

AI Final Decision Controller

↓

Trade Management
```



Final outputs:


- BUY

- WATCH

- REJECT



With:


- conviction score

- confidence level

- decision explanation



---


# Risk Management Status


Implemented:


✓ Risk scoring

✓ Portfolio risk filtering

✓ Position sizing

✓ Stop loss calculation

✓ Target calculation

✓ Reward/risk analysis

✓ Expected value calculation



Trade approval now requires:


- AI approval

- portfolio approval

- risk approval



---


# Trade Management Status


Implemented:


Trade setup generation:


- entry price

- stop loss

- target 1

- target 2

- position size

- capital allocation



Trade grading:


- A

- B

- C

- D



Execution states:


- READY

- WATCH

- MONITOR

- BLOCKED



---


# Feedback Learning Foundation


Added foundation modules:


```
trade_history.py

trade_history_manager.py

trade_feedback.py

trade_performance.py

trade_performance_tracker.py

ai_learning_engine.py

trade_exit_manager.py

live_trade_monitor.py
```



Purpose:


Create future learning cycle:



Trade Decision

↓

Outcome Tracking

↓

Performance Analysis

↓

Strategy Improvement



---


# Current Known Limitations


## Model Validation


Need:


- walk-forward validation

- longer testing periods

- market regime testing



---


## Probability Calibration


Need:


- calibrated confidence

- probability reliability analysis



---


## Backtesting


Need:


- professional equity curve

- drawdown analysis

- benchmark comparison

- transaction cost simulation

- Sharpe ratio

- Sortino ratio



---


## Portfolio Intelligence


Need:


- correlation analysis

- sector exposure

- risk budgeting

- portfolio optimization



---


# Current Development Priorities


## Priority 1 — Professional Validation


Build:


- walk-forward testing

- benchmark comparison

- risk-adjusted metrics



---


## Priority 2 — AI Quality Improvement


Improve:


- false positive reduction

- confidence calibration

- decision accuracy

- historical validation



---


## Priority 3 — Learning System


Develop:


- trade outcome feedback

- performance analysis

- automatic improvement suggestions



---


# Development Philosophy


The platform follows quantitative research principles.



Optimize for:


✓ realistic performance

✓ reproducibility

✓ transparency

✓ controlled risk

✓ continuous improvement



Avoid:


✗ unrealistic accuracy

✗ overfitting

✗ data leakage

✗ curve fitting

✗ unsupported automation



---


# Final Project Direction


The goal is to build:


An AI-powered quantitative research assistant.



The system should help answer:


- Which opportunities have historical support?

- Which setups have favorable risk/reward?

- Which decisions are supported by multiple intelligence layers?

- How does performance improve over time?



The platform evolves through:


historical evidence + machine learning + risk analysis + feedback learning.
