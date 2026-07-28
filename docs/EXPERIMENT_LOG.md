\# AI Trading Research Platform — Experiment Log



\## Purpose



This document tracks important engineering experiments,

changes, tests, and their outcomes.



Each experiment should record:



\- Date

\- Objective

\- Files changed

\- Dataset/model impact

\- Result

\- Decision

\- Next action





\---



\# Experiment History





\## EXP-001 — Initial Scanner Development



Date:

2026-07



Objective:

Build first automated stock scanning pipeline.



Changes:

\- Created stock universe builder

\- Added Yahoo price collection

\- Added technical indicators

\- Created scanner pipeline



Result:

Successfully generated technical stock signals.



Decision:

Continue expanding into ML prediction system.





\---



\## EXP-002 — Historical Feature Dataset Creation



Date:

2026-07



Objective:

Create historical training data for machine learning.



Changes:

\- Built feature\_history\_builder.py

\- Generated historical feature files

\- Created historical\_ml\_dataset.csv



Dataset:



Stocks:

\~4,000



Rows:

220,849+



Features:

\- Returns

\- RSI

\- SMA

\- Volume metrics

\- Volatility

\- Momentum





Result:

Created foundation ML dataset.



Decision:

Proceed with supervised learning.





\---



\## EXP-003 — First ML Models



Objective:

Train prediction models for successful trades.



Models tested:



\- Logistic Regression

\- Random Forest





Evaluation:



Metrics:

\- Accuracy

\- Precision

\- Recall

\- F1

\- ROC-AUC





Result:

Random Forest performed better for trade recall.



Decision:

Use champion/challenger system.





\---



\## EXP-004 — Model v27 Investigation



Date:

2026-07



Objective:

Review previous champion model.



Model:

model\_v27





Original metrics:



Accuracy:

98.3%



F1:

96.1%





Finding:



Model likely affected by:



\- Small dataset

\- Data leakage

\- Bias





Decision:



Retire model\_v27 as unreliable.



New models must be trained using:



\- Larger historical dataset

\- Improved features

\- Leakage prevention

\- Realistic validation





Status:

Completed





\---



\## EXP-005 — Expanded Dataset Retraining



Objective:



Retrain models using improved dataset.





Changes:



Added:



\- ATR

\- ATR\_Percent

\- Range\_Position

\- Distance\_From\_52W\_High

\- Volume\_Trend





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

0.448





Decision:



Accepted as new champion because previous model was unreliable.





\---



\## EXP-006 — Automatic Threshold Optimization



Status:

In Progress





Objective:



Replace manually selected filters:



AI\_Confidence > 40

ML Probability > 25

Rank > 50





with data-driven thresholds.





Files:



app/historical\_threshold\_optimizer.py





Goal:



Create:



data/models/optimal\_thresholds.json





Status:



Improving optimizer logic.





\---



\# Future Experiments



\## EXP-007 — Probability Calibration



Status:

Planned





\## EXP-008 — SHAP Explainability



Status:

Planned





\## EXP-009 — Walk Forward Validation



Status:

Planned



\---



\## Historical Threshold Optimizer v1.1



Date:

2026-07-28



Changes:



\- Removed duplicate candidate generation function

\- Improved trade deduplication logic

\- Added validation for minimum trade requirements



Reason:



The optimizer was producing results but required cleanup before further research.



Previous issues:



\- Duplicate function definitions created unnecessary code duplication

\- Trade deduplication could keep weaker signals when multiple signals existed for the same symbol/date

\- Additional validation was needed before metric calculation



Improvements:



\- Candidate generation now uses one standardized percentile-based function

\- Duplicate trades now keep the highest Rank\_Score setup

\- Threshold evaluation rejects insufficient trade samples



Expected impact:



\- More reliable threshold optimization

\- Reduced bias from duplicate signals

\- Better reproducibility for future experiments



Status:



Completed



