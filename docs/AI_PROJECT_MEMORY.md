# AI Trading Research Platform — Project Memory

Last Updated:

2026-07-29


Repository:

AI-Trading-Research-Platform


GitHub:

https://github.com/AnastasiyaKotelnikova/AI-Trading-Research-Platform


Local Path:

C:\Users\anast\scanner-project



# 1. Project Mission


This project is a personal AI-assisted stock trading research platform.


The goal is not to create a guaranteed prediction system.


The goal is to build a quantitative research assistant that:


- collects market data
- generates technical features
- learns historical market patterns
- evaluates trade quality
- ranks trading opportunities
- explains AI decisions
- manages portfolio research
- monitors model performance
- improves through historical feedback and retraining


Long-term vision:


Market Data

↓

Feature Engineering

↓

Scanner Signals

↓

Machine Learning Models

↓

Historical Pattern Analysis

↓

AI Research Ranking

↓

Trade Quality Filtering

↓

AI Decision Engine

↓

Portfolio Intelligence

↓

Performance Monitoring

↓

Model Improvement



The platform is designed as a quantitative research system rather than a simple stock scanner.



# 2. Development Environment


Operating System:

Windows


Python:

3.11.9


Virtual Environment:

venv


Run modules:

python -m app.module_name


Main project folder:

C:\Users\anast\scanner-project


Development Tools:

- VS Code
- Git
- GitHub
- Jupyter
- Pandas
- NumPy
- Scikit-learn
- PyTorch
- Matplotlib



# 3. Current Development Phase


Current Phase:

Phase 3 — AI Research Engine


Estimated Completion:

~90%


Overall Platform Completion:

Approximately 70%


Current Focus:


- AI ranking improvement
- confidence calibration
- research score normalization
- historical validation
- risk adjustment
- threshold optimization
- professional backtesting
- model monitoring


Current development direction:


The project has evolved beyond a scanner.

It is becoming a quantitative research platform containing:


- machine learning prediction
- historical intelligence
- AI analysis
- portfolio decision support
- automated research reports
- continuous optimization



# 4. Completed Development



# Phase 1 — Data Engineering


Status:

COMPLETE


Completed:


✓ Historical market data collection

✓ Price history storage

✓ Feature generation

✓ Feature history database

✓ ML dataset builder

✓ Daily pipeline automation

✓ Historical dataset expansion


Main components:


app/price_history_collector.py

app/feature_history_builder.py

app/historical_ml_builder.py

app/daily_pipeline.py




# Phase 2 — Machine Learning Foundation


Status:

COMPLETE


Completed:


✓ ML training pipeline

✓ Feature selection

✓ Model evaluation

✓ Model versioning

✓ Champion model system

✓ ML prediction pipeline

✓ Backtesting integration

✓ ROC-AUC evaluation

✓ Chronological validation

✓ Improved model comparison logic

✓ Historical return evaluation


Main components:


app/train_model.py

app/model_registry.py

app/ml_predictor.py

app/ml_backtest.py




# 5. Machine Learning Evolution



## Retired Model


Model:

model_v27


Status:

RETIRED


Reason:


The model showed unrealistic performance:


Accuracy:

98.3%


F1:

96.1%


Problems discovered:


- trained on smaller dataset
- possible data leakage
- biased historical representation
- unrealistic validation results


Decision:


model_v27 is not used as a performance benchmark.



The project now prioritizes realistic validation over artificially high metrics.




# Current ML Approach


Dataset:


data/historical_ml_dataset.csv


Validation method:


Chronological split


Purpose:


Reduce future information leakage and simulate realistic market conditions.


Models are evaluated using:


- classification performance
- trading performance
- historical returns
- win rate
- risk-adjusted results



# 6. Current Champion Model



Latest Accepted Model:


model_v33



Algorithm:


Random Forest



Configuration:


n_estimators:

500


max_depth:

20


min_samples_leaf:

10


max_features:

sqrt


class_weight:

balanced



Performance:


ROC-AUC:

0.669


F1:

0.467


Accuracy:

0.551



Backtest:


Trades:

210


Win Rate:

46.7%


Average Return:

0.448%



Champion selection considers:


- F1 score
- ROC-AUC
- average return
- win rate
- reliability


Models are no longer accepted only because of classification metrics.



# 7. Current Feature Set



## Volume Features

- Volume
- Average_Volume
- RVOL
- Volume_Trend


## Return Features

- Return_5D
- Return_10D
- Return_20D


## Momentum Features

- Momentum_Acceleration


## Technical Indicators

- RSI
- RSI_Change
- SMA20
- SMA50
- Above_SMA20
- Above_SMA50
- SMA_Gap


## Volatility Features

- Volatility_20D
- ATR
- ATR_Percent


## Position Features

- Range_Position
- Distance_From_52W_High


## Research Features

- Research Score
- Rank Score
- Confidence Score
- Risk Reward
- Historical Trade Results
- Strategy Classification



# 8. AI Research Engine



Status:

Advanced Development (~90% complete)



The AI Research Engine is the intelligence layer of the platform.



It combines:


- technical analysis
- machine learning probability
- historical trade outcomes
- risk analysis
- ranking systems
- decision logic



Goal:


"Which stocks have the highest-quality historical setup characteristics?"



The system evaluates probability, quality, and risk.

It does not predict guaranteed winners.



## Completed Components


✓ AI ranking system

✓ Research scoring engine

✓ AI confidence system

✓ Historical ML probability integration

✓ Trade quality filtering

✓ AI final decisions

✓ Automated research reports

✓ Trade explanations

✓ Historical setup analysis



Main components:


app/ai_ranker.py

app/ai_score_engine.py

app/ai_decision_engine.py

app/ai_final_decision_controller.py

app/ai_investment_analyst.py

app/ai_trade_explanation_engine.py

app/trade_quality_filter.py



## Current Research Ranking System


Evaluates:


- Research Score
- Rank Score
- Strategy quality
- Risk/Reward
- RSI conditions
- Historical performance
- Momentum
- Trend strength



Output:


data/analysis/research_ranked.csv



Current capabilities:


✓ ranks opportunities

✓ compares setups historically

✓ identifies stronger candidates

✓ provides research scores



# 9. Historical Intelligence System



Status:

Implemented



The platform now stores historical trade outcomes and uses them as learning information.



File:


data/historical_trade_database.csv



Purpose:


Create a historical memory system that evaluates:


- which setups work
- which strategies fail
- which scores predict successful trades
- which filters improve results



Current database:


Records:

1000+



Stored information:


- Symbol
- Entry price
- Exit price
- Return %
- Highest price
- Lowest price
- Target levels
- Stop loss
- Result
- Sector
- Signal
- Strategy
- Research Score
- Confidence Score
- Rank Score
- Momentum Score
- Trend Score
- Relative Strength
- Risk Reward
- RSI
- Return_5D
- Return_20D
- Distance from High
- SMA position
- Breakout status
- Overextended status
- Test date



Main component:


app/historical_trade_database.py



Current status:


Initial historical intelligence system completed.



Future improvements:


- larger historical dataset
- multi-year testing
- strategy performance tracking
- market regime analysis
- sector analysis



# 10. Historical Threshold Optimizer



Current module:


app/historical_threshold_optimizer.py



Purpose:


Automatically search for better decision thresholds using historical outcomes.



Optimization targets:


- Rank Score
- Confidence Score
- Research Score
- Risk Reward



Evaluation metrics:


- Win Rate
- Average Return
- Profit Factor
- Expectancy
- Maximum Drawdown
- Sharpe-like score
- Reliability Score
- Consistency Score



Optimization profiles:



## AGGRESSIVE


Purpose:


More opportunities with lower filtering.


Settings:


Minimum trades:

100


Minimum symbols:

10


Minimum win rate:

25%



## BALANCED


Purpose:


Default research profile.


Focus:


- reasonable trade count
- quality filtering
- acceptable risk


Settings:


Minimum trades:

125


Minimum symbols:

10


Minimum win rate:

30%



## CONSERVATIVE


Purpose:


Higher confirmation requirements.


Settings:


Minimum trades:

200


Minimum symbols:

25


Minimum win rate:

45%



Current optimization results example:


Trades tested:

130


Symbols:

10


Win Rate:

30%


Average Return:

9.859%


Profit Factor:

4.917


Sharpe-like:

0.407


Optimizer Score:

111.92



Current limitations:


- dataset still limited
- duplicate threshold combinations exist
- thresholds not automatically deployed



Future improvements:


- percentile-based thresholds
- decimal threshold support
- automatic deployment
- walk-forward validation



# 11. Self Optimization System



Status:

Implemented



Main components:


app/self_optimization_engine.py

app/adaptive_ranking_optimizer.py



Purpose:


Analyze historical performance and adjust ranking intelligence.



Capabilities:


✓ strategy optimization weights

✓ optimization scoring

✓ ranking adjustments

✓ optimization confidence



Output:


data/models/self_optimization_weights.json



Future:


- automatic retraining triggers
- Bayesian optimization
- reinforcement learning experiments
- adaptive market regime weighting



# 12. Portfolio Intelligence



Status:

Early Development



The platform has expanded from individual stock analysis into portfolio research.



Main components:


app/portfolio_memory_engine.py

app/ai_portfolio_rebalancer.py



Capabilities:


✓ portfolio research memory

✓ candidate ranking

✓ allocation recommendations

✓ portfolio scoring



Future development:


- correlation analysis
- sector exposure limits
- risk budgeting
- volatility targeting
- portfolio optimization



# 13. Trading Strategy Profiles



The system supports multiple research profiles.



Available profiles:


## SCALP

Short-term opportunities.



## SWING

Multi-day technical setups.



## QUALITY

Higher quality research candidates.



## BREAKOUT

Momentum breakout setups.



## PREMARKET_SCALP

Early market momentum opportunities.



Profile management:


app/profiles.py

app/profile_manager.py

app/profile_filters.py



Profiles control:


- liquidity requirements
- price requirements
- volume conditions
- volatility conditions
- breakout rules
- risk filters



# 14. Reporting and Dashboard System



Status:

Implemented



Generated outputs:


✓ AI research reports

✓ HTML dashboards

✓ performance charts

✓ ranking summaries



Main folders:


data/reports/

data/charts/

data/analysis/



Dashboard information:


- market overview
- ranked opportunities
- AI decisions
- sector analysis
- performance information



Future:


- interactive Streamlit dashboard
- portfolio dashboard
- model monitoring dashboard



# 15. Important Data Files



Machine Learning Dataset:


data/historical_ml_dataset.csv



Trade Database:


data/trade_database.csv



Historical Trade Database:


data/historical_trade_database.csv



Models:


data/models/



Contains:


- trained models
- model registry
- optimization weights
- performance history



Research:


data/analysis/



Reports:


data/reports/



Charts:


data/charts/



# 16. Immediate Development Roadmap



## Priority 1 — AI Research Engine


Tasks:


1. Normalize Research Score

2. Optimize AI Final Score weighting

3. Calibrate confidence probabilities

4. Improve explainable AI

5. Add historical score validation



## Priority 2 — Professional Backtesting


Tasks:


- walk-forward validation
- SPY/QQQ benchmark comparison
- equity curve generation
- drawdown analysis
- Sharpe ratio
- Sortino ratio
- CAGR calculation



## Priority 3 — Model Monitoring


Tasks:


- model performance tracking
- feature drift detection
- automatic retraining triggers
- champion/challenger automation
- model rollback system



## Priority 4 — Portfolio Intelligence


Tasks:


- portfolio allocation
- correlation analysis
- sector exposure limits
- risk budgeting
- portfolio optimization



# 17. Professional Backtesting Status



Status:

Early Development



Completed:


✓ Forward testing engine

✓ Trade outcome tracking

✓ Historical return evaluation

✓ Win/loss analysis



Remaining:


- walk-forward validation
- benchmark comparison
- equity curve
- drawdown analysis
- Sharpe/Sortino metrics
- CAGR calculation



# 18. Model Monitoring Status



Status:

Planned / Early Framework



Future components:


- model registry improvements
- performance monitoring
- feature drift detection
- automatic retraining triggers
- champion/challenger automation
- rollback system



# 19. Development Philosophy



The platform is being developed as a quantitative research system, not a prediction engine.



Avoid:


- unrealistic accuracy metrics
- data leakage
- overfitting
- curve fitting
- accepting models only because of classification scores



Prefer:


- realistic validation
- historical testing
- reproducible experiments
- documented decisions
- continuous improvement



The objective is to build an AI research assistant that helps analyze markets and improve decision quality through data-driven learning.
