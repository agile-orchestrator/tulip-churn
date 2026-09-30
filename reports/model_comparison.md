# Model comparison

Stratified 5-fold CV, ranked by precision in the top 10%.

| Model | ROC AUC | PR AUC | Precision top 10% | Recall top 10% |
|---|---|---|---|---|
| `gradient_boosting` | 0.801 ± 0.007 | 0.522 ± 0.013 | 0.608 ± 0.017 | 0.320 ± 0.009 |
| `hist_gradient_boosting_balanced` | 0.788 ± 0.006 | 0.505 ± 0.010 | 0.597 ± 0.019 | 0.314 ± 0.010 |
| `xgboost` | 0.762 ± 0.004 | 0.461 ± 0.007 | 0.556 ± 0.022 | 0.293 ± 0.012 |
| `logistic_regression_balanced` | 0.755 ± 0.012 | 0.448 ± 0.022 | 0.533 ± 0.028 | 0.281 ± 0.015 |
| `logistic_regression` | 0.749 ± 0.013 | 0.441 ± 0.023 | 0.525 ± 0.024 | 0.276 ± 0.012 |

No candidate beats the baseline by more than 0.05 ROC AUC.
