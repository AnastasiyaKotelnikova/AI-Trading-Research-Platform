\# AI Trading Research Platform - Project Status



Last Updated:

2026-07-28



\## Project Goal



Build an AI-assisted quantitative stock research platform for personal trading research.



The system is designed to:

\- collect market data

\- generate technical features

\- train machine learning models

\- rank trading candidates

\- evaluate strategies

\- monitor model performance

\- eventually support paper trading and possible automation



\---



\# Current Architecture



\## Data Pipeline



Status: COMPLETE ✅



Completed:

\- Historical price collection

\- Feature engineering

\- Feature history storage

\- ML dataset generation

\- Daily pipeline automation



\---



\# Historical Dataset



Current dataset:



File:

data/historical\_ml\_dataset.csv



Important:

\- Dataset was expanded significantly from initial version

\- Previous model versions trained on smaller datasets are considered unreliable

\- Earlier model\_v27 had possible data leakage and bias issues

\- Do not treat old metrics as production quality



\---



\# Machine Learning Status



Current Phase:

Phase 2 -> Phase 3 transition



\## Previous Champion Model



model\_v27



Status:

RETIRED ❌



Reason:

\- trained on insufficient data

\- possible data leakage

\- unrealistic metrics

\- F1 score 0.961 considered unreliable



Do not compare future models against v27.



\---



\## Current Training System



Training script:



app/train\_model.py



Models tested:

\- Logistic Regression

\- Random Forest



Current evaluation metrics:

\- Accuracy

\- Precision

\- Recall

\- F1

\- ROC-AUC

\- Backtest return

\- Win rate



Champion selection:

app/model\_registry.py



Current logic:

Weighted score using:

\- F1

\- ROC-AUC

\- Average Return

\- Win Rate



\---



\# Current Model



Latest trained model:



model\_v33



Status:

Champion candidate / current champion



Training:

\- Dataset: expanded historical dataset

\- Features:

&#x20; - Return features

&#x20; - RSI

&#x20; - SMA

&#x20; - Volume

&#x20; - ATR

&#x20; - Volatility

&#x20; - Momentum

&#x20; - Range position



Latest metrics:



ROC-AUC:

0.669



F1:

0.467



Backtest:

Trades: 210



Win Rate:

46.7%



Average Return:

0.448



\---



\# Current Problems To Fix



\## 1. Model evaluation



Need:

\- better validation methodology

\- walk-forward testing

\- avoid overfitting



\---



\## 2. Probability calibration



Need:

\- calibrated ML probabilities

\- confidence score improvement



\---



\## 3. Research Engine



In progress:



Need improvement:

\- AI ranking

\- score normalization

\- risk adjustment

\- explanation engine



\---



\# Important Development Rules



When continuing development:



1\. Do not trust model\_v27 metrics.

2\. Prefer models trained on expanded datasets.

3\. Always test with unseen future data.

4\. Avoid data leakage.

5\. Compare models using:

&#x20;  - predictive quality

&#x20;  - trading performance

&#x20;  - stability



\---



\# Current Roadmap Position



Phase 1:

Data Engineering

COMPLETE ✅



Phase 2:

ML Foundation

\~95% COMPLETE



Remaining:

\- Champion refinement

\- Probability calibration

\- Feature reports



Phase 3:

AI Research Engine

IN PROGRESS



Current focus:

Improve model quality and research scoring.



\---



\# Next Recommended Tasks



1\. Clean champion model history

2\. Improve model registry

3\. Add proper walk-forward validation

4\. Add probability calibration

5\. Improve AI ranking engine

6\. Build professional backtesting system



