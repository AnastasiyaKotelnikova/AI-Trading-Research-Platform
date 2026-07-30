# AI Trading Research Platform — Experiment Log


## Purpose


This document tracks important engineering experiments,

changes, tests, and their outcomes.


Each experiment should record:


- Date

- Objective

- Files changed

- Dataset/model impact

- Result

- Decision

- Next action



---

# Experiment History



## EXP-001 — Initial Scanner Development


Date:

2026-07


Objective:

Build first automated stock scanning pipeline.


Changes:

- Created stock universe builder

- Added Yahoo price collection

- Added technical indicators

- Created scanner pipeline


Result:

Successfully generated technical stock signals.


Decision:

Continue expanding into ML prediction system.



---

## EXP-002 — Historical Feature Dataset Creation


Date:

2026-07


Objective:

Create historical training data for machine learning.


Changes:

- Built feature_history_builder.py

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

Created foundation ML dataset.


Decision:

Proceed with supervised learning.



---

## EXP-003 — First ML Models


Date:

2026-07


Objective:

Train prediction models for successful trades.


Models tested:


- Logistic Regression

- Random Forest


Evaluation:


Metrics:

- Accuracy

- Precision

- Recall

- F1

- ROC-AUC


Result:

Random Forest performed better for trade recall.


Decision:

Use champion/challenger system.



---

## EXP-004 — Model v27 Investigation


Date:

2026-07


Objective:

Review previous champion model.


Model:

model_v27


Original metrics:


Accuracy:

98.3%


F1:

96.1%


Finding:


Model likely affected by:


- Small dataset

- Data leakage

- Biased historical representation

- Unrealistic validation


Decision:


Retire model_v27 as unreliable.


New models must be trained using:


- Larger historical dataset

- Improved features

- Leakage prevention

- Realistic validation


Status:

Completed



---

## EXP-005 — Expanded Dataset Retraining


Date:

2026-07


Objective:


Retrain models using improved dataset.


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


Results:


Random Forest:


F1:

0.467


ROC-AUC:

0.669


Backtest:


Trades:

210


Average Return:

0.448%


Decision:


Accepted as new champion because previous model was unreliable.



---

# AI Research Engine Experiments



## EXP-006 — Automatic Threshold Optimization


Date:

2026-07


Status:

Completed / Improving


Objective:


Replace manually selected filters with data-driven optimization.


Previous manual filters:


- AI_Confidence > 40

- ML Probability > 25

- Rank > 50


Files:


app/historical_threshold_optimizer.py


Goal:


Create:


data/models/optimal_thresholds.json


Implemented:


- Historical threshold evaluation

- Multiple optimization profiles

- Risk-adjusted scoring

- Expectancy calculation

- Drawdown consideration


Result:


Optimizer successfully evaluates historical filtering performance.


Decision:


Continue improving threshold selection before automatic deployment.



---

---

## EXP-007 — Research Score Normalization V3


Date:

2026-07-29


Objective:

Improve Research Score quality by removing score inflation and creating a normalized research ranking system.


Problem:

Previous Research Score calculation:

- directly added Rank Score
- strategy bonuses
- sector bonuses
- risk reward bonuses
- RSI bonuses


Result:

Scores exceeded expected range:

Examples:

Research_Score > 100


Problems:

- poor comparability
- threshold optimization distortion
- ranking saturation


Changes:


Updated:

app/research_ranker.py


Implemented:

- normalized Research Score calculation
- improved factor weighting
- controlled scoring range
- better distribution


New Distribution:


Minimum:

35.04


Maximum:

77.15


Average:

53.98



Impact:


Improved:

✓ score interpretability

✓ ranking separation

✓ threshold optimization readiness

✓ historical validation compatibility


Decision:

Accept Research Ranker V3.


Next action:


Continue optimizing:

- AI Final Score weighting
- Confidence calibration
- historical score validation


Status:

Completed

---



---

EXP-008 — Research Score Calibration Validation

Date:
2026-07-29

Objective:
Validate whether Research_Score ranking correlates with future trade performance.

Dataset:
data/trade_database.csv

Rows:
20,420 trades

Method:
Quartile bucket analysis

Results:

Research Score buckets:

Top:
944 trades
Average Return:
+7.98%

High:
767 trades
Average Return:
+3.48%

Medium:
1003 trades
Average Return:
-0.92%

Low:
1298 trades
Average Return:
+1.05%


Finding:

Research_Score demonstrates meaningful ranking ability.
Higher Research Scores produced significantly higher average returns.

Decision:

Accept Research_Score V3 as improved ranking model.

Next:

Validate AI_Final_Score using historical trade database after adding score persistence.

---

# EXP-009 — Research Ranker V2


Date:

2026-07-29


Objective:


Improve Research Score calculation and move from simple bonus scoring toward multi-factor ranking.


Previous approach:


Research Score was calculated using:


- Rank Score

- Strategy bonuses

- Sector bonuses

- Risk reward bonuses

- RSI bonus


Problems discovered:


- Score compression

- Limited separation between candidates

- Several features behaved like constants


Changes:


Updated:


app/research_ranker.py


New ranking factors:


- Rank Score

- Momentum Score

- Trend Score

- Relative Strength

- Risk Reward

- Strategy classification


Result:


Research ranking became more structured and transparent.


Example:


Previous Research Score range:


75-88


New system:


More flexible multi-factor scoring framework.


Decision:


Continue improving with percentile normalization.



---

## EXP-010 — Research Feature Distribution Analysis


Date:

2026-07-29


Objective:


Analyze whether ranking features provide enough separation between trading candidates.


Dataset:


data/analysis/strategy_results.csv


Sample size:


68 candidates


Findings:


Rank Score:


Mean:

80.29


Range:

75-88


Observation:


Score distribution was compressed.


Momentum Score:


Mean:

20.66


Range:

20-25


Observation:


Most candidates receive similar momentum scores.


Trend Score:


Mean:

19.70


Range:

10-20


Observation:


Trend score provides limited differentiation.


Relative Strength:


Mean:

16.90


Range:

10.18-28.75


Observation:


Relative Strength provides stronger candidate separation.


Risk Reward:


Mean:

3.67


Maximum:

36.84


Observation:


Extreme values require normalization or capping.


Decision:


Research Score normalization is required before AI Final Score optimization.



---

# Future Experiments



## EXP-011 — Research Score Normalization V3


Status:

Next Development


Objective:


Convert raw research factors into normalized percentile-based scores.


Planned improvements:


- percentile scaling

- feature weighting

- risk reward normalization

- improved score distribution

- validation against historical outcomes



---

## EXP-012 — Probability Calibration


Status:

Planned



Objective:


Improve confidence reliability so predicted probabilities better match historical success rates.



---

## EXP-013 — SHAP Explainability


Status:

Planned



Objective:


Add model explainability and feature contribution analysis.



---

## EXP-014 — Walk Forward Validation


Status:

Planned



Objective:


Create realistic out-of-sample testing using historical market periods.



---

# Experiment Rules


Before accepting any major improvement:


- Validate with historical data

- Avoid data leakage

- Compare against previous version

- Record results

- Update architecture documentation


The platform prioritizes realistic research performance over artificially high metrics.
