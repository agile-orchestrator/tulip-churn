"""Compare candidate churn models on the same stratified CV folds.

Run with: uv run python -m tulip_churn.compare
Writes reports/model_comparison.md.
"""

from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.base import ClassifierMixin
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import GradientBoostingClassifier, HistGradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score, roc_auc_score
from sklearn.model_selection import StratifiedKFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from xgboost import XGBClassifier

from tulip_churn.data import TARGET, load_data
from tulip_churn.features import CATEGORICAL, FEATURES, add_features

REPORT_PATH = Path(__file__).resolve().parents[2] / "reports" / "model_comparison.md"
BASELINE_NAME = "gradient_boosting"
TOP_SHARE = 0.10
N_SPLITS = 5
SEED = 42
LEAKAGE_MARGIN = 0.05


def candidates() -> dict[str, ClassifierMixin]:
    return {
        "logistic_regression": LogisticRegression(max_iter=1000),
        "logistic_regression_balanced": LogisticRegression(
            max_iter=1000, class_weight="balanced"
        ),
        BASELINE_NAME: GradientBoostingClassifier(n_estimators=200, max_depth=3),
        "hist_gradient_boosting_balanced": HistGradientBoostingClassifier(
            class_weight="balanced"
        ),
        "xgboost": XGBClassifier(eval_metric="logloss"),
    }


def build_pipeline(estimator: ClassifierMixin) -> Pipeline:
    encoder = ColumnTransformer(
        [("categorical", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL)],
        remainder="passthrough",
    )
    return Pipeline([("encode", encoder), ("model", estimator)])


def top_share_precision_recall(
    y_true: np.ndarray, y_proba: np.ndarray, top_share: float = TOP_SHARE
) -> tuple[float, float]:
    n_top = max(1, int(len(y_true) * top_share))
    top_indices = np.argsort(y_proba)[::-1][:n_top]
    y_top = y_true[top_indices]
    precision = y_top.mean()
    recall = y_top.sum() / y_true.sum()
    return precision, recall


@dataclass
class FoldScores:
    roc_auc: list[float] = field(default_factory=list)
    pr_auc: list[float] = field(default_factory=list)
    precision_top: list[float] = field(default_factory=list)
    recall_top: list[float] = field(default_factory=list)

    def add(self, y_true: np.ndarray, y_proba: np.ndarray) -> None:
        precision, recall = top_share_precision_recall(y_true, y_proba)
        self.roc_auc.append(roc_auc_score(y_true, y_proba))
        self.pr_auc.append(average_precision_score(y_true, y_proba))
        self.precision_top.append(precision)
        self.recall_top.append(recall)

    def summary(self) -> dict[str, float]:
        return {
            f"{metric}_{stat}": getattr(np, stat)(values)
            for metric, values in vars(self).items()
            for stat in ("mean", "std")
        }


def evaluate_candidate(
    estimator: ClassifierMixin, X: pd.DataFrame, y: pd.Series, cv: StratifiedKFold
) -> dict[str, float]:
    scores = FoldScores()
    for train_idx, test_idx in cv.split(X, y):
        pipeline = build_pipeline(estimator)
        pipeline.fit(X.iloc[train_idx], y.iloc[train_idx])
        y_proba = pipeline.predict_proba(X.iloc[test_idx])[:, 1]
        scores.add(y.iloc[test_idx].to_numpy(), y_proba)
    return scores.summary()


def run_comparison(df: pd.DataFrame) -> pd.DataFrame:
    featured = add_features(df)
    X = featured[FEATURES]
    y = featured[TARGET]
    cv = StratifiedKFold(n_splits=N_SPLITS, shuffle=True, random_state=SEED)
    rows = {name: evaluate_candidate(est, X, y, cv) for name, est in candidates().items()}
    return pd.DataFrame.from_dict(rows, orient="index")


def flag_leakage_suspects(results: pd.DataFrame, margin: float = LEAKAGE_MARGIN) -> list[str]:
    baseline_auc = results.loc[BASELINE_NAME, "roc_auc_mean"]
    return [
        name
        for name, row in results.iterrows()
        if name != BASELINE_NAME and row["roc_auc_mean"] - baseline_auc > margin
    ]


def format_metric(results: pd.DataFrame, name: str, metric: str) -> str:
    return f"{results.loc[name, f'{metric}_mean']:.3f} ± {results.loc[name, f'{metric}_std']:.3f}"


def format_report(results: pd.DataFrame, leakage_suspects: list[str]) -> str:
    ranked = results.sort_values("precision_top_mean", ascending=False)
    lines = [
        "# Model comparison",
        "",
        f"Stratified {N_SPLITS}-fold CV, ranked by precision in the top {int(TOP_SHARE * 100)}%.",
        "",
        "| Model | ROC AUC | PR AUC | Precision top 10% | Recall top 10% |",
        "|---|---|---|---|---|",
    ]
    for name in ranked.index:
        lines.append(
            f"| `{name}` | {format_metric(results, name, 'roc_auc')} "
            f"| {format_metric(results, name, 'pr_auc')} "
            f"| {format_metric(results, name, 'precision_top')} "
            f"| {format_metric(results, name, 'recall_top')} |"
        )
    lines.append("")
    if leakage_suspects:
        lines.append(
            "**Leakage suspects** (more than "
            f"{LEAKAGE_MARGIN} ROC AUC above the baseline): {', '.join(leakage_suspects)}"
        )
    else:
        lines.append(f"No candidate beats the baseline by more than {LEAKAGE_MARGIN} ROC AUC.")
    lines.append("")
    return "\n".join(lines)


def write_report(report: str, path: Path = REPORT_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(report)


def main() -> None:
    df = load_data()
    results = run_comparison(df)
    leakage_suspects = flag_leakage_suspects(results)
    report = format_report(results, leakage_suspects)
    write_report(report)
    print(report)


if __name__ == "__main__":
    main()
