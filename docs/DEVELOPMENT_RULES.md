\# AI Trading Research Platform — Development Rules



Last Updated:



2026-07-28





\# Purpose



These rules keep the project organized as it grows.



The goal is to maintain:



\- reproducibility

\- experiment history

\- model transparency

\- clean development workflow





\# 1. Before Making Major Changes



Before modifying important components:



Check:



\- AI\_PROJECT\_MEMORY.md

\- ARCHITECTURE.md

\- ROADMAP.md

\- EXPERIMENT\_LOG.md





Understand:



\- why the change is needed

\- what problem it solves

\- how success will be measured





\# 2. Model Development Rules



Every ML model training must record:





Dataset:



\- file name

\- number of rows

\- number of features

\- training/testing split





Features:



\- added features

\- removed features

\- reason for changes





Model:



\- algorithm

\- hyperparameters

\- training date





Evaluation:



Required:



\- Accuracy

\- Precision

\- Recall

\- F1

\- ROC-AUC





Trading evaluation:



Required:



\- number of trades

\- win rate

\- average return

\- drawdown

\- risk metrics





Decision:



Every model must be:



\- Accepted

\- Rejected

\- Retired





Reason must be documented.





\# 3. Champion Model Rules



A new model cannot replace the champion only because of:



\- higher accuracy

\- higher F1

\- higher training score





The model must demonstrate:



\- realistic validation

\- acceptable trading performance

\- no evidence of leakage

\- improvement over current champion





\# 4. Experiment Logging



Every significant experiment must update:



docs/EXPERIMENT\_LOG.md





Examples:



\- new feature

\- new algorithm

\- new dataset

\- changed scoring logic

\- changed thresholds

\- changed validation method





\# 5. Dataset Rules



Dataset changes must be documented.



Record:



\- source

\- date range

\- number of stocks

\- number of rows

\- features included





Never compare models trained on different datasets without noting the difference.





\# 6. Git Rules



Before major milestones:



Check:



git status





Commit:



git add .



git commit -m "Description of change"





Push:



git push





Commit messages should explain the purpose.





Examples:





Good:



"Add ROC-AUC evaluation to ML pipeline"





Bad:



"Changed stuff"





\# 7. Testing Rules



Before accepting major changes:



Run:



\- training test

\- scanner test

\- backtest

\- validation





Record results.





\# 8. Architecture Rules



New modules should have:



\- clear purpose

\- descriptive name

\- documentation

\- integration point





Avoid:



\- duplicate files

\- unnecessary backups

\- unused code





\# 9. Trading Research Philosophy



The platform is a research system.



It should optimize for:



\- realistic performance

\- repeatability

\- risk control

\- continuous improvement





Not:



\- unrealistic prediction accuracy

\- overfitted models

\- misleading metrics





\# 10. Future Development



Future additions should follow the roadmap:



Phase 3:

AI Research Engine



Phase 4:

Professional Backtesting



Phase 5:

Portfolio Management



Phase 6:

Model Monitoring



Phase 7:

Paper Trading



Phase 8:

Optional Live Trading

