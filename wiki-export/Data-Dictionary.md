# 📖 Data Dictionary

Source: monthly customer extract from the core banking system (`Churn_Modelling.csv`, one row per customer, ~10,000 rows). For local development we use a synthetic extract with the same schema (`scripts/generate_data.py`).

## Raw columns

| Column | Type | Meaning | Notes |
|---|---|---|---|
| `RowNumber` | int | Row index in the extract | Dropped, no meaning |
| `CustomerId` | int | Internal customer identifier | Personal data. Dropped before training, never logged |
| `Surname` | string | Customer surname | Personal data. Dropped before training, never logged |
| `CreditScore` | int | Internal credit score (350–850) | |
| `Geography` | category | Country of residence: France, Germany, Spain | |
| `Gender` | category | Male / Female | Sensitive attribute, see fairness notes in the model card |
| `Age` | int | Age in years | Sensitive attribute |
| `Tenure` | int | Years as a customer (0–10) | |
| `Balance` | float | Account balance in EUR | Many customers have 0 |
| `NumOfProducts` | int | Number of bank products held (1–4) | |
| `HasCrCard` | 0/1 | Holds a Tulip credit card | |
| `IsActiveMember` | 0/1 | Logged in or transacted in the last 3 months | |
| `EstimatedSalary` | float | Estimated yearly salary in EUR | |
| `Exited` | 0/1 | **Target.** 1 = customer left the bank within the observation window | Not available at scoring time |

## Engineered features

| Feature | Definition | Source |
|---|---|---|
| `BalanceToSalary` | Balance / EstimatedSalary | `features.py` |
| `ZeroBalance` | 1 if Balance = 0 | `features.py` |
| `AgeBand` | <30, 30–39, 40–49, 50–59, 60+ | `features.py` |
| `AccountClosureRequested` | 1 if the customer asked their branch to close an account (CRM flag) | `features.py` (added in PR #22) |
