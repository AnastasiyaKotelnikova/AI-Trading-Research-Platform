# AI Trading Research Platform — Experiment Log


Last Updated:

2026-08-03



# Purpose


This document tracks important engineering experiments, model changes, system improvements, validation tests, and architecture decisions.


Each experiment records:


- Date
- Objective
- Files changed
- Dataset/model impact
- Result
- Decision
- Next action



The purpose is to maintain:


- reproducibility
- transparency
- experiment history
- controlled development



---

# Experiment History



# EXP-001 — Initial Scanner Development


Date:

2026-07



Objective:


Build the first automated stock scanning pipeline.



Changes:


- Created stock universe builder
- Added Yahoo price collection
- Added technical indicators
- Created scanner pipeline



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


- Built historical feature pipeline
- Generated historical feature files
- Created historical_ml_dataset.csv



Dataset:


Stocks:

~4,000



Rows:

220,849+



Features:


- Returns
- RSI
- SMA
- Volume metrics
- Volatility
- Momentum



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


- Logistic Regression
- Random Forest



Metrics:


- Accuracy
- Precision
- Recall
- F1
- ROC-AUC



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



Reported metrics:


Accuracy:

98.3%



F1:

96.1%



Finding:


The results were considered unreliable.



Problems discovered:


- insufficient dataset size
- possible data leakage
- unrealistic validation
- biased historical representation



Decision:


Retire model_v27.



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


- ATR
- ATR_Percent
- Range_Position
- Distance_From_52W_High
- Volume_Trend



Dataset:


Training records:

3,504,289



Testing records:

98,034



Validation:


Chronological split.



Result:


Created more realistic ML evaluation framework.



Decision:


Continue model comparison using realistic metrics.



---

# EXP-006 — model_v33 Champion Selection


Date:

2026-07-28



Objective:


Select a reliable champion model using expanded data.



Model:


model_v33



Algorithm:


Random Forest



Configuration:


- n_estimators: 500
- max_depth: 20
- min_samples_leaf: 10
- max_features: sqrt
- class_weight: balanced



Results:


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



Decision:


Accepted as current historical ML champion.



Reason:


Improved reliability compared with retired model_v27.



---

# EXP-007 — Research Score Normalization V3


Date:

2026-07-29



Objective:


Improve Research Score quality.



Problem:


Previous scoring allowed inflated scores above expected ranges.



Issues:


- poor comparability
- ranking saturation
- threshold optimization problems



Changes:


Updated:


app/research_ranker.py



Implemented:


- normalized scoring
- improved factor weighting
- controlled score range
- better ranking separation



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


- ML_Probability
- ML_Prediction
- ML_Model



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


- multi-layer scoring
- risk integration
- ML confidence integration
- final BUY/WATCH/REJECT decision



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


- entry price
- ATR stop loss
- target calculation
- position sizing
- reward/risk calculation
- expected value calculation



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


- trade_history.py
- trade_history_manager.py
- trade_feedback.py
- trade_performance.py
- trade_performance_tracker.py
- trade_exit_manager.py
- live_trade_monitor.py
- ai_learning_engine.py



Purpose:


Track:


- decisions
- outcomes
- performance
- future improvement signals



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


- AI ranking
- portfolio risk
- final conviction scoring
- trade approval logic



Result:


Weak opportunities can now be rejected before trade planning.



Decision:


Accept risk-aware decision pipeline.



---

# Future Experiments



# EXP-014 — Probability Calibration


Status:


Planned



Objective:


Improve confidence reliability.



Goal:


Predicted probabilities should better match actual success frequency.



---

# EXP-015 — Walk Forward Validation


Status:


Planned



Objective:


Create professional out-of-sample testing.



Method:


Rolling historical validation.



---

# EXP-016 — SHAP Explainability


Status:


Planned



Objective:


Understand feature contribution and AI reasoning.



---

# EXP-017 — Professional Backtesting


Status:


Planned



Add:


- transaction costs
- benchmark comparison
- equity curves
- drawdown analysis
- Sharpe ratio
- Sortino ratio



---

# Experiment Rules


Before accepting improvements:


Required:


- validate with historical data
- avoid leakage
- compare against previous version
- document results
- update architecture documentation



The platform prioritizes:


realistic research performance over artificially high metrics.
