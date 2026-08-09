# AI Trading Research Platform — Architecture & Development Update

**Last Updated:**

2026-08-08

---

# Purpose

This document records the current architecture, development state, model governance, trade intelligence system, and major engineering decisions for the AI Trading Research Platform.

The platform is an AI-assisted quantitative stock research system designed to:

* collect market data
* generate technical features
* train machine learning models
* generate current-market ML predictions
* rank trading opportunities
* combine multiple intelligence layers
* apply risk management
* generate structured trade plans
* track approved trades
* monitor open trades
* evaluate completed trades
* provide model feedback from real recorded trading outcomes
* evaluate model quality using both ML metrics and trading performance
* manage the current champion model

The platform is a **research and paper-trading development system**.

It is **not approved for automated real-money trading**.

Future live trading requires additional validation, including:

* extended paper trading
* walk-forward validation
* realistic transaction-cost modeling
* portfolio-level risk controls
* execution monitoring
* model monitoring
* rollback procedures
* operational reliability testing

---

# Major Architecture Update

The platform now consists of several connected intelligence layers rather than a single ML prediction system.

The current architecture separates:

1. Historical ML research
2. Current scanner ML prediction
3. Research ranking
4. AI decision making
5. Risk-aware trade management
6. Trade history
7. Open-trade monitoring
8. Completed-trade feedback
9. Model quality evaluation
10. Champion management

The system therefore evaluates models using both:

* traditional machine-learning metrics
* actual recorded trading performance

This distinction is important.

A model with excellent classification metrics is not automatically considered a good trading model.

---

# ML Architecture

The platform maintains two distinct ML paths.

These paths serve different purposes and must remain separate.

---

# ML Path 1 — Historical ML Prediction System

## Purpose

Train and evaluate machine-learning models using historical market data.

Main training module:

`app/train_model.py`

Historical dataset:

`data/historical_ml_dataset.csv`

The historical ML path is used for:

* model development
* historical pattern research
* chronological validation
* model comparison
* backtesting
* model registry evaluation

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

The historical ML path uses chronological validation rather than random splitting.

Required model metrics include:

* Accuracy
* Precision
* Recall
* F1
* ROC-AUC

Trading evaluation should also include:

* number of trades
* win rate
* average return
* drawdown
* risk-adjusted metrics

---

# ML Path 2 — Scanner ML Prediction System

## Purpose

Provide machine-learning predictions for current scanner candidates.

Main modules:

`app/ml_predictor.py`

`app/model_loader.py`

This path operates on current scanner opportunities.

It uses the current scanner feature set and produces prediction information used by the AI research pipeline.

Outputs include:

* ML_Probability
* ML_Prediction
* ML_Model
* ML_F1
* ML_Accuracy

The scanner ML prediction is combined with other research intelligence rather than being used as an isolated trading decision.

---

# Historical ML Integration

Historical ML information is also incorporated separately into the research pipeline.

Function:

`add_historical_ml_predictions()`

Output:

`Historical_ML_Probability`

Purpose:

Compare current opportunities with historical patterns.

The research system can therefore consider:

* current scanner ML probability
* historical ML probability
* research ranking
* AI confidence
* risk/reward
* market conditions

This creates a multi-layer research signal.

---

# Model Governance

The platform now treats model governance as a separate responsibility from model training.

Relevant components include:

* `app/model_registry.py`
* `app/model_quality_evaluator.py`
* `app/champion_manager.py`
* `app/model_champion_tracker.py`
* `app/model_feedback_loop.py`

Model selection is no longer based solely on training or classification metrics.

A model must demonstrate meaningful trading evidence before it can become the recommended champion.

---

# Model v27 Retirement

Previous model:

`model_v27`

Status:

**RETIRED**

`model_v27` is no longer considered a valid benchmark for future model comparison.

Its previously reported metrics were:

Accuracy:

98.3%

F1:

96.1%

These results were subsequently considered unreliable because of concerns including:

* insufficient dataset size
* possible data leakage
* unrealistic validation
* biased historical representation
* overly optimistic classification results

The project therefore explicitly excludes `model_v27` from future model-quality evaluation.

Important principle:

> High ML classification metrics do not automatically demonstrate useful trading performance.

Future models must be evaluated using realistic validation and actual trading evidence.

---

# Current Champion Model

Current champion:

`model_v33`

Champion model file:

`data/models/champion_model.pkl`

Current champion manager result:

`model_v33`

The current champion was confirmed by:

`app/champion_manager.py`

Current status:

**CHAMPION**

The champion system reports:

* Best model: `model_v33`
* Current champion: `model_v33`
* Champion unchanged

---

# Model v33 Historical Research Results

The original historical acceptance experiment for `model_v33` recorded:

Algorithm:

Random Forest

Configuration:

* n_estimators: 500
* max_depth: 20
* min_samples_leaf: 10
* max_features: sqrt
* class_weight: balanced

Historical evaluation:

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

These values represent the historical experiment used when `model_v33` was initially accepted.

They should not be confused with the platform's later recorded trade-history results.

---

# Current Recorded Trading Performance

The current model feedback report records completed trades associated with `model_v33`.

Source:

`data/models/model_feedback_report.csv`

Current recorded result:

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

Stored model metrics:

Accuracy:

98.3%

F1:

96.1%

The stored classification metrics are historical model metrics and are therefore kept separate from current trading outcomes.

The current trading results are the more relevant evidence for evaluating whether the model is useful in the trading system.

---

# Model Quality Evaluation

Module:

`app/model_quality_evaluator.py`

Output:

`data/models/model_quality_report.csv`

Recommended champion:

`data/models/recommended_champion.txt`

The evaluator combines:

* F1
* Win Rate
* Average Return
* Completed Trades

The current architecture also applies a trading eligibility requirement.

A model must have:

`Completed_Trades > 0`

to be considered trading-eligible.

Models without completed trading history cannot become the recommended champion.

The system therefore prevents models from winning solely because they have high F1 or other historical classification metrics while having no actual recorded trading evidence.

---

# Trading Quality Score

The current quality evaluation uses:

F1:

40%

Win Rate:

30%

Average Return:

20%

Completed-trade evidence:

10%

Models without completed trades receive:

`Trading_Quality_Score = 0`

This prevents untested models from becoming the recommended champion.

Current evaluation result:

`model_v33` is the recommended model because it is currently the only model with qualifying completed trading history in the evaluated model set.

---

# Champion Management

Module:

`app/champion_manager.py`

Purpose:

Compare the recommended model against the current champion and update champion status when appropriate.

Current result:

Best model:

`model_v33`

Current champion:

`model_v33`

Status:

**Champion unchanged.**

The champion management layer therefore confirms that the current champion remains `model_v33`.

---

# Champion Tracking

Module:

`app/model_champion_tracker.py`

Output:

`data/models/model_champion_status.csv`

The current champion status records:

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

The champion-tracking record represents the current model-governance state and should be distinguished from older historical model experiments.

---

# AI Decision Pipeline

The AI research pipeline now contains multiple intelligence layers.

Current conceptual flow:

Market Data

↓

Technical Features

↓

Research Ranking

↓

Scanner ML Prediction

↓

Historical ML Evidence

↓

AI Confidence

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

↓

Trade History

↓

Open-Trade Monitoring

↓

Completed Trade Outcome

↓

Model Feedback

↓

Model Quality Evaluation

↓

Champion Management

This creates a feedback-oriented research architecture.

---

# Research Intelligence Layer

Core components include:

* `app/research_ranker.py`
* `app/ai_score_engine.py`
* `app/ai_decision.py`
* `app/ai_final_decision_controller.py`

Responsibilities:

* opportunity ranking
* technical signal interpretation
* ML confirmation
* confidence evaluation
* decision explanation
* final research classification

The research layer does not independently execute real-money trades.

---

# AI Decision Engine

Module:

`app/ai_decision.py`

Purpose:

Generate AI research decisions from multiple inputs.

Inputs can include:

* AI Final Score
* AI Confidence
* ML Probability
* Historical ML Probability
* Risk/Reward
* Market conditions

Possible decision levels include:

* HIGH CONVICTION
* STRONG CANDIDATE
* CANDIDATE
* WATCHLIST
* PASS

The engine also generates explanations for decisions.

Examples include:

* strong technical ranking
* strong current ML confirmation
* historical patterns support setup
* positive risk/reward

---

# AI Final Decision Controller

Module:

`app/ai_final_decision_controller.py`

Purpose:

Provide the final approval layer before trade management.

Inputs include:

* optimized rankings
* ML information
* confidence information
* portfolio risk decisions

The final conviction score combines:

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

Confidence levels:

* HIGH
* MEDIUM
* LOW

---

# Trade Management

Module:

`app/trade_management.py`

Purpose:

Convert approved research opportunities into structured trade plans.

The trade-management layer can calculate:

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

Trades require appropriate approval conditions before being accepted into trade tracking.

---

# Trade History Architecture

Module:

`app/trade_history.py`

Database:

`data/trade_history.csv`

The trade-history system is now the central recorded-trade database.

It stores:

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

`add_new_trades()`

Only rows with:

`Final_AI_Status == "APPROVED TRADE"`

are added as new trades.

The system also prevents duplicate open trades for the same symbol.

Each new trade records:

* entry information
* risk levels
* AI decision information
* ML information
* model information
* portfolio allocation
* position size
* capital allocation

The initial status is:

`OPEN`

---

# Open Trade Monitoring

Module:

`app/live_trade_monitor.py`

The live monitor reads:

`data/analysis/final_ai_signals.csv`

It verifies that required price fields exist:

* Symbol
* Close

The monitor loads the trade history and displays currently open positions.

For each open trade it tracks:

* Entry Price
* Current Price
* Stop Loss
* Target 1
* Days Held

It then updates the open trades using current scanner prices.

---

# Trade Exit Logic

Module:

`app/trade_history.py`

Open trades are automatically evaluated against:

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

This provides the completed-trade evidence used by the model feedback system.

---

# Trade Performance Calculation

For a closed trade:

Return is calculated as:

`(Exit_Price - Entry_Price) / Entry_Price * 100`

Profit is calculated using:

`Return_% × Capital_Allocation_$`

This creates a direct connection between trade outcomes and recorded capital allocation.

---

# Model Feedback Loop

Module:

`app/model_feedback_loop.py`

Output:

`data/models/model_feedback_report.csv`

Purpose:

Evaluate model performance using completed trades recorded in the trade-history database.

The feedback loop:

1. Loads `data/trade_history.csv`
2. Selects closed trades
3. Groups completed trades by `Model_Name`
4. Calculates trading performance
5. Records model metrics
6. Produces a model feedback report

Current calculated trading metrics include:

* Completed Trades
* Winning Trades
* Losing Trades
* Win Rate
* Average Return
* Best Trade
* Worst Trade

Stored model metrics are also included when available:

* Model Accuracy
* Model F1

This creates the foundation for outcome-based model monitoring.

---

# Daily Pipeline

Main controller:

`app/daily_pipeline.py`

The daily pipeline executes the major research stages sequentially.

Current pipeline stages include:

1. Running Integrated Scanner
2. Saving Signal History
3. Running Forward Test
4. Updating Trade Database
5. Generating AI Rankings
6. Generating AI Decisions
7. Generating AI Report
8. Updating Model Feedback Loop
9. Updating Model Champion Tracker

The pipeline records:

* current status
* current step
* completed steps
* failed step
* start time
* end time
* duration

Status file:

`data/logs/pipeline_status.json`

Log file:

`data/logs/daily_pipeline.log`

If a pipeline step fails, the pipeline stops and records the failed step.

---

# Model Feedback in the Daily Pipeline

The daily pipeline now connects trading outcomes to model monitoring.

The relevant sequence is:

Trade Database

↓

AI Decisions

↓

Trade History

↓

Completed Trade Outcomes

↓

Model Feedback Loop

↓

Model Champion Tracker

This allows model performance to be evaluated from actual recorded outcomes rather than classification metrics alone.

---

# Risk Management

Risk management remains integrated into final trade evaluation.

The system considers:

* portfolio risk
* position sizing
* stop-loss distance
* capital allocation
* trade approval
* reward/risk
* expected value

Future risk improvements include:

* volatility targeting
* correlation analysis
* sector exposure limits
* dynamic position sizing
* portfolio-level risk budgeting

---

# Current Architecture Layers

## Layer 1 — Data Engineering

Responsibilities:

* market data collection
* historical data storage
* feature generation
* scanner data preparation

Status:

**Foundation complete**

---

## Layer 2 — Machine Learning

Responsibilities:

Historical ML:

* model training
* chronological validation
* model comparison
* historical evaluation

Scanner ML:

* current prediction
* candidate scoring
* ML confirmation

Status:

**Foundation complete**

---

## Layer 3 — Research Intelligence

Components:

* `research_ranker.py`
* `ai_score_engine.py`
* `ai_decision.py`
* `ai_final_decision_controller.py`

Responsibilities:

* opportunity ranking
* confidence evaluation
* ML integration
* decision explanation

Status:

**Active development**

---

## Layer 4 — Risk and Trade Management

Components:

* `trade_management.py`
* portfolio risk modules
* trade approval logic

Responsibilities:

* risk filtering
* position sizing
* stop-loss calculation
* target calculation
* capital allocation
* trade planning

Status:

**Developing**

---

## Layer 5 — Trade Intelligence

Components:

* `trade_history.py`
* `live_trade_monitor.py`
* `trade_feedback.py`
* `trade_performance_tracker.py`

Responsibilities:

* trade tracking
* open-position monitoring
* exit evaluation
* outcome recording
* performance analysis

Status:

**Active foundation**

---

## Layer 6 — Model Feedback and Governance

Components:

* `model_feedback_loop.py`
* `model_quality_evaluator.py`
* `model_champion_tracker.py`
* `champion_manager.py`

Responsibilities:

* completed-trade model evaluation
* trading-quality scoring
* model eligibility
* champion recommendation
* champion tracking

Status:

**Active**

---

# Current End-to-End Architecture

The current platform can be represented as:

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

AI Decision

↓

Risk Evaluation

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

Champion Manager

↓

Current Champion

↓

Future Model Evaluation

This creates a continuous research loop.

---

# Current Development Priority

## Phase 3 — AI Research Engine

The original AI decision architecture is now substantially implemented.

Current priorities are no longer basic pipeline construction.

The next focus is validation and improvement.

Priority:

1. Confidence calibration
2. False-positive reduction
3. Historical score validation
4. Walk-forward validation
5. Professional backtesting
6. Model monitoring
7. Portfolio-level risk validation

---

# Phase 4 — Professional Backtesting

Priority:

**High**

Required capabilities:

* walk-forward validation
* benchmark comparison
* transaction-cost simulation
* equity curves
* maximum drawdown
* Sharpe ratio
* Sortino ratio
* CAGR
* realistic entry/exit assumptions

The purpose is to determine whether the complete research strategy remains useful under realistic historical conditions.

---

# Phase 5 — Portfolio Intelligence

Future capabilities:

* correlation analysis
* sector exposure limits
* portfolio optimization
* risk budgeting
* portfolio-level position constraints
* concentration control

---

# Phase 6 — Model Monitoring

Planned capabilities:

* feature drift detection
* prediction drift
* model health scoring
* automatic retraining triggers
* champion/challenger monitoring
* rollback system

The existing trade-feedback architecture provides the foundation for this phase.

---

# Model Governance Rules

Every future model must record:

## Dataset

* dataset file
* dataset size
* date range
* feature set

## Training

* algorithm
* parameters
* training date
* model version

## Evaluation

* Accuracy
* Precision
* Recall
* F1
* ROC-AUC

## Trading

* completed trades
* win rate
* average return
* best trade
* worst trade
* drawdown
* risk metrics

## Decision

One of:

* Accepted
* Rejected
* Retired

The reason for the decision must be documented.

---

# Development Rules

Before changing ML architecture, review:

* `docs/MODEL_HISTORY.md`
* `docs/EXPERIMENT_LOG.md`
* `docs/ARCHITECTURE.md`

Never:

* reintroduce `model_v27` as a benchmark
* optimize only for accuracy
* accept unrealistic validation
* treat classification metrics as proof of trading usefulness
* create duplicate model-management systems without architectural justification

New modules must:

* have one clear purpose
* avoid duplicate functionality
* connect to the existing architecture
* preserve reproducibility
* be tested independently
* be documented when they become part of the active pipeline

---

# Current Development Workflow

Before committing changes:

```text
git status
```

Test changed modules individually:

```text
python -m app.module_name
```

Run the relevant pipeline or evaluator.

Review generated outputs.

Update documentation.

Then:

```text
git add .
git commit -m "Description of change"
git push
```

---

# Current Project State

The platform has evolved from:

Stock Scanner

↓

ML Prediction System

↓

AI Research Engine

↓

Risk-Aware Trading Research Platform

↓

Outcome-Based Model Feedback System

The current system now contains:

✓ Market data pipeline

✓ Historical ML foundation

✓ Scanner ML prediction

✓ Model registry

✓ Research ranking

✓ AI scoring

✓ AI decision layer

✓ Risk-aware trade planning

✓ Trade history database

✓ Open-trade monitoring

✓ Automated trade outcome calculation

✓ Model feedback loop

✓ Trading-based model quality evaluation

✓ Champion management

✓ Daily pipeline status tracking

---

# Current Champion State

Current champion:

`model_v33`

Retired model:

`model_v27`

`model_v27` must not be used as a benchmark for future champion selection.

Current model-quality evaluation identifies `model_v33` as the recommended champion because it has qualifying completed trading history.

The current recorded trading evidence for `model_v33` is:

* 272 completed trades
* 30.88% win rate
* 2.65% average return
* 70.30% best trade
* -9.96% worst trade

These results should be treated as current recorded trading evidence, not as proof that the strategy is ready for live trading.

---

# Next Major Milestone

The next major milestone is:

**Professional validation before paper trading.**

The system should now focus less on adding additional layers and more on determining whether the existing layers produce reliable results.

Required validation:

* walk-forward testing
* realistic backtesting
* transaction costs
* benchmark comparison
* drawdown analysis
* risk-adjusted returns
* confidence calibration
* false-positive analysis
* model drift monitoring

Only after these validations should the project progress toward extended paper trading.

---

# Final Development Principle

The system should behave like a quantitative research platform.

Success is measured by:

* realistic validation
* repeatable experiments
* controlled risk
* transparent decisions
* recorded outcomes
* evidence-based model selection
* continuous improvement

The objective is not perfect prediction.

The objective is to determine whether the complete research system can consistently improve decision quality through:

* historical evidence
* machine learning
* quantitative validation
* AI reasoning
* risk analysis
* trade outcome feedback
* controlled model evolution

The platform should prefer **credible evidence over impressive metrics**.
