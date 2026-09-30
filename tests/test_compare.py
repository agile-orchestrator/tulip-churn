import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedKFold

from tulip_churn.compare import (
    BASELINE_NAME,
    candidates,
    evaluate_candidate,
    flag_leakage_suspects,
    format_report,
    run_comparison,
    top_share_precision_recall,
)
from tulip_churn.data import TARGET
from tulip_churn.features import FEATURES, add_features


def test_top_share_precision_recall_picks_highest_scored_positives():
    y_true = np.array([1, 0, 1, 0, 0, 0, 0, 0, 0, 0])
    y_proba = np.array([0.9, 0.8, 0.7, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1])
    precision, recall = top_share_precision_recall(y_true, y_proba, top_share=0.3)
    assert precision == 2 / 3
    assert recall == 1.0


def test_each_candidate_fits_and_scores(raw_df):
    featured = add_features(raw_df)
    X = featured[FEATURES]
    y = featured[TARGET]
    cv = StratifiedKFold(n_splits=2, shuffle=True, random_state=0)
    for estimator in candidates().values():
        scores = evaluate_candidate(estimator, X, y, cv)
        assert 0.0 <= scores["roc_auc_mean"] <= 1.0


def test_run_comparison_covers_every_candidate(raw_df):
    results = run_comparison(raw_df)
    assert set(results.index) == set(candidates())
    assert BASELINE_NAME in results.index


def test_flag_leakage_suspects_ignores_baseline():
    results = pd.DataFrame(
        {"roc_auc_mean": [0.80, 0.90]}, index=[BASELINE_NAME, "suspicious_candidate"]
    )
    assert flag_leakage_suspects(results) == ["suspicious_candidate"]


def test_flag_leakage_suspects_empty_when_within_margin():
    results = pd.DataFrame({"roc_auc_mean": [0.80, 0.82]}, index=[BASELINE_NAME, "xgboost"])
    assert flag_leakage_suspects(results) == []


def test_format_report_lists_every_candidate_and_leakage_note():
    results = pd.DataFrame(
        {
            "roc_auc_mean": [0.80, 0.70],
            "roc_auc_std": [0.01, 0.01],
            "pr_auc_mean": [0.50, 0.40],
            "pr_auc_std": [0.01, 0.01],
            "precision_top_mean": [0.60, 0.50],
            "precision_top_std": [0.01, 0.01],
            "recall_top_mean": [0.30, 0.25],
            "recall_top_std": [0.01, 0.01],
        },
        index=[BASELINE_NAME, "logistic_regression"],
    )
    report = format_report(results, leakage_suspects=[])
    assert BASELINE_NAME in report
    assert "logistic_regression" in report
    assert "No candidate beats the baseline" in report
