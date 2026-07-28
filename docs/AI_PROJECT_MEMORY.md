\# AI Trading Research Platform — Project Memory



Last Updated:

2026-07-28





Repository:



AI-Trading-Research-Platform





GitHub:



https://github.com/AnastasiyaKotelnikova/AI-Trading-Research-Platform





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





Run modules:



python -m app.module\_name





Main project folder:



C:\\Users\\anast\\scanner-project









\# 3. Current Development Phase





Current Phase:



Phase 3 — AI Research Engine





Estimated Completion:



\~75%





Overall Platform Completion:



Approximately 45-50%





Current Focus:



Improving:



\- AI ranking

\- confidence calibration

\- research scoring

\- risk adjustment

\- historical threshold optimization









\# 4. Completed Development







\# Phase 1 — Data Engineering



Status:



COMPLETE





Completed:



✓ Historical market data collection



✓ Price history storage



✓ Feature generation



✓ Feature history database



✓ ML dataset builder



✓ Daily pipeline automation





Main components:





app/price\_history\_collector.py



app/feature\_history\_builder.py



app/historical\_ml\_builder.py



app/daily\_pipeline.py











\# Phase 2 — Machine Learning Foundation





Status:



Mostly Complete





Completed:





✓ ML training pipeline



✓ Feature selection



✓ Model evaluation



✓ Model versioning



✓ Champion model system



✓ ML prediction pipeline



✓ Backtesting integration



✓ ROC-AUC evaluation



✓ Improved model comparison logic







Main components:





app/train\_model.py



app/model\_registry.py



app/ml\_predictor.py



app/ml\_backtest.py











\# 5. Important Model Evolution







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

\- unrealistic validation results





Decision:





model\_v27 is not used as a performance benchmark.













\# Current ML Approach







Dataset:





data/historical\_ml\_dataset.csv







Current training size:





Training samples:



3,504,289





Testing samples:



98,034







Validation method:





Chronological split





Purpose:





Reduce future information leakage and create more realistic evaluation.









\# 6. Current Champion Model







Latest Accepted Model:





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







Champion selection now considers:





\- F1 score

\- ROC-AUC

\- Average return

\- Win rate







Models are no longer accepted only because of high classification metrics.











\# 7. Current Feature Set







Features used:





\## Volume



Volume



Average\_Volume



RVOL



Volume\_Trend







\## Returns





Return\_5D



Return\_10D



Return\_20D







\## Momentum





Momentum\_Acceleration







\## Technical Indicators





RSI



RSI\_Change



SMA20



SMA50



Above\_SMA20



Above\_SMA50



SMA\_Gap







\## Volatility





Volatility\_20D



ATR



ATR\_Percent







\## Position





Range\_Position



Distance\_From\_52W\_High









\# 8. AI Research Engine Status







Completed:





✓ AI ranking system



✓ AI scoring engine



✓ AI confidence system



✓ Historical ML probability



✓ Trade quality filtering



✓ AI decisions



✓ Automated research reports







Main files:





app/ai\_ranker.py



app/ai\_score\_engine.py



app/ai\_decision\_engine.py



app/trade\_quality\_filter.py









\# 9. Current Research Problems







\## Research Score





Needs:





\- normalization

\- percentile scaling

\- distribution correction







\## AI Final Score





Needs:





\- automatic weight optimization

\- validation against historical outcomes







\## Risk Adjustment





Future:





\- volatility-based stops

\- market regime adjustment

\- dynamic position sizing







\## Confidence Calibration





Goal:





Confidence scores should represent real historical probabilities.





Example:





70% confidence should historically produce approximately 70% successful setups.











\# 10. Historical Threshold Optimization







Current file:





app/historical\_threshold\_optimizer.py







Purpose:





Find optimal filtering thresholds.







Current targets:





\- Rank Score

\- Confidence Score

\- Research Score







Future improvements:





\- percentile thresholds

\- decimal thresholds

\- minimum trade requirements

\- drawdown penalties

\- Sharpe-like scoring

\- expectancy optimization











\# 11. Documentation System





Created:





docs/





AI\_PROJECT\_MEMORY.md



ARCHITECTURE.md



EXPERIMENT\_LOG.md



MODEL\_HISTORY.md



ROADMAP.md



DEVELOPMENT\_RULES.md







Purpose:





Maintain:





\- project history

\- experiment results

\- model evolution

\- architecture decisions

\- development roadmap









\# 12. Git Development Workflow







Repository:





AI-Trading-Research-Platform







Major changes:





git add .



git commit -m "Description"



git push







Documentation updates are required after:





\- model changes

\- architecture changes

\- completed phases

\- major experiments











\# 13. Important Data Files







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









\# 14. Next Development Priorities







\## Priority 1 — AI Research Engine







Tasks:





1\. Improve research score normalization





2\. Optimize AI final score weighting





3\. Implement confidence calibration





4\. Improve explainable AI









\## Priority 2 — Historical Threshold Optimizer







Tasks:





\- remove duplicate threshold results

\- use percentile-based search

\- support decimal thresholds

\- connect optimized thresholds to scanner









\## Priority 3 — Professional Backtesting







Tasks:





\- walk-forward validation

\- benchmark comparison

\- equity curve

\- drawdown analysis

\- Sharpe/Sortino metrics









\## Priority 4 — Model Monitoring







Tasks:





\- drift detection

\- automatic retraining

\- model rollback

\- performance tracking









\# 15. Development Philosophy







The platform should evolve like a professional quantitative research system.







Avoid:





\- overfitting

\- unrealistic metrics

\- data leakage

\- accepting models only because of accuracy







Prefer:





\- realistic testing

\- reproducible experiments

\- documented decisions

\- continuous improvement

