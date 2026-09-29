# tulip-churn

Churn early-warning for **Tulip Bank**: predict which customers are likely to leave so the
Retention team can contact them first.

## Quickstart

```bash
uv sync                                   # install deps (Python 3.11+)
uv run python scripts/generate_data.py    # writes data/raw/Churn_Modelling.csv
uv run jupyter nbconvert --to notebook --execute --inplace notebooks/01_exploration.ipynb
                                          # trains and saves models/model.joblib
uv run uvicorn tulip_churn.api:app --reload
curl -X POST localhost:8000/score -H 'content-type: application/json' -d '{
  "CreditScore": 619, "Geography": "France", "Gender": "Female", "Age": 42, "Tenure": 2,
  "Balance": 0, "NumOfProducts": 1, "HasCrCard": 1, "IsActiveMember": 1,
  "EstimatedSalary": 101348.88}'
```

Tests and lint: `uv run pytest` and `uv run ruff check .`

## Data

`data/raw/` is gitignored. By default we use a synthetic dataset with the same schema as the
Kaggle [Churn Modelling](https://www.kaggle.com/datasets/shrutimechlearn/churn-modelling)
dataset. To use the real one instead (needs `~/.kaggle/kaggle.json`):

```bash
uv run --with kaggle kaggle datasets download -d shrutimechlearn/churn-modelling -p data/raw --unzip
```

Column meanings are in the [Data Dictionary](https://github.com/agile-orchestrator/tulip-churn/wiki/Data-Dictionary) page on the wiki.

## Layout

```
src/tulip_churn/
  data.py       load + clean
  features.py   feature engineering
  train.py      training entrypoint
  evaluate.py   metrics
  api.py        FastAPI scoring service (POST /score)
notebooks/      exploration + training
tests/
```

## Ways of working

Backlog lives on the GitHub Project board, documentation (DoR, DoD, ADRs, meeting notes) on the
[GitHub Wiki](https://github.com/agile-orchestrator/tulip-churn/wiki). See `CLAUDE.md` for conventions.
