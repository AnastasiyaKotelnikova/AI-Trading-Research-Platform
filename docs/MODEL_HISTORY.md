\# AI Trading Research Platform — Model History



Last Updated:



2026-07-28





\# Purpose



This document tracks every important machine learning model experiment.



For each model version we record:



\- training dataset

\- feature set

\- algorithm

\- training changes

\- evaluation metrics

\- backtest results

\- acceptance/rejection decision

\- lessons learned





The purpose is to prevent repeating mistakes and understand how the ML system evolved.







\# Model Development Timeline







\## Early Models (v1 - v6)



Status:



Historical development phase





Purpose:



Initial ML pipeline testing.





Characteristics:



\- smaller datasets

\- early feature engineering

\- basic evaluation

\- no mature validation system





Limitations discovered:



\- insufficient historical data

\- possible bias

\- limited feature coverage





Decision:



Retired.







\---





\# model\_v7





Status:



Rejected





Reason:



Failed to outperform champion model.





Notes:



Introduced improved evaluation process using:



\- F1 score

\- precision

\- recall







\---





\# model\_v8





Status:



Rejected





Reason:



Performance improvement was insufficient.







\---





\# model\_v9





Status:



Rejected





Reason:



Improved F1 but failed champion comparison.







\---





\# model\_v10 - model\_v26





Status:



Historical development models





General improvements:



\- more features added

\- better training pipeline

\- improved feature engineering

\- expanded evaluation





Limitations:



Models still affected by:



\- limited historical data

\- possible leakage

\- insufficient validation







\---





\# model\_v27





Status:



RETIRED





Previous Champion:



Yes





Reported metrics:



Accuracy:



98.3%





F1:



96.1%







\## Why It Was Retired





The performance appeared unrealistic.





Problems identified:





1\. Training dataset was too small.





2\. Data leakage was likely present.





3\. Validation did not represent realistic future trading conditions.





4\. Metrics were too optimistic compared with expected market prediction difficulty.







Decision:



Remove as performance benchmark.





Lesson:



High ML metrics do not automatically mean a useful trading model.







\---





\# Dataset Expansion Phase





Major improvement:





The historical dataset was expanded significantly.





Previous issues addressed:





✓ More historical examples



✓ More stocks



✓ More feature history



✓ Better chronological validation



✓ Reduced leakage risk







Current dataset:





File:



data/historical\_ml\_dataset.csv





Training records:



3,504,289





Testing records:



98,034







Validation method:





Chronological split:



Training:



Before 2026-05-15





Testing:



After 2026-05-15







Purpose:



Simulate future prediction.







\---





\# model\_v32





Status:



Rejected





Algorithm:



Random Forest





Configuration:



n\_estimators:



500





max\_depth:



20





min\_samples\_leaf:



10





Evaluation:





ROC-AUC:



0.669





F1:



0.467





Reason:



Did not exceed final acceptance criteria.







\---





\# model\_v33





Status:



CURRENT CHAMPION





Accepted:



2026-07-28







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







Dataset:



Expanded historical ML dataset







Features:



21 technical and market features.







\## Validation Results





Accuracy:



0.551





F1:



0.467





ROC-AUC:



0.669







\## Trading Backtest





Trades:



210





Win Rate:



46.7%





Average Return:



0.448%







\## Acceptance Logic





The model was accepted because:





New Model Score:



0.430





Previous Champion Score:



0.192







Score components:





F1:



20%





ROC-AUC:



30%





Average Return:



30%





Win Rate:



20%







Decision:



Champion model updated.







\---





\# Current Champion





File:



data/models/champion\_model.pkl







Current model:



model\_v33







Use:



Production research pipeline







Not approved for:



Real money trading.







Requires:



\- longer paper trading validation

\- walk-forward testing

\- more market regimes

\- better risk analysis







\---





\# Future Model Experiments







\## Planned Models





\### XGBoost



Purpose:



Compare against Random Forest.







\### LightGBM



Purpose:



High-performance gradient boosting research.







\### CatBoost



Purpose:



Alternative tree-based model.







\### Neural Networks



Purpose:



Research only after dataset stabilization.







\---





\# Future Evaluation Improvements





Future models should include:





\## Calibration



Probability output should match real success frequency.





Example:



Predicted 70% probability:



Should historically produce approximately 70% successful trades.







\## Walk-forward validation





Instead of:



Train once → Test once





Use:



Train period



↓



Validate



↓



Move forward



↓



Retrain







\## Additional metrics





Add:





\- Sharpe ratio

\- Maximum drawdown

\- Profit factor

\- Expectancy

\- Sortino ratio

\- Risk-adjusted return







\---





\# Model Training Rules





Every future model training must record:





Date:



Dataset size:



Feature count:



Features added/removed:



Algorithm:



Hyperparameters:



Metrics:



Backtest:



Decision:



Reason:







\# Important Lesson





The goal is not to build the model with the highest score.



The goal is to build the model that survives realistic market testing.

