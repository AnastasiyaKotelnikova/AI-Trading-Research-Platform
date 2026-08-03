# AI Trading Research Platform — Development Rules


Repository:

AI-Trading-Research-Platform


GitHub:

https://github.com/AnastasiyaKotelnikova/AI-Trading-Research-Platform


Local Path:

C:\Users\anast\scanner-project



Last Updated:

2026-08-03



# Purpose


These rules keep the project organized as it grows.



The goal is to maintain:


- reproducibility

- experiment history

- model transparency

- clean development workflow

- architecture consistency

- realistic trading research standards



The platform is a quantitative research system.


It is not designed around unrealistic prediction accuracy or uncontrolled automation.



---


# 1. Before Making Major Changes


Before modifying important components:


Always review:


- AI_PROJECT_MEMORY.md

- ARCHITECTURE.md

- ROADMAP.md

- EXPERIMENT_LOG.md

- MODEL_HISTORY.md



Understand:


- why the change is needed

- what problem it solves

- how success will be measured

- what existing components are affected



Avoid:


- creating duplicate systems

- replacing working modules without reason

- changing architecture without documentation



---


# 2. Machine Learning Development Rules


Every ML model training experiment must record:



## Dataset


Document:


- dataset file name

- date range

- number of rows

- number of features

- training/testing split

- validation method



Never compare models trained on different datasets without documenting the difference.



---


## Features


Record:


- added features

- removed features

- feature importance

- reason for changes

- possible leakage concerns



Feature changes must be documented in:


```
docs/EXPERIMENT_LOG.md
```



---


## Model Information


Record:


- model version

- algorithm

- hyperparameters

- training date

- training environment



Examples:


- Random Forest

- XGBoost

- LightGBM

- Neural Network



---


# 3. Model Evaluation Rules


Required classification metrics:


- Accuracy

- Precision

- Recall

- F1 Score

- ROC-AUC



However:


Classification metrics alone are not enough.



Trading evaluation must include:


- number of trades

- win rate

- average return

- drawdown

- risk metrics

- stability across market conditions



The project prioritizes trading usefulness over classification scores.



---


# 4. Champion Model Rules


A new model cannot replace the champion only because it has:


- higher accuracy

- higher F1 score

- higher training score



A replacement model must demonstrate:


✓ realistic validation

✓ no evidence of leakage

✓ improved trading performance

✓ acceptable risk

✓ stability



Champion decisions must be recorded in:


```
docs/MODEL_HISTORY.md
```



---


# 5. Model v27 Rule


model_v27 is permanently retired.



Previous reported metrics:


Accuracy:

98.3%



F1:

96.1%



Reason:


- insufficient dataset

- possible leakage

- unrealistic validation

- misleading performance expectations



Important:


model_v27 must not be used as a benchmark.



Future models must compare against reliable validation standards.



---


# 6. Two ML Path Architecture Rule


The platform contains two separate ML paths.



They must remain logically separated.



---


## Historical ML Path


Purpose:


Learn from historical market behavior.



Source:


```
data/historical_ml_dataset.csv
```



Output:


```
Historical_ML_Probability
```



Used for:


- historical similarity

- pattern confirmation

- research confidence



---


## Scanner ML Path


Purpose:


Evaluate current market candidates.



Output:


```
ML_Probability
```



Used for:


- scanner ranking

- AI scoring

- current opportunity evaluation



Do not merge these paths without architectural review.



---


# 7. Experiment Logging Rules


Every significant experiment must update:


```
docs/EXPERIMENT_LOG.md
```



Examples:


- new feature

- new model

- new algorithm

- scoring changes

- threshold changes

- validation changes

- risk logic changes

- decision pipeline changes



Each experiment should include:


- date

- objective

- files changed

- result

- decision

- next action



---


# 8. Dataset Rules


Dataset changes must record:


- source

- date range

- number of stocks

- number of rows

- feature list

- generation method



Never silently replace datasets.



Historical datasets are part of the research record.



---


# 9. AI Decision System Rules


AI decisions must remain explainable.



Every final decision should consider:


- ranking quality

- ML confidence

- historical evidence

- risk evaluation

- reward potential

- strategy performance



Final decisions should include:


- decision

- confidence level

- reasoning



Avoid:


- black-box decisions

- unsupported trade recommendations

- ignoring risk controls



---


# 10. Risk Management Rules


Risk management is required before trade approval.



Trade logic must consider:


- stop loss

- position size

- reward/risk ratio

- expected value

- portfolio exposure



No trade should become executable only because of:


- high ML probability

- high ranking score

- historical success rate



Risk filtering remains mandatory.



---


# 11. Trade Management Rules


Trade management changes must be tested before acceptance.



Document changes involving:


- entries

- exits

- stop calculations

- targets

- sizing

- execution states



Relevant modules:


```
trade_management.py

trade_exit_manager.py

trade_history_manager.py
```



---


# 12. Git Rules


Before major milestones:



Check:


```
git status
```



Review:


- modified files

- untracked files

- generated data changes



Commit:


```
git add .

git commit -m "Description of change"

git push
```



Good commit examples:


```
Improve AI decision risk filtering

Add historical ML probability integration

Update trade management logic

Improve model validation pipeline
```



Avoid:


```
changes

update

test

stuff
```



---


# 13. Testing Rules


Before accepting major changes run:



Required:


- training test

- scanner test

- AI decision test

- backtest

- validation



Record results.



Major changes require documentation updates.



---


# 14. Architecture Rules


New modules must have:


- clear purpose

- descriptive name

- documentation

- integration point



Avoid:


- duplicate files

- unused code

- abandoned experiments

- multiple competing pipelines



Before creating a new module:


Ask:


"Can an existing module be extended instead?"



---


# 15. Documentation Rules


Update documentation after major changes:



Required files:


```
AI_PROJECT_MEMORY.md

MODEL_HISTORY.md

EXPERIMENT_LOG.md

ARCHITECTURE.md

ROADMAP.md
```



Documentation should explain:


- what changed

- why it changed

- how it improves the system



---


# 16. Trading Research Philosophy


The platform optimizes for:


✓ realistic performance

✓ repeatability

✓ transparency

✓ risk control

✓ continuous improvement



Not:


✗ unrealistic prediction accuracy

✗ overfitted models

✗ misleading metrics

✗ automatic trading without validation



The goal:


Build an AI research assistant that improves decision quality through:


- historical evidence

- machine learning

- quantitative testing

- risk analysis

- feedback learning



---


# 17. Future Development Order


Future development should follow the roadmap:



Phase 3:

AI Research Engine


↓

Phase 4:

Professional Backtesting


↓

Phase 5:

Portfolio Intelligence


↓

Phase 6:

Model Monitoring


↓

Phase 7:

Paper Trading


↓

Phase 8:

Optional Live Trading



New features should not skip validation stages.



---


# Final Rule


The platform should evolve like a professional quantitative research system.



Every improvement must answer:


1. Does it improve research quality?

2. Is it validated with evidence?

3. Does it reduce risk?

4. Is it reproducible?

5. Is it documented?
