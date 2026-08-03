# AI Trading Research Platform — Changelog


Repository:

AI-Trading-Research-Platform


GitHub:

https://github.com/AnastasiyaKotelnikova/AI-Trading-Research-Platform


Local Path:

C:\Users\anast\scanner-project



All notable changes to this project are documented here.



---

# [2026-08-03]


## AI Decision Pipeline, Risk Management, and ML Architecture Update


### Added


### Two Separate ML Intelligence Paths


Implemented separation between:


## Historical ML Path


Purpose:

Historical market pattern validation.



Features:


- expanded historical dataset

- technical indicators

- momentum features

- volatility features

- volume features

- ATR-based features



Output:


```
Historical_ML_Probability
```



Used for:


- historical similarity analysis

- research confidence

- pattern validation



---


## Scanner ML Path


Purpose:

Current market opportunity evaluation.



Features:


- RSI

- returns

- trend indicators

- ranking features

- momentum factors

- risk/reward factors



Output:


```
ML_Probability
```



Used for:


- scanner confirmation

- AI ranking

- decision scoring



---


# Model History Cleanup


## model_v27


Status:


RETIRED ❌



Previous reported metrics:


Accuracy:

98.3%



F1:

96.1%



Reason for retirement:


- insufficient training data

- possible data leakage

- unrealistic validation

- misleading performance expectations



Decision:


model_v27 removed as performance benchmark.



Lesson:


High classification metrics do not guarantee useful trading performance.



---


# Current Champion Model


## model_v33


Status:


Current Champion ✅



Algorithm:


Random Forest



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

- reliability



---


# AI Research Engine Improvements


## Research Ranking System


Updated:


Research Score normalization.



Improvements:


- reduced score inflation

- improved ranking separation

- improved comparison between candidates

- better historical validation compatibility



---


# AI Decision Pipeline


Added:


AI decision intelligence layer.



Components:


```
ai_decision.py

ai_final_decision_controller.py
```



Capabilities:


- multi-factor scoring

- ML confidence integration

- risk filtering

- strategy weighting

- final BUY/WATCH/REJECT decisions



Outputs:


- final conviction score

- confidence level

- decision explanation



---


# Risk Management Integration


Improved trade approval workflow.



Added:


- portfolio risk validation

- risk score integration

- trade approval filtering

- position sizing controls



Trade decisions now consider:


- opportunity quality

- risk profile

- expected value

- reward/risk ratio



---


# Trade Management Improvements


Updated:


```
trade_management.py
```



Added:


- ATR-based stop loss

- multiple profit targets

- position sizing

- risk per trade calculation

- reward/risk calculation

- expected value calculation

- execution readiness status



Trade states:


- READY

- WATCH

- MONITOR

- BLOCKED



---


# Trade Intelligence Foundation


Added:


```
trade_history.py

trade_history_manager.py

trade_feedback.py

trade_performance.py

trade_performance_tracker.py

trade_exit_manager.py

live_trade_monitor.py

ai_learning_engine.py
```



Purpose:


Create future feedback learning loop:



Trade Decision

↓

Execution Tracking

↓

Performance Analysis

↓

Future Improvement



---


# Documentation Updates


Updated:


- AI_PROJECT_MEMORY.md

- MODEL_HISTORY.md

- EXPERIMENT_LOG.md

- ROADMAP.md

- DEVELOPMENT_RULES.md



Documentation now includes:


- model retirement history

- two ML architecture paths

- AI decision pipeline

- risk management rules

- future development stages



---


# [2026-07-29]


## Research Ranker V3


### Added


Normalized Research Score framework.



Improvements:


- removed score inflation

- improved factor weighting

- improved candidate separation

- prepared system for historical validation



---


# [2026-07]


## Machine Learning Foundation Expansion


### Added


Historical ML training pipeline.



Implemented:


- expanded historical dataset

- chronological validation

- Random Forest evaluation

- model registry

- champion model selection



Retired:


Earlier models trained on smaller datasets.



---


# [2026-07]


## Initial Platform Development


### Added


Core research platform foundation.



Implemented:


- stock universe management

- Yahoo market data collection

- technical indicators

- feature generation

- historical data storage

- scanner pipeline



---


# Development Philosophy


This project follows quantitative research principles.



Priority:


1. Realistic validation

2. Reproducible experiments

3. Risk control

4. Transparent decisions

5. Continuous improvement



The system is designed as:


An AI-assisted trading research platform.



It is not:


- a guaranteed prediction system

- automatic trading software

- a replacement for risk management



---

# Future Planned Changes


Upcoming:


- walk-forward validation

- professional backtesting

- benchmark comparison

- probability calibration

- SHAP explainability

- model monitoring

- paper trading framework

- portfolio optimization

- optional broker integration
