\# AI Trading Research Platform — Project Memory



Last Updated:

2026-07-28



Repository:

AI-Trading-Research-Platform



Local Path:

C:\\Users\\anast\\scanner-project





\# 1. Project Mission



This project is a personal AI-assisted stock trading research platform.



The goal is not to create a guaranteed prediction system.



The goal is to build a quantitative research assistant that:



\- collects market data

\- generates technical features

\- learns historical patterns

\- evaluates trade quality

\- ranks opportunities

\- explains decisions

\- monitors performance

\- improves through retraining





Long-term vision:



Market Data

&#x20;     ↓

Feature Engineering

&#x20;     ↓

Scanner Signals

&#x20;     ↓

Machine Learning Models

&#x20;     ↓

Historical Pattern Analysis

&#x20;     ↓

AI Ranking

&#x20;     ↓

Trade Quality Filtering

&#x20;     ↓

Portfolio Decisions

&#x20;     ↓

Performance Monitoring

&#x20;     ↓

Model Improvement





\# 2. Development Environment



Operating System:



Windows



Python:



3.11.9



Virtual Environment:



venv





Run application modules:



python -m app.module\_name





Main project folder:



C:\\Users\\anast\\scanner-project





\# 3. Current Development Phase



Current Phase:



Phase 3 — AI Research Engine





Estimated completion:



\~75%





Overall project completion:



Approximately 45-50%





Current focus:



Improving AI ranking, confidence calibration, risk adjustment, and research scoring.





\# 4. Completed Development





\## Phase 1 — Data Engineering



Status:



COMPLETE





Completed:



✓ Historical market data collection



✓ Price history storage



✓ Feature generation



✓ Feature history database



✓ ML dataset builder



✓ Daily data pipeline





Main components:



app/price\_history\_collector.py



app/feature\_history\_builder.py



app/historical\_ml\_builder.py



app/daily\_pipeline.py







\## Phase 2 — Machine Learning Foundation



Status:



Mostly Complete





Completed:



✓ ML training pipeline



✓ Feature selection



✓ Model evaluation



✓ Model versioning



✓ Champion model system



✓ ML predictions



✓ Backtesting integration





Main components:



app/train\_model.py



app/model\_registry.py



app/ml\_predictor.py



app/ml\_backtest.py







\# 5. Important Model History





\## Retired Model



Model:



model\_v27





Status:



RETIRED





Reason:



The model showed unrealistic performance:



Accuracy:

98.3%



F1:

96.1%





Problems discovered:



\- trained on smaller dataset

\- possible data leakage

\- biased historical representation

\- unrealistic for live trading





Decision:



Do not use model\_v27 as performance benchmark.





\# Current ML Approach





Dataset:



data/historical\_ml\_dataset.csv





Current training size:



Training samples:

3,504,289





Testing samples:



98,034





Training method:



Chronological split.



Purpose:



Prevent future information leakage.







\# 6. Current Champion Model





Latest accepted model:



model\_v33





Algorithm:



Random Forest





Configuration:



n\_estimators:

500



max\_depth:

20



min\_samples\_leaf:

10



max\_features:

sqrt



class\_weight:

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







Important:



Current model evaluation uses multiple factors:



\- F1 score

\- ROC-AUC

\- Average return

\- Win rate





The champion system no longer accepts models based only on F1.







\# 7. Current Feature Set





Features currently used:





Volume





Returns:



Return\_5D



Return\_10D



Return\_20D





Momentum:



Momentum\_Acceleration





Technical indicators:



RSI



RSI\_Change



SMA20



SMA50



Above\_SMA20



Above\_SMA50



SMA\_Gap





Volatility:



Volatility\_20D



ATR



ATR\_Percent





Volume:



Average\_Volume



RVOL



Volume\_Trend





Position:



Range\_Position



Distance\_From\_52W\_High







\# 8. AI Research Engine Status





Completed:



✓ AI ranking system



✓ AI scoring engine



✓ AI confidence



✓ Historical ML probability



✓ Trade quality filtering



✓ AI decisions



✓ Automated reports





Current files:



app/ai\_ranker.py



app/ai\_score\_engine.py



app/ai\_decision\_engine.py



app/trade\_quality\_filter.py







\# 9. Current Research Problems





\## Research Score



Needs:



\- normalization

\- percentile scaling

\- better distribution handling





\## AI Final Score



Needs:



\- automatic weight optimization

\- validation against historical outcomes





\## Risk Adjustment



Future:



\- volatility based stops

\- market regime adjustment

\- dynamic position sizing





\## Confidence Calibration



Goal:



A confidence score should represent real historical probability.





Example:



70% confidence should historically produce approximately 70% successful setups.







\# 10. Historical Threshold Optimization





Current file:



app/historical\_threshold\_optimizer.py





Purpose:



Find optimal filtering thresholds.





Current optimization targets:



\- Rank Score

\- Confidence Score

\- Research Score





Future improvements:



\- percentile thresholds

\- decimal thresholds

\- minimum trade requirements

\- drawdown penalties

\- Sharpe-like scoring







\# 11. Data Files





Important:





Historical ML dataset:



data/historical\_ml\_dataset.csv





Trade database:



data/trade\_database.csv





Quality results:



data/results/quality\_results.csv





Models:



data/models/





Reports:



data/reports/







\# 12. Future Documentation Rule





Every major change must update:



docs/EXPERIMENT\_LOG.md





Every model training must update:



docs/MODEL\_HISTORY.md





Every phase completion must update:



docs/ROADMAP.md





Architecture changes update:



docs/ARCHITECTURE.md







\# 13. Next Development Priorities





Priority 1:



Improve AI Research Engine.





Tasks:



1\. Research score normalization



2\. AI score optimization



3\. Confidence calibration



4\. Explainable AI





Priority 2:



Improve professional backtesting.





Tasks:



\- walk-forward testing

\- benchmark comparison

\- equity curve

\- drawdown analysis





Priority 3:



Improve model monitoring.





Tasks:



\- drift detection

\- automatic retraining

\- model rollback





\# 14. Important Development Philosophy





The platform should evolve like a professional quantitative research system.





Avoid:



\- overfitting

\- unrealistic metrics

\- leakage

\- accepting models only because of high accuracy





Prefer:



\- realistic testing

\- reproducible experiments

\- documented decisions

\- continuous improvement

