\# AI Trading Research Platform — Next Chat Start Guide





\## How to Continue Work in a New Chat





Before making recommendations or code changes:



Read these project documents first:





docs/AI\_PROJECT\_MEMORY.md



docs/MODEL\_HISTORY.md



docs/EXPERIMENT\_LOG.md



docs/ARCHITECTURE.md



docs/ROADMAP.md



docs/DEVELOPMENT\_RULES.md







These files contain:



\- current project status

\- completed phases

\- previous decisions

\- model history

\- experiments

\- architecture

\- development rules







\# Current Project State





Project:



AI Trading Research Platform





Location:



C:\\Users\\anast\\scanner-project





Environment:



Python 3.11.9



Virtual environment:



venv





Run modules:



python -m app.module\_name







\# Current Development Phase





Phase 3 — AI Research Engine





Progress:



\~75% complete







Current priority:



Improve AI research quality before expanding into production features.







Current focus:



1\. Historical threshold optimization



2\. Research score normalization



3\. AI final score optimization



4\. Confidence calibration



5\. Explainable AI







\# Important Previous Decisions





\## Model v27





Retired.





Reason:



\- trained on smaller dataset

\- possible data leakage

\- unrealistic metrics

\- biased historical representation





Do not use model\_v27 as a benchmark.







\## Current ML System





Latest accepted model:



model\_v33





Evaluation considers:



\- F1

\- ROC-AUC

\- Average Return

\- Win Rate





Do not optimize only for accuracy.







\# Development Rules





Before changing code:



1\. Understand existing architecture.



2\. Check related files.



3\. Avoid creating duplicate systems.



4\. Preserve working pipeline.



5\. Explain why a change improves the system.







When modifying ML:



Update:



docs/MODEL\_HISTORY.md





When testing experiments:



Update:



docs/EXPERIMENT\_LOG.md





When completing phases:



Update:



docs/ROADMAP.md





When changing architecture:



Update:



docs/ARCHITECTURE.md







\# Git Workflow





Git commands must be run in:



C:\\Users\\anast\\scanner-project





with virtual environment active:



(venv)







\## Check status





PowerShell:



git status







\## Save meaningful progress





Example:





git add .



git commit -m "Improve historical threshold optimizer"



git push







\## Good commit examples:





"Add ROC-AUC evaluation"



"Improve champion model scoring"



"Fix ML data leakage issue"



"Complete Phase 3 threshold optimization"







Avoid meaningless commits:





"changes"



"update"



"test"







\# Before Starting Coding





First check:





git status





Confirm:



nothing to commit



or review existing changes.







\# After Completing Work





Always:





1\. Test code



Example:



python -m app.module\_name





2\. Update documentation



3\. Commit changes



4\. Push to GitHub







\# New Chat Opening Message





Copy this:





"I am continuing my AI Trading Research Platform project.



First read:



docs/AI\_PROJECT\_MEMORY.md

docs/MODEL\_HISTORY.md

docs/EXPERIMENT\_LOG.md

docs/ARCHITECTURE.md

docs/ROADMAP.md

docs/DEVELOPMENT\_RULES.md



Use these as the source of truth.



My current phase is Phase 3 — AI Research Engine.



Continue from the last completed task. Do not redesign the architecture unless necessary."

