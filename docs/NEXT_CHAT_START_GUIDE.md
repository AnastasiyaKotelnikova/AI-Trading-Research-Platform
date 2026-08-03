# AI Trading Research Platform — Next Chat Start Guide


Repository:

AI-Trading-Research-Platform


GitHub:

https://github.com/AnastasiyaKotelnikova/AI-Trading-Research-Platform


Local Path:

C:\Users\anast\scanner-project



Last Updated:

2026-08-03



# How to Continue Work in a New Chat


Before making recommendations, architecture changes, or code modifications:


Read these documents first:


```
docs/AI_PROJECT_MEMORY.md

docs/MODEL_HISTORY.md

docs/EXPERIMENT_LOG.md

docs/ARCHITECTURE.md

docs/ROADMAP.md

docs/DEVELOPMENT_RULES.md

docs/CHANGELOG.md
```



These files contain:


- current project status

- completed phases

- architecture decisions

- model history

- experiments

- development rules

- recent changes



These documents are the source of truth.



---


# Current Project State


Project:


AI Trading Research Platform



Purpose:


Build an AI-assisted quantitative stock research system.



The platform is designed to:


- collect market data

- generate technical features

- train machine learning models

- rank opportunities

- evaluate historical performance

- analyze risk

- generate AI decisions

- track trade outcomes

- improve through feedback



The system is a research assistant.


It is not a guaranteed prediction engine.



---


# Development Environment


Location:


```
C:\Users\anast\scanner-project
```



Environment:


```
Python 3.11.9

venv
```



Run modules:


```
python -m app.module_name
```



Example:


```
python -m app.train_model
```



---


# Current Development Phase


## Phase 3 — AI Research Engine


Status:


Advanced / Near Completion



Current objective:


Improve research quality before production-level features.



Current priorities:


1. Improve AI decision quality

2. Validate ranking performance

3. Add probability calibration

4. Improve backtesting

5. Build feedback learning loop



---


# Important Architecture Update


The platform now contains two separate ML paths.



They must remain separated.



---


# ML Path 1 — Historical ML


Purpose:


Learn from historical market behavior.



Training source:


```
data/historical_ml_dataset.csv
```



Features:


- returns

- RSI

- SMA indicators

- volume features

- volatility

- ATR

- momentum

- range position



Used by:


```
load_historical_ml_model()
```



Output:


```
Historical_ML_Probability
```



Purpose:


Measure historical pattern similarity.



---


# ML Path 2 — Scanner ML


Purpose:


Evaluate current market candidates.



Features:


- RSI

- returns

- technical ranking

- momentum

- trend

- relative strength

- risk/reward



Used by:


```
load_model()
```



Output:


```
ML_Probability
```



Purpose:


Current opportunity confirmation.



Do not merge these paths without architectural review.



---


# Current ML Model Status


## model_v27


Status:


RETIRED ❌



Previous:


Accuracy:

98.3%



F1:

96.1%



Reason:


- small dataset

- possible leakage

- unrealistic validation

- misleading performance



Rule:


Never use model_v27 as benchmark.



---


# Current Champion Model


## model_v33


Status:


Current Champion ✅



Algorithm:


Random Forest



Evaluation:


- F1 Score

- ROC-AUC

- Average Return

- Win Rate



Current results:


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



The project does not optimize only for accuracy.



---


# Current AI Decision Pipeline


Current flow:



Market Data

↓

Feature Engineering

↓

Scanner ML Probability

↓

Historical ML Probability

↓

Research Ranking

↓

AI Final Score

↓

Risk Evaluation

↓

AI Final Decision Controller

↓

Trade Management

↓

Performance Tracking



---


# Current Important Modules


Machine Learning:


```
app/train_model.py

app/ml_predictor.py

app/model_loader.py

app/model_registry.py
```



AI Decision:


```
app/ai_decision.py

app/ai_final_decision_controller.py

app/ai_decision_engine.py
```



Ranking:


```
app/research_ranker.py

app/ai_ranker.py
```



Risk / Trade:


```
app/trade_management.py

app/trade_exit_manager.py

app/trade_history_manager.py

app/trade_performance_tracker.py
```



Learning:


```
app/ai_learning_engine.py

app/trade_feedback.py
```



---


# Important Development Rules


Before changing code:


1. Read existing architecture.

2. Check related modules.

3. Avoid duplicate systems.

4. Preserve working pipeline.

5. Explain why the change improves the platform.



---


# ML Development Rules


Every model experiment must record:


- dataset

- features

- algorithm

- hyperparameters

- metrics

- backtest results

- acceptance decision



Update:


```
docs/MODEL_HISTORY.md
```



---


# Experiment Rules


Every major experiment must update:


```
docs/EXPERIMENT_LOG.md
```



Include:


- objective

- files changed

- result

- decision

- next action



---


# Documentation Rules


After major changes update:


```
AI_PROJECT_MEMORY.md

MODEL_HISTORY.md

EXPERIMENT_LOG.md

ARCHITECTURE.md

ROADMAP.md

DEVELOPMENT_RULES.md

CHANGELOG.md
```



---


# Git Workflow


Always work from:


```
C:\Users\anast\scanner-project
```



Check:


```
git status
```



Review changes before committing.



Commit format:


```
git add .

git commit -m "Describe meaningful change"

git push
```



Good examples:


```
Improve AI decision risk filtering

Add trade feedback tracking

Improve historical ML validation
```



Avoid:


```
update

changes

test
```



---


# Before Coding


Confirm:


- current architecture

- existing modules

- previous decisions

- experiment history



Do not redesign the system unless necessary.



---


# After Coding


Always:


1. Run tests.

2. Validate output.

3. Update documentation.

4. Commit changes.

5. Push to GitHub.



---


# Current Recommended Next Tasks


Priority order:



## 1. Professional Backtesting


Develop:


- walk-forward validation

- benchmark comparison

- equity curve

- drawdown analysis

- Sharpe ratio

- Sortino ratio



---


## 2. Probability Calibration


Improve:


- ML confidence reliability

- probability interpretation

- confidence thresholds



---


## 3. AI Decision Validation


Analyze:


- BUY decisions

- false positives

- successful patterns

- failed setups



---


## 4. Feedback Learning System


Develop:


- trade outcome tracking

- model feedback

- strategy improvement



---


# New Chat Opening Message


Copy this:


```
I am continuing my AI Trading Research Platform project.

First read:

docs/AI_PROJECT_MEMORY.md

docs/MODEL_HISTORY.md

docs/EXPERIMENT_LOG.md

docs/ARCHITECTURE.md

docs/ROADMAP.md

docs/DEVELOPMENT_RULES.md

docs/CHANGELOG.md

Use these documents as the source of truth.

Current repository:

AI-Trading-Research-Platform

Local path:

C:\Users\anast\scanner-project

Current phase:

Phase 3 — AI Research Engine

Important:

model_v27 is retired.
Do not use it as a benchmark.

Current accepted model:

model_v33

The platform has two separate ML paths:

1. Historical ML probability
2. Scanner ML probability

Continue from the last completed task.

Do not redesign architecture unless necessary.
```
