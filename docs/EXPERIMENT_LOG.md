# AI Trading Research Platform — Experiment Log

Last Updated:

2026-08-08

# Purpose

This document tracks important engineering experiments, model changes, system improvements, validation tests, and architecture decisions.

Each experiment records:

* Date
* Objective
* Files changed
* Dataset/model impact
* Result
* Decision
* Next action

The purpose is to maintain:

* reproducibility
* transparency
* experiment history
* controlled development

---

# Experiment History

# EXP-001 — Initial Scanner Development

Date:

2026-07

Objective:

Build the first automated stock scanning pipeline.

Changes:

* Created stock universe builder
* Added Yahoo price collection
* Added technical indicators
* Created scanner pipeline

Result:

Successfully generated technical stock signals.

Decision:

Continue expanding into ML prediction and AI research.

---

# EXP-002 — Historical Feature Dataset Creation

Date:

2026-07

Objective:

Create historical training data for machine learning.

Changes:

* Built historical feature pipeline
* Generated historical feature files
* Created historical_ml_dataset.csv

Dataset:

Stocks:

~4,000

Rows:

220,849+

Features:

* Returns
* RSI
* SMA
* Volume metrics
* Volatility
* Momentum

Result:

Created the foundation for supervised learning.

Decision:

Proceed with ML development.

---

# EXP-003 — Initial ML Models

Date:

2026-07

Objective:

Train first ML prediction models.

Models tested:

* Logistic Regression
* Random Forest

Metrics:

* Accuracy
* Precision
* Recall
* F1
* ROC-AUC

Result:

Random Forest showed better trade classification performance.

Decision:

Create champion/challenger model system.

---

# EXP-004 — model_v27 Investigation and Retirement

Date:

2026-07

Objective:

Review previous champion model performance.

Model:

model_v27

Previously reported metrics:

Accuracy:

98.3%

F1:

96.1%

Finding:

The results were considered unreliable for the current research framework.

Problems identified:

* insufficient dataset size
* possible data leakage
* unrealistic validation
* biased historical representation

Decision:

Retire model_v27 from the active research path.

model_v27 is no longer considered a valid candidate for future champion selection.

Important lesson:

High ML metrics do not guarantee useful trading performance.

---

# EXP-005 — Expanded Dataset Retraining

Date:

2026-07

Objective:

Retrain models using improved historical data.

Changes:

Added:

* ATR
* ATR_Percent
* Range_Position
* Distance_From_52W_High
* Volume_Trend

Dataset:

Training records:

3,504,289

Testing records:

98,034

Validation:

Chronological split.

Result:

Created a more realistic ML evaluation framework.

Decision:

Continue model comparison using realistic metrics.

---

# EXP-006 — model_v33 Development

Date:

2026-07-28

Objective:

Develop a model using the expanded historical dataset and more realistic validation.

Model:

model_v33

Algorithm:

Random Forest

Configuration:

* n_estimators: 500
* max_depth: 20
* min_samples_leaf: 10
* max_features: sqrt
* class_weight: balanced

Results:

ROC-AUC:

0.669

F1:

0.467

Accuracy:

0.551

Training records:

3,504,289

Observed trading performance:

Completed trades:

272

Win Rate:

30.88%

Average Return:

2.65%

Best Trade:

70.3%

Worst Trade:

-9.96%

Decision:

Retain model_v33 as the current active research champion.

Reason:

model_v33 is supported by actual completed trading history, unlike the previously retired high-metric model_v27.

---

# EXP-007 — Research Score Normalization V3

Date:

2026-07-29

Objective:

Improve Research Score quality.

Problem:

Previous scoring allowed inflated scores above expected ranges.

Issues:

* poor comparability
* ranking saturation
* threshold optimization problems

Changes:

Updated:

app/research_ranker.py

Implemented:

* normalized scoring
* improved factor weighting
* controlled score range
* better ranking separation

Result:

Research Score became more interpretable.

Decision:

Accept Research Ranker V3.

---

# EXP-008 — Research Score Validation

Date:

2026-07-29

Objective:

Validate whether Research Score correlates with future performance.

Dataset:

data/trade_database.csv

Method:

Quartile analysis.

Finding:

Higher Research Scores produced stronger average historical returns.

Decision:

Accept normalized Research Score system.

---

# EXP-009 — Two ML Path Architecture Separation

Date:

2026-08-03

Objective:

Clarify separation between historical ML research and scanner ML prediction.

Problem:

Previous documentation did not clearly distinguish the two systems.

Changes:

Documented:

## Historical ML Path

Module:

app/train_model.py

Purpose:

Historical pattern prediction using expanded ML dataset.

Output:

Historical ML probability.

---

## Scanner ML Path

Modules:

app/ml_predictor.py

app/model_loader.py

Purpose:

Current opportunity confirmation inside scanner pipeline.

Output:

* ML_Probability
* ML_Prediction
* ML_Model

Result:

Clear separation between training research and scanner intelligence.

Decision:

Maintain two independent ML paths.

---

# EXP-010 — AI Final Decision Controller

Date:

2026-08-03

Objective:

Create final AI approval layer combining ranking, ML confidence, and risk.

Module:

app/ai_final_decision_controller.py

Changes:

Added:

* multi-layer scoring
* risk integration
* ML confidence integration
* final BUY/WATCH/REJECT decision

Scoring:

Risk:

25%

Ranking:

45%

ML Confidence:

20%

Strategy:

10%

Result:

Created final conviction-based decision framework.

Decision:

Accept AI Final Decision Controller.

---

# EXP-011 — Trade Management Integration

Date:

2026-08-03

Objective:

Convert approved AI decisions into structured trade plans.

Module:

app/trade_management.py

Added:

* entry price
* ATR stop loss
* target calculation
* position sizing
* reward/risk calculation
* expected value calculation

Result:

Research signals can now generate structured trade plans.

Decision:

Accept trade management layer.

---

# EXP-012 — Trade Intelligence Foundation

Date:

2026-08-03

Objective:

Create foundation for learning from trade outcomes.

Added modules:

* trade_history.py
* trade_history_manager.py
* trade_feedback.py
* trade_performance.py
* trade_performance_tracker.py
* trade_exit_manager.py
* live_trade_monitor.py
* ai_learning_engine.py

Purpose:

Track:

* decisions
* outcomes
* performance
* future improvement signals

Decision:

Foundation accepted.

Next:

Connect feedback into model monitoring and optimization.

---

# EXP-013 — Risk-Aware AI Pipeline Update

Date:

2026-08-03

Objective:

Improve decision quality by integrating portfolio risk controls.

Changes:

Connected:

* AI ranking
* portfolio risk
* final conviction scoring
* trade approval logic

Result:

Weak opportunities can now be rejected before trade planning.

Decision:

Accept risk-aware decision pipeline.

---

# EXP-014 — Model Trading Eligibility Control

Date:

2026-08-08

Objective:

Prevent models without real completed trading history from being selected as the recommended champion.

Problem:

The previous model quality calculation could rank models highly based on F1 alone even when those models had no completed trading history.

Changes:

Updated:

app/model_quality_evaluator.py

Implemented:

* Trading_Eligible flag
* completed-trade requirement
* models with zero completed trades receive a Trading_Quality_Score of zero
* only trading-eligible models can become the recommended champion

Eligibility rule:

A model is considered trading eligible when:

Completed_Trades > 0

Result:

Models with impressive historical ML metrics but no completed trading history can no longer automatically become the recommended champion.

Current eligible model:

model_v33

Current observed performance:

Completed Trades:

272

Win Rate:

30.88%

Average Return:

2.65%

Current Trading Quality Score:

38.491474

Decision:

Accept trading-eligibility control.

Important lesson:

ML classification metrics and real trading evidence must both be considered when selecting the active research champion.

---

# EXP-015 — model_v27 Permanent Evaluation Exclusion

Date:

2026-08-08

Objective:

Remove the retired model_v27 from future model-quality evaluation.

Model:

model_v27

Reason:

model_v27 belongs to the previously identified unreliable high-metric experiment and should not influence future champion selection.

Changes:

Updated:

app/model_quality_evaluator.py

Implemented:

Explicit exclusion list:

model_v27

Result:

model_v27 is removed before model-quality scoring and cannot become the recommended champion.

Decision:

Keep model_v27 permanently excluded from the active evaluation path.

---

# EXP-016 — Champion Manager Validation

Date:

2026-08-08

Objective:

Verify that the champion manager correctly uses the recommended model and does not unnecessarily replace the current champion.

Module:

app/champion_manager.py

Validation:

Recommended model:

model_v33

Current champion:

model_v33

Result:

Champion manager reported:

Best model:

model_v33

Current champion:

model_v33

Decision:

Champion unchanged.

Result confirms that the champion manager is correctly aligned with the current evaluator result.

---

# EXP-017 — Model Feedback Loop Validation

Date:

2026-08-08

Objective:

Connect completed trade outcomes to model-level performance reporting.

Module:

app/model_feedback_loop.py

Input:

data/trade_history.csv

Output:

data/models/model_feedback_report.csv

Current feedback:

model_v33:

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

70.3%

Worst Trade:

-9.96%

Stored model metrics:

Accuracy:

55.14%

F1:

46.74%

Result:

The feedback loop successfully groups completed trades by model and produces model-level trading performance statistics.

Decision:

Accept feedback reporting layer.

Next:

Use validated trading feedback as part of ongoing model monitoring and future retraining decisions.

---

# EXP-018 — Live Trade Monitoring Foundation

Date:

2026-08-08

Objective:

Monitor currently open trades and update their status using current market prices.

Modules:

* app/live_trade_monitor.py
* app/trade_history.py

Capabilities:

* load open trades
* load current prices
* update current price
* calculate days held
* detect stop loss
* detect Target 1
* detect Target 2
* enforce maximum holding period
* calculate realized return
* calculate realized profit
* close completed trades

Maximum holding period:

30 days

Exit conditions:

* STOP LOSS
* TARGET 1 HIT
* TARGET 2 HIT
* TIME EXIT

Result:

The platform now has a structured mechanism for monitoring open trades and recording completed trade outcomes.

Decision:

Accept live trade monitoring foundation.

Next:

Continue integrating monitoring results into the feedback and model-performance lifecycle.

---

# EXP-019 — Daily Pipeline Integration

Date:

2026-08-08

Objective:

Establish a single controlled execution path for the major scanner, AI, trade, and model-feedback components.

Module:

app/daily_pipeline.py

Current pipeline stages:

1. Running Integrated Scanner
2. Saving Signal History
3. Running Forward Test
4. Updating Trade Database
5. Generating AI Rankings
6. Generating AI Decisions
7. Generating AI Report
8. Updating Model Feedback Loop
9. Updating Model Champion Tracker

Pipeline capabilities:

* sequential execution
* subprocess isolation
* logging
* pipeline status tracking
* failure detection
* completed-step tracking
* start/end timestamps
* duration tracking
* failure reporting

Status file:

data/logs/pipeline_status.json

Log file:

data/logs/daily_pipeline.log

Result:

The major research and trading components are organized into a controlled daily execution pipeline.

Decision:

Accept the current pipeline controller as the execution foundation.

Next:

Validate the complete end-to-end pipeline and identify any remaining integration gaps before adding additional intelligence.

---

# Current Model State

As of:

2026-08-08

Current research champion:

model_v33

Model status:

CHAMPION

Model metrics:

Accuracy:

55.14%

F1:

46.74%

ROC-AUC:

0.669

Training records:

3,504,289

Observed trading performance:

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

70.3%

Worst Trade:

-9.96%

model_v27 status:

RETIRED / EXCLUDED

model_v27 is not part of future model-quality evaluation or champion selection.

---

# Future Experiments

# EXP-020 — Probability Calibration

Status:

Planned

Objective:

Improve confidence reliability.

Goal:

Predicted probabilities should better match actual success frequency.

---

# EXP-021 — Walk Forward Validation

Status:

Planned

Objective:

Create professional out-of-sample testing.

Method:

Rolling historical validation.

---

# EXP-022 — SHAP Explainability

Status:

Planned

Objective:

Understand feature contribution and AI reasoning.

---

# EXP-023 — Professional Backtesting

Status:

Planned

Add:

* transaction costs
* benchmark comparison
* equity curves
* drawdown analysis
* Sharpe ratio
* Sortino ratio

---

# EXP-024 — Automated Model Monitoring

Status:

Planned

Objective:

Create a controlled monitoring system that continuously evaluates the active champion using newly completed trades.

Potential components:

* minimum completed-trade threshold
* rolling win rate
* rolling average return
* drawdown monitoring
* model degradation detection
* comparison against previous champion
* retraining trigger conditions

Decision criteria should be based on actual trading performance rather than ML classification metrics alone.

---

# EXP-025 — Automated Retraining and Champion Promotion

Status:

Planned

Objective:

Create a controlled lifecycle for future model retraining.

Potential workflow:

New data

→

Model training

→

Model evaluation

→

Trading validation

→

Quality scoring

→

Champion recommendation

→

Champion promotion

→

Production monitoring

Requirements:

* no data leakage
* chronological validation
* sufficient trading evidence
* minimum performance thresholds
* reproducible model versioning
* explicit promotion rules

---

# Experiment Rules

Before accepting improvements:

Required:

* validate with historical data
* avoid leakage
* compare against previous version
* document results
* update architecture documentation
* verify downstream pipeline compatibility

The platform prioritizes:

**realistic research performance over artificially high metrics.**

# Current Development Principle

The platform should not select a model solely because it has a high ML classification score.

A model must demonstrate:

1. valid historical evaluation
2. realistic validation
3. actual trading evidence
4. sufficient completed trades
5. acceptable trading performance
6. compatibility with the production pipeline

The current active research champion is:

**model_v33**

The previously retired model_v27 is excluded from future evaluation.
