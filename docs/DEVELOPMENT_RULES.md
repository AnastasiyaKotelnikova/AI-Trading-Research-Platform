# AI Trading Research Platform — Development Rules

Repository:

AI-Trading-Research-Platform

GitHub:

https://github.com/AnastasiyaKotelnikova/AI-Trading-Research-Platform

Local Path:

C:\Users\anast\scanner-project

Last Updated:

2026-11-10 

# Purpose

These rules keep the project organized as it grows.

The goal is to maintain:

* reproducibility
* experiment history
* model transparency
* clean development workflow
* architecture consistency
* realistic trading research standards
* controlled model governance
* reliable feedback and validation

The platform is a quantitative research system.

It is not designed around unrealistic prediction accuracy or uncontrolled automation.

The platform is not approved for automated real-money trading.

---

# 1. Before Making Major Changes

Before modifying important components:

Always review:

* AI_PROJECT_MEMORY.md
* ARCHITECTURE.md
* ROADMAP.md
* EXPERIMENT_LOG.md
* MODEL_HISTORY.md

Understand:

* why the change is needed
* what problem it solves
* how success will be measured
* what existing components are affected
* whether an existing module already performs the required function

Avoid:

* creating duplicate systems
* replacing working modules without reason
* changing architecture without documentation
* creating competing data sources
* creating multiple versions of the same feedback or performance system

Before adding a new module, search the repository for related functionality.

---

# 2. Machine Learning Development Rules

Every ML model training experiment must record:

## Dataset

Document:

* dataset file name
* date range
* number of rows
* number of features
* training/testing split
* validation method

Never compare models trained on different datasets without documenting the difference.

---

## Features

Record:

* added features
* removed features
* feature importance
* reason for changes
* possible leakage concerns

Feature changes must be documented in:

```text
docs/EXPERIMENT_LOG.md
```

---

## Model Information

Record:

* model version
* algorithm
* hyperparameters
* training date
* training environment

Examples:

* Random Forest
* XGBoost
* LightGBM
* Neural Network

---

# 3. Model Evaluation Rules

Required classification metrics:

* Accuracy
* Precision
* Recall
* F1 Score
* ROC-AUC

However:

Classification metrics alone are not enough.

Trading evaluation must include:

* completed trades
* win rate
* average return
* best trade
* worst trade
* drawdown
* risk metrics
* stability across market conditions

The project prioritizes trading usefulness over classification scores.

A model with excellent classification metrics but no demonstrated trading performance must not automatically become champion.

---

## Trading Evidence Verification — November 2026

The existing model-quality evaluator uses:

`Completed_Trades > 0`

as its documented trading-eligibility requirement.

This is a minimum software eligibility condition, not proof of statistical reliability or real-world profitability.

Before completed trades are used for model promotion, verify:

1. The source of the trade records.
2. Whether the trades are historical simulations, research records, paper trades, or actual executed trades.
3. That entry and exit prices are supported by historical market data.
4. That trade outcomes follow the documented strategy rules.
5. That no future information was used to generate earlier decisions.
6. That the evaluated trade sample is sufficiently representative.

Previously generated model-feedback statistics must not be interpreted as verified live trading results.

Future model-governance improvements should introduce stronger minimum sample-size, stability, and risk requirements.

---

# 5. Model Quality Evaluation

The model quality evaluator is:

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

It produces:

```text
Trading_Quality_Score
```

Models without completed trading history receive:

```text
Trading_Eligible = False
```

and cannot become the recommended champion.

The current system therefore distinguishes between:

1. predictive quality
2. trading eligibility
3. trading quality
4. champion status

This distinction must be preserved.

---

# 6. Champion Model Rules

A new model cannot replace the champion only because it has:

* higher accuracy
* higher F1 score
* higher training score
* higher ROC-AUC

A replacement model must demonstrate:

✓ realistic validation

✓ no evidence of leakage

✓ trading eligibility

✓ meaningful trading performance

✓ acceptable risk

✓ sufficient stability

Champion decisions must be recorded in:

```text
docs/MODEL_HISTORY.md
```

The champion manager must not automatically promote an unproven model simply because of superior classification metrics.

---

# 7. Current Champion Governance

The current historical research champion is:

`model_v33`

**Status:** Current Research Champion — Not Production Approved

The previously recorded model-governance evaluation reported:

| Metric | Value |
|---|---|
| F1 Score | 0.4674 |
| Accuracy | 55.14% |
| Completed Trades | 272 |
| Win Rate | 30.88% |
| Average Return | 2.65% |

These values are historical evaluation snapshots.

The source and consistency of the completed-trade statistics must be verified against the current trade-history database and feedback outputs.

The current research champion must not be treated as a production-ready trading model.

### Model Retirement

`model_v27` remains retired and excluded from current champion selection.

Its earlier classification results must not be used as the benchmark for new models.

### November 2026 Governance Priority

The model-governance architecture includes:

- `app/model_quality_evaluator.py`
- `app/champion_manager.py`
- `app/model_champion_tracker.py`
- `app/model_feedback_loop.py`

The immediate unfinished development task is to verify integration and execution order within `app/daily_pipeline.py`.

Required checks:

1. Correct model-quality evaluation.
2. Exclusion of retired models.
3. Correct trading-eligibility decisions.
4. Consistent champion recommendation and active champion status.
5. Reliable handling of missing or invalid data.
6. Correct downstream outputs.
7. Failure logging and reproducibility.

Do not replace the champion until a challenger demonstrates validated improvement under documented governance rules.

---

# 8. Model v27 Rule

model_v27 is permanently retired.

Previous reported metrics:

Accuracy:

98.3%

F1:

96.1%

Reason:

* insufficient dataset
* possible leakage
* unrealistic validation
* misleading performance expectations

Important:

model_v27 must not be used as a benchmark.

Do not:

* compare new models against v27 as the performance standard
* restore v27 because of its historical metrics
* use its 98.3% accuracy or 96.1% F1 as a target
* allow old v27 results to influence champion selection

Future models must be evaluated using reliable validation and actual trading evidence.

---

# 9. Two ML Path Architecture Rule

The platform contains two separate ML paths.

They must remain logically separated.

---

## Historical ML Path

Purpose:

Learn from historical market behavior.

Primary training system:

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
* research confidence
* historical evidence

---

## Scanner ML Path

Purpose:

Evaluate current market candidates.

Primary modules:

```text
app/ml_predictor.py
app/model_loader.py
```

Outputs may include:

```text
ML_Probability
ML_Prediction
ML_Model
ML_F1
ML_Accuracy
```

Used for:

* scanner ranking
* AI scoring
* current opportunity evaluation
* confidence assessment

Do not merge these paths without architectural review.

Do not assume that a historical model probability and a scanner prediction represent the same type of evidence.

---

# 10. Experiment Logging Rules

Every significant experiment must update:

```text
docs/EXPERIMENT_LOG.md
```

Examples:

* new feature
* new model
* new algorithm
* scoring changes
* threshold changes
* validation changes
* risk logic changes
* decision pipeline changes
* feedback-system changes
* model-governance changes
* backtesting changes

Each experiment should include:

* date
* objective
* files changed
* dataset/model impact
* result
* decision
* next action

Experiments that materially change architecture must also update:

```text
docs/ARCHITECTURE.md
```

---

# 11. Dataset Rules

Dataset changes must record:

* source
* date range
* number of stocks
* number of rows
* feature list
* generation method

Never silently replace datasets.

Historical datasets are part of the research record.

Changes to:

```text
data/historical_ml_dataset.csv
```

must be treated as meaningful research changes.

Dataset expansion or regeneration must be documented before comparing resulting models with previous versions.

---

# 12. AI Decision System Rules

AI decisions must remain explainable.

Every final decision should consider, where applicable:

* ranking quality
* ML confidence
* historical evidence
* risk evaluation
* reward potential
* strategy performance
* portfolio constraints

Final decisions should include:

* decision
* confidence level
* reasoning

Current decision outputs include:

```text
BUY
WATCH
REJECT
```

The AI decision layer must not be treated as a guaranteed prediction engine.

Avoid:

* black-box decisions
* unsupported trade recommendations
* ignoring risk controls
* treating confidence as certainty

---

# 13. Risk Management Rules

Risk management is required before trade approval.

Trade logic must consider:

* stop loss
* position size
* reward/risk ratio
* expected value
* portfolio exposure
* allocation limits

No trade should become executable only because of:

* high ML probability
* high ranking score
* high historical success rate
* high AI confidence

Risk filtering remains mandatory.

Future risk improvements should include:

* volatility targeting
* correlation analysis
* sector exposure controls
* dynamic position sizing
* portfolio risk budgeting

---

# 14. Trade Management Rules

Trade management changes must be tested before acceptance.

Document changes involving:

* entries
* exits
* stop calculations
* targets
* sizing
* execution states
* reward/risk
* expected value

Relevant modules include:

```text
trade_management.py
trade_exit_manager.py
trade_history_manager.py
trade_feedback.py
trade_performance.py
trade_performance_tracker.py
```

Trade management must remain downstream of AI approval and risk controls.

---

# 15. Feedback and Learning Rules

Completed trades are a source of model-performance evidence.

The model feedback system includes:

```text
app/model_feedback_loop.py
```

Its purpose is to evaluate completed trades by model.

Feedback may include:

* completed trades
* winning trades
* losing trades
* win rate
* average return
* best trade
* worst trade
* model accuracy
* model F1

Feedback output:

```text
data/models/model_feedback_report.csv
```

The feedback loop must not automatically retrain or replace models without explicit governance rules.

Feedback is evidence for:

* model evaluation
* model monitoring
* champion/challenger analysis
* future retraining decisions

Do not interpret a small trading sample as statistically conclusive.

## Historical Trade Reconciliation Rules

The November 2026 review identified three OPEN research trades:

- KOD
- CNMD
- REZI

These trades must be reconciled using historical market data and the strategy rules applicable to their original entry dates.

### Required Procedure

1. Preserve the original trade records before modifying them.
2. Confirm entry date, entry price, stop loss, targets, and maximum holding period.
3. Retrieve historical prices covering the complete evaluation period.
4. Evaluate exits chronologically.
5. Apply documented stop-loss, target, and time-exit rules.
6. Handle missing data explicitly.
7. Record the historical exit date, price, outcome, and calculation method.
8. Recalculate model feedback only after trade outcomes have been verified.

### Prohibited Practices

- Closing historical trades using arbitrary current prices.
- Selecting favorable exits after observing future price movements.
- Inventing prices for missing historical sessions.
- Changing original stop-loss or target values retrospectively without documenting the change.
- Treating simulated trades as actual broker executions.
- Overwriting original research records without preserving an audit trail.

Historical reconciliation must be reproducible and free of lookahead bias.

---

# 16. Champion Manager Rules

Champion management must remain controlled.

Current module:

```text
app/champion_manager.py
```

The manager compares:

* recommended model
* current champion

A champion should remain unchanged when the recommended model does not provide sufficient evidence for replacement.

Example:

```text
Best model: model_v33
Current champion: model_v33

Champion unchanged.
```

Future automatic promotion should require clearly defined governance thresholds.

No automatic model promotion should be based solely on:

* one evaluation run
* one high F1 score
* one profitable trade period
* insufficient sample size

---

# 17. Daily Pipeline Rules

The daily pipeline coordinates major research stages.

Current controller:

```text
app/daily_pipeline.py
```

Pipeline stages include:

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

Each stage must:

* have a clear purpose
* return a meaningful success/failure status
* log failures
* preserve pipeline state

A failed downstream model-governance step must not be silently ignored.

Pipeline changes must be documented in:

```text
docs/ARCHITECTURE.md
docs/EXPERIMENT_LOG.md
```

---

# 18. Git Rules

Before major milestones:

Check:

```text
git status
```

Review:

* modified files
* untracked files
* generated data changes
* unexpected files
* duplicate modules

Commit:

```text
git status --short
git add docs/ARCHITECTURE.md
git diff --cached
git commit -m "docs: update architecture"
git push
```

## Git Synchronization and Backup Safety

The local repository may contain unfinished source-code changes, generated data, and untracked files.

Before synchronizing with GitHub:

1. Inspect `git status --short`.
2. Identify changes made directly on GitHub.
3. Review local modifications before pulling or merging.
4. Preserve unfinished work before attempting synchronization.
5. Stage only the files intentionally included in a commit.
6. Inspect staged differences before committing.
7. Verify synchronization before updating backups.

Do not run `git reset --hard` or other destructive commands to resolve synchronization differences without a verified backup and explicit review.

Do not indiscriminately stage generated datasets or model outputs.

The USB backup is a recovery copy and should not be assumed to contain the latest GitHub documentation until synchronization has been completed and verified.

**Local repository:** `C:\Users\anast\scanner-project`

**USB backup:** `E:\AI-Trading-Research-Backup`

Good commit examples:

```text
Improve AI decision risk filtering

Add historical ML probability integration

Update trade management logic

Improve model validation pipeline

Add model feedback evaluation

Improve champion selection governance
```

Avoid:

```text
changes

update

test

stuff
```

Before committing a major architecture change:

* run relevant tests
* review documentation
* inspect generated outputs
* verify that no unintended files changed

---

# 19. Testing Rules

Before accepting major changes run appropriate tests.

Required where applicable:

* training test
* scanner test
* AI decision test
* backtest
* validation
* trade feedback test
* model quality evaluation
* champion manager test

For model changes, verify:

* dataset
* features
* metrics
* trading performance
* output files
* model version
* champion status

Record significant results.

Major changes require documentation updates.

---

# 20. Architecture Rules

New modules must have:

* clear purpose
* descriptive name
* documentation
* integration point
* defined input/output

Avoid:

* duplicate files
* unused code
* abandoned experiments
* multiple competing pipelines
* multiple competing feedback systems
* multiple sources of truth

Before creating a new module:

Ask:

> Can an existing module be extended instead?

Search the repository first.

For example, before creating another feedback or performance module, inspect existing:

```text
app/model_feedback*
app/model_performance*
app/performance*
app/trade_feedback*
app/trade_performance*
```

If overlapping functionality already exists, consolidate or extend the existing system rather than creating another parallel implementation.

---

# 21. Documentation Rules

Update documentation after major changes.

Required files:

```text
docs/AI_PROJECT_MEMORY.md

docs/MODEL_HISTORY.md

docs/EXPERIMENT_LOG.md

docs/ARCHITECTURE.md

docs/ROADMAP.md

docs/DEVELOPMENT_RULES.md
```

Documentation should explain:

* what changed
* why it changed
* how it improves the system
* what was tested
* what the result was
* what remains to be done

Documentation must reflect the actual current code.

Do not document planned functionality as completed.

---

# 22. Professional Backtesting Rules

Before paper trading, the platform must develop professional validation.

Required capabilities:

* walk-forward validation
* out-of-sample testing
* benchmark comparison
* transaction costs
* equity curves
* maximum drawdown
* Sharpe ratio
* Sortino ratio
* CAGR
* market-regime analysis

Backtesting must avoid:

* look-ahead bias
* survivorship bias where applicable
* future information leakage
* unrealistic execution assumptions
* unrealistic transaction costs

A profitable backtest alone does not prove that a strategy is ready for live trading.

---

# 23. Paper Trading Rules

Paper trading cannot begin solely because:

* a model has a high F1
* a backtest is profitable
* a model has a high win rate
* the AI produces many BUY decisions

Before paper trading, the system should demonstrate:

✓ professional backtesting

✓ walk-forward validation

✓ stable model behavior

✓ functioning risk controls

✓ functioning trade tracking

✓ functioning performance monitoring

✓ functioning model feedback

✓ controlled champion management

Paper trading must remain separate from real-money execution.

---

# 24. Trading Research Philosophy

The platform optimizes for:

✓ realistic performance

✓ repeatability

✓ transparency

✓ risk control

✓ continuous improvement

✓ reproducible evidence

Not:

✗ unrealistic prediction accuracy

✗ overfitted models

✗ misleading metrics

✗ data leakage

✗ curve fitting

✗ automatic trading without validation

✗ automatic champion replacement without evidence

✗ treating small samples as proof of profitability

The goal:

Build an AI research assistant that improves decision quality through:

* historical evidence
* machine learning
* quantitative testing
* risk analysis
* feedback learning
* continuous model evaluation

---

# 25. Future Development Order

Future development should follow the roadmap:

```text
Phase 3

AI Research Engine

↓

Phase 4

Professional Backtesting

↓

Phase 5

Portfolio Intelligence

↓

Phase 6

Model Monitoring

↓

Phase 7

Paper Trading

↓

Phase 8

Optional Live Trading
```

New features should not skip validation stages.

The immediate priority is validation quality, not automated execution.

---

# 26. Current Development Priorities

**Checkpoint Date:** November 10, 2026

**Current Phase:** Phase 3 — AI Research Engine

**Phase 3 Progress:** Approximately 95% implemented

**Current Milestone:** Reliable AI Research Validation

Development resumed after approximately 2.5 months.

The current objective is to validate and stabilize the existing platform before expanding into professional backtesting and paper trading.

## Priority 1 — Data and Research Integrity

- Verify historical market data coverage.
- Validate stock-universe exclusions, including LUCY.
- Check historical feature consistency.
- Identify missing, stale, or inconsistent datasets.
- Preserve reproducibility.

## Priority 2 — Model Governance Integration

- Validate `app/model_quality_evaluator.py`.
- Validate `app/champion_manager.py`.
- Verify integration in `app/daily_pipeline.py`.
- Confirm retired-model exclusions.
- Validate champion eligibility and recommendation outputs.
- Verify failure handling.

## Priority 3 — Trade-History Reconciliation

- Review OPEN research trades KOD, CNMD, and REZI.
- Reconstruct historical exits using documented trade rules.
- Verify exit dates and prices.
- Update model feedback only after reconciliation.

## Priority 4 — Professional Backtesting

- Build realistic historical backtesting.
- Implement walk-forward validation.
- Add transaction-cost assumptions.
- Compare against SPY and QQQ.
- Calculate drawdown, Sharpe, Sortino, and CAGR.
- Validate results across different market conditions.

## Priority 5 — Probability and Confidence Calibration

- Evaluate probability reliability.
- Analyze false positives.
- Improve confidence thresholds.
- Validate calibration out of sample.

## Priority 6 — Advanced Portfolio Intelligence

- Improve portfolio risk budgeting.
- Add sector exposure controls.
- Evaluate correlations.
- Refine position sizing.
- Introduce concentration limits.
- Evaluate volatility targeting.

## Priority 7 — Model Monitoring and Continuous Learning

- Monitor model degradation.
- Detect data and prediction drift.
- Establish controlled retraining triggers.
- Maintain champion/challenger comparisons.
- Introduce reproducible rollback procedures.

## Priority 8 — Paper Trading Preparation

- Validate the complete research pipeline.
- Verify trade tracking and risk controls.
- Implement realistic simulated execution.
- Monitor performance over a meaningful observation period.
- Keep paper trading separate from real-money execution.

**Development Rule:** Reuse and validate existing modules before creating new systems.

**Current Unfinished Task:** Model-governance integration and validation in `app/daily_pipeline.py`.

---

# 27. Final Rule

The platform should evolve like a professional quantitative research system.

Every improvement must answer:

1. Does it improve research quality?
2. Is it validated with evidence?
3. Does it reduce or control risk?
4. Is it reproducible?
5. Is it documented?
6. Does it integrate with the existing architecture?
7. Does it avoid creating duplicate functionality?

If the answer is no, the change should not be accepted until the issue is resolved.

The objective is not to build the model with the highest historical metric.

The objective is to build a **reliable, measurable, explainable, and continuously improving quantitative research platform.**
