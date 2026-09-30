---
description: Draft or update the model card on the wiki from models/metrics.json and the code
---
Take the numbers from `models/metrics.json`, which `uv run python -m tulip_churn.train` writes,
and everything else from the code in `src/tulip_churn/`. Never copy numbers from the notebook:
its saved outputs can be stale.

1. If `models/metrics.json` is missing, stop and ask the user to run the training command. If
   `git_dirty` is true or `git_commit` is not on `main`, say so on the card and in your reply.
2. Pull the wiki clone (`git -C ../tulip-churn.wiki pull`) and read the
   [Model Card Template](https://github.com/agile-orchestrator/tulip-churn/wiki/Model-Card-Template)
   and any existing `Model-Card-*.md` page. If one exists, update it. Otherwise draft a new page
   titled "Model card — <algorithm> <package_version>".
3. Fill the template from `metrics.json`:
   - Model details: `algorithm`, `params`, `trained_at`, `git_commit`, `sklearn_version`
   - Training data: `data_path`, `data.rows`, `data.churn_rate`, preprocessing from
     `data.clean()`
   - Evaluation: hold-out from `params.test_size` and `params.seed` (see `data.split()`),
     `test` metrics, `threshold`
   - Fairness: `by_group` (Gender, AgeBand, Geography)
   - Features: `features`. For each one, use `features.py` and the `Customer` model in `api.py`
     to confirm it is available at scoring time
4. Take intended use, limitations and monitoring from the wiki pages. Where no source says it,
   write "to be completed". Do not invent anything.
5. Flag anything suspicious: ROC AUC near 1.0 (check for leakage), a group whose metrics are well
   below the overall, very small groups, or a feature that is not available at scoring time.
6. Write the draft to the scratchpad directory and share the content for review. Only publish it
   to the wiki (commit and push in `../tulip-churn.wiki`, and link it from `_Sidebar.md`) after
   the user agrees, then share the link.
